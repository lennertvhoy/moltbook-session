"""Monte Carlo readiness model for AI-agent networks.

This model is intentionally presented as an assumption-driven scenario tool.
It is not an empirical forecast. The scenario inputs live in
``data/forecast_scenarios.json`` so the assumptions can be audited directly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"
DATA_PATH = ROOT / "data" / "forecast_scenarios.json"
SEED = 42


@dataclass(frozen=True)
class PillarConfig:
    """Configuration for one readiness pillar."""

    name: str
    code: str
    initial_2026: float
    growth_mu: float
    volatility: float
    neg_shock_prob: float
    neg_shock_size: float
    weight: float


@dataclass(frozen=True)
class Scenario:
    """Container for one scenario's pillar assumptions."""

    name: str
    pillars: tuple[PillarConfig, ...]
    threshold: float
    floor_values: dict[str, float]
    min_consecutive_years: int


def load_config() -> dict[str, Any]:
    """Load the scenario configuration from disk.

    Returns:
        Parsed forecast configuration payload.
    """
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def create_scenarios(config: dict[str, Any]) -> dict[str, Scenario]:
    """Build scenario objects from the JSON config.

    Args:
        config: Parsed forecast configuration.

    Returns:
        Mapping of scenario name to scenario object.
    """
    weights = config["weights"]
    descriptions = config["pillar_descriptions"]
    scenarios: dict[str, Scenario] = {}
    for scenario_data in config["scenarios"]:
        pillars = tuple(
            PillarConfig(
                name=descriptions[pillar["code"]],
                code=pillar["code"],
                initial_2026=float(pillar["initial_2026"]),
                growth_mu=float(pillar["growth_mu"]),
                volatility=float(pillar["volatility"]),
                neg_shock_prob=float(pillar["neg_shock_prob"]),
                neg_shock_size=float(pillar["neg_shock_size"]),
                weight=float(weights[pillar["code"]]),
            )
            for pillar in scenario_data["pillars"]
        )
        scenarios[scenario_data["name"]] = Scenario(
            name=scenario_data["name"],
            pillars=pillars,
            threshold=float(config["threshold"]),
            floor_values={key: float(value) for key, value in config["floor_values"].items()},
            min_consecutive_years=int(config["min_consecutive_years"]),
        )
    return scenarios


class AgentNetworkForecaster:
    """Monte Carlo forecaster for the readiness index."""

    def __init__(self, scenario: Scenario, n_simulations: int = 10000, seed: int = SEED):
        self.scenario = scenario
        self.n_simulations = n_simulations
        self.years = np.arange(2026, 2041)
        self.rng = np.random.default_rng(seed)

    def _simulate_pillar(self, pillar: PillarConfig) -> np.ndarray:
        """Simulate one pillar over time.

        Args:
            pillar: Pillar configuration.

        Returns:
            Matrix of simulated values with shape (n_simulations, n_years).
        """
        values = np.zeros((self.n_simulations, len(self.years)))
        values[:, 0] = pillar.initial_2026

        for year_index in range(1, len(self.years)):
            log_growth = self.rng.normal(
                loc=pillar.growth_mu,
                scale=pillar.volatility,
                size=self.n_simulations,
            )
            shocks = self.rng.random(self.n_simulations) < pillar.neg_shock_prob
            log_growth[shocks] += pillar.neg_shock_size
            values[:, year_index] = np.clip(values[:, year_index - 1] * np.exp(log_growth), 0, 100)

        return values

    def _calculate_readiness_index(self, pillar_values: dict[str, np.ndarray]) -> np.ndarray:
        """Calculate the weighted geometric mean readiness index.

        Args:
            pillar_values: Simulated pillar arrays keyed by pillar code.

        Returns:
            Readiness index matrix.
        """
        index = np.ones((self.n_simulations, len(self.years)))
        for pillar in self.scenario.pillars:
            index *= (pillar_values[pillar.code] / 100.0) ** pillar.weight
        return index * 100.0

    def _check_threshold_crossing(
        self,
        index: np.ndarray,
        pillar_values: dict[str, np.ndarray],
        threshold: float | None = None,
        floor_values: dict[str, float] | None = None,
    ) -> np.ndarray:
        """Determine the first year a simulation crosses and sustains the threshold.

        Args:
            index: Readiness index matrix.
            pillar_values: Simulated pillar arrays.
            threshold: Optional threshold override for sensitivity checks.
            floor_values: Optional floor override for sensitivity checks.

        Returns:
            Crossing years array with NaN for simulations that never cross.
        """
        active_threshold = self.scenario.threshold if threshold is None else threshold
        active_floors = self.scenario.floor_values if floor_values is None else floor_values
        crossing_years = np.full(self.n_simulations, np.nan)

        for simulation_index in range(self.n_simulations):
            consecutive = 0
            for year_idx, year in enumerate(self.years):
                floors_met = all(
                    pillar_values[code][simulation_index, year_idx] >= minimum
                    for code, minimum in active_floors.items()
                )
                if index[simulation_index, year_idx] >= active_threshold and floors_met:
                    consecutive += 1
                    if consecutive >= self.scenario.min_consecutive_years:
                        crossing_years[simulation_index] = year
                        break
                else:
                    consecutive = 0

        return crossing_years

    def run(self) -> dict[str, Any]:
        """Run the full simulation for the configured scenario.

        Returns:
            Dictionary containing simulated pillar values, readiness index, and
            crossing years.
        """
        pillar_values = {pillar.code: self._simulate_pillar(pillar) for pillar in self.scenario.pillars}
        index = self._calculate_readiness_index(pillar_values)
        crossing_years = self._check_threshold_crossing(index, pillar_values)
        return {
            "pillar_values": pillar_values,
            "index": index,
            "crossing_years": crossing_years,
        }

    def calculate_statistics(
        self,
        results: dict[str, Any],
        threshold: float | None = None,
        floor_values: dict[str, float] | None = None,
    ) -> dict[str, Any]:
        """Summarize the simulation results.

        Args:
            results: Output of ``run``.
            threshold: Optional threshold override for sensitivity checks.
            floor_values: Optional floor override for sensitivity checks.

        Returns:
            Summary statistics dictionary.
        """
        crossing_years = results["crossing_years"]
        if threshold is not None or floor_values is not None:
            crossing_years = self._check_threshold_crossing(
                results["index"],
                results["pillar_values"],
                threshold,
                floor_values,
            )
        valid = crossing_years[~np.isnan(crossing_years)]

        stats = {
            "p_by_2030": float(np.mean(crossing_years <= 2030)),
            "p_by_2035": float(np.mean(crossing_years <= 2035)),
            "p_by_2040": float(np.mean(crossing_years <= 2040)),
            "median_year": float(np.median(valid)) if len(valid) else np.nan,
            "p5_year": float(np.percentile(valid, 5)) if len(valid) else np.nan,
            "p95_year": float(np.percentile(valid, 95)) if len(valid) else np.nan,
            "never_crosses": float(np.mean(np.isnan(crossing_years))),
            "n_simulations": self.n_simulations,
            "year_probs": {int(year): float(np.mean(crossing_years <= year)) for year in self.years},
        }
        return stats


def run_all_scenarios(n_simulations: int = 10000) -> dict[str, dict[str, Any]]:
    """Run all configured scenarios.

    Args:
        n_simulations: Number of Monte Carlo runs per scenario.

    Returns:
        Mapping of scenario name to results, forecaster, and statistics.
    """
    config = load_config()
    scenarios = create_scenarios(config)
    all_results: dict[str, dict[str, Any]] = {}

    for index, (name, scenario) in enumerate(scenarios.items()):
        print(f"\nRunning {name} scenario...")
        forecaster = AgentNetworkForecaster(
            scenario=scenario,
            n_simulations=n_simulations,
            seed=SEED + (index * 100),
        )
        results = forecaster.run()
        stats = forecaster.calculate_statistics(results)
        all_results[name] = {
            "scenario": scenario,
            "forecaster": forecaster,
            "results": results,
            "stats": stats,
        }

    return all_results


def run_threshold_sensitivity(
    base_result: dict[str, Any],
    thresholds: list[float],
) -> list[dict[str, Any]]:
    """Run threshold sensitivity checks for the base scenario.

    Args:
        base_result: Base-case result bundle from ``run_all_scenarios``.
        thresholds: Thresholds to test.

    Returns:
        List of threshold sensitivity summaries.
    """
    forecaster: AgentNetworkForecaster = base_result["forecaster"]
    results = base_result["results"]
    sensitivity_rows: list[dict[str, Any]] = []
    for threshold in thresholds:
        stats = forecaster.calculate_statistics(results, threshold=threshold)
        sensitivity_rows.append(
            {
                "Threshold": threshold,
                "P(<=2035)": stats["p_by_2035"],
                "P(<=2040)": stats["p_by_2040"],
                "Median": stats["median_year"],
            }
        )
    return sensitivity_rows


def run_floor_sensitivity(
    base_result: dict[str, Any],
    floor_values: list[float],
) -> list[dict[str, Any]]:
    """Run floor sensitivity checks for the base scenario.

    Args:
        base_result: Base-case result bundle from ``run_all_scenarios``.
        floor_values: Floor values applied to M, R, N, and G.

    Returns:
        List of floor sensitivity summaries.
    """
    forecaster: AgentNetworkForecaster = base_result["forecaster"]
    results = base_result["results"]
    rows: list[dict[str, Any]] = []
    for floor in floor_values:
        stats = forecaster.calculate_statistics(
            results,
            floor_values={code: float(floor) for code in forecaster.scenario.floor_values},
        )
        rows.append(
            {
                "Floor": floor,
                "P(<=2035)": stats["p_by_2035"],
                "P(<=2040)": stats["p_by_2040"],
                "Median": stats["median_year"],
            }
        )
    return rows


def plot_forecast_results(
    all_results: dict[str, dict[str, Any]],
    threshold_sensitivity: list[dict[str, Any]],
    floor_sensitivity: list[dict[str, Any]],
) -> Path:
    """Create the forecast visualization.

    Args:
        all_results: Scenario simulation outputs.
        threshold_sensitivity: Threshold sensitivity summaries.
        floor_sensitivity: Floor sensitivity summaries.

    Returns:
        Path to the saved PNG file.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    colors = {"Conservative": "#1d4ed8", "Base case": "#15803d", "Accelerated": "#dc2626"}

    ax1 = axes[0, 0]
    for scenario_name, payload in all_results.items():
        years = payload["forecaster"].years
        index = payload["results"]["index"]
        median = np.median(index, axis=0)
        p25 = np.percentile(index, 25, axis=0)
        p75 = np.percentile(index, 75, axis=0)
        ax1.plot(years, median, linewidth=2.2, color=colors[scenario_name], label=scenario_name)
        ax1.fill_between(years, p25, p75, color=colors[scenario_name], alpha=0.18)
    ax1.axhline(y=75, color="black", linestyle="--", linewidth=1)
    ax1.set_title("Readiness index trajectories")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Index")
    ax1.set_ylim(0, 100)
    ax1.legend()

    ax2 = axes[0, 1]
    for scenario_name, payload in all_results.items():
        year_probs = payload["stats"]["year_probs"]
        ax2.plot(
            list(year_probs.keys()),
            list(year_probs.values()),
            marker="o",
            linewidth=2,
            color=colors[scenario_name],
            label=scenario_name,
        )
    ax2.set_title("Probability of crossing by year")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Cumulative probability")
    ax2.set_ylim(0, 1)
    ax2.legend()

    ax3 = axes[1, 0]
    crossing_groups = []
    labels = []
    for scenario_name in ("Conservative", "Base case", "Accelerated"):
        valid = all_results[scenario_name]["results"]["crossing_years"]
        valid = valid[~np.isnan(valid)]
        if len(valid):
            crossing_groups.append(valid)
            labels.append(f"{scenario_name}\n(n={len(valid)})")
    boxplot = ax3.boxplot(crossing_groups, tick_labels=labels, patch_artist=True)
    for patch, scenario_name in zip(boxplot["boxes"], ("Conservative", "Base case", "Accelerated"), strict=True):
        patch.set_facecolor(colors[scenario_name])
        patch.set_alpha(0.25)
    ax3.set_title("Crossing-year distribution")
    ax3.set_ylabel("Year")

    ax4 = axes[1, 1]
    ax4.axis("off")
    base_stats = all_results["Base case"]["stats"]
    summary_lines = [
        "Base-case audit notes",
        "",
        f"- Median crossing year: {base_stats['median_year']:.0f}",
        f"- 90% interval among crossings: {base_stats['p5_year']:.0f}-{base_stats['p95_year']:.0f}",
        f"- Never crosses by 2040: {base_stats['never_crosses']:.1%}",
        "",
        "Threshold sensitivity",
    ]
    for row in threshold_sensitivity:
        median = "N/A" if np.isnan(row["Median"]) else f"{row['Median']:.0f}"
        summary_lines.append(
            f"- threshold {row['Threshold']:.0f}: "
            f"P<=2035 {row['P(<=2035)']:.1%}, "
            f"P<=2040 {row['P(<=2040)']:.1%}, "
            f"median {median}"
        )
    summary_lines.append("")
    summary_lines.append("Floor sensitivity")
    for row in floor_sensitivity:
        median = "N/A" if np.isnan(row["Median"]) else f"{row['Median']:.0f}"
        summary_lines.append(
            f"- floors {row['Floor']:.0f}: "
            f"P<=2035 {row['P(<=2035)']:.1%}, "
            f"P<=2040 {row['P(<=2040)']:.1%}, "
            f"median {median}"
        )
    summary_lines.extend(
        [
            "",
            "Interpretation",
            "- Monte Carlo sampling error is small relative to assumption error",
            "- In this parameterization the floor constraints bind before the headline threshold",
            "- Floor choices and scenario inputs move the result more than sampling noise",
            "- Use as a scenario tool, not as a point prediction",
        ]
    )
    ax4.text(
        0.02,
        0.98,
        "\n".join(summary_lines),
        va="top",
        ha="left",
        fontsize=10,
        family="monospace",
        bbox={"boxstyle": "round,pad=0.6", "facecolor": "#f8fafc", "edgecolor": "#cbd5e1"},
    )

    fig.suptitle("AI-agent network readiness model", fontsize=16, fontweight="bold")
    fig.tight_layout()

    output_path = ASSETS_DIR / "forecast_distribution.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def print_forecast_report(
    all_results: dict[str, dict[str, Any]],
    threshold_sensitivity: list[dict[str, Any]],
    floor_sensitivity: list[dict[str, Any]],
) -> None:
    """Print the audit-friendly forecast summary.

    Args:
        all_results: Scenario simulation outputs.
        threshold_sensitivity: Threshold sensitivity summaries.
        floor_sensitivity: Floor sensitivity summaries.
    """
    print("=" * 72)
    print("AI-AGENT NETWORK FORECAST (ASSUMPTION-DRIVEN)")
    print("=" * 72)

    print("\nModel standard")
    print("-" * 72)
    first = next(iter(all_results.values()))
    scenario: Scenario = first["scenario"]
    print(f"Simulations per scenario: {first['stats']['n_simulations']:,}")
    print(f"Threshold: {scenario.threshold:.0f}")
    print(
        "Floor constraints: "
        + ", ".join(f"{code}>={value:.0f}" for code, value in scenario.floor_values.items())
    )
    print(f"Minimum consecutive years: {scenario.min_consecutive_years}")
    print(f"Random seed: {SEED}")

    print("\nResults by scenario")
    print("-" * 72)
    for scenario_name in ("Conservative", "Base case", "Accelerated"):
        stats = all_results[scenario_name]["stats"]
        median = "N/A" if np.isnan(stats["median_year"]) else f"{stats['median_year']:.0f}"
        interval = (
            "N/A"
            if np.isnan(stats["p5_year"])
            else f"{stats['p5_year']:.0f}-{stats['p95_year']:.0f}"
        )
        print(f"\n{scenario_name}")
        print(f"  P(Level-3 by 2030): {stats['p_by_2030']:.1%}")
        print(f"  P(Level-3 by 2035): {stats['p_by_2035']:.1%}")
        print(f"  P(Level-3 by 2040): {stats['p_by_2040']:.1%}")
        print(f"  Median crossing year: {median}")
        print(f"  90% interval among crossings: {interval}")
        print(f"  Never crosses by 2040: {stats['never_crosses']:.1%}")

    print("\nThreshold sensitivity (base case)")
    print("-" * 72)
    for row in threshold_sensitivity:
        median = "N/A" if np.isnan(row["Median"]) else f"{row['Median']:.0f}"
        print(
            f"threshold {row['Threshold']:.0f}: "
            f"P<=2035 {row['P(<=2035)']:.1%}, "
            f"P<=2040 {row['P(<=2040)']:.1%}, "
            f"median {median}"
        )

    print("\nFloor sensitivity (base case)")
    print("-" * 72)
    for row in floor_sensitivity:
        median = "N/A" if np.isnan(row["Median"]) else f"{row['Median']:.0f}"
        print(
            f"floors {row['Floor']:.0f}: "
            f"P<=2035 {row['P(<=2035)']:.1%}, "
            f"P<=2040 {row['P(<=2040)']:.1%}, "
            f"median {median}"
        )

    print("\nInterpretation")
    print("-" * 72)
    print("This model is useful for structured discussion of assumptions.")
    print("It should not be presented as a data-derived point forecast.")
    print("In this parameterization, floor constraints bind before the headline threshold.")
    print("Scenario inputs and floor choices dominate the output.")
    print("\n" + "=" * 72)


def main() -> None:
    """Run the forecast model and save the figure."""
    all_results = run_all_scenarios()
    config = load_config()
    threshold_sensitivity = run_threshold_sensitivity(
        all_results["Base case"],
        thresholds=[float(value) for value in config["sensitivity_thresholds"]],
    )
    floor_sensitivity = run_floor_sensitivity(
        all_results["Base case"],
        floor_values=[float(value) for value in config["sensitivity_floor_values"]],
    )
    print_forecast_report(all_results, threshold_sensitivity, floor_sensitivity)
    output_path = plot_forecast_results(all_results, threshold_sensitivity, floor_sensitivity)
    print(f"\nSaved figure: {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
