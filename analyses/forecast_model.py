"""Monte Carlo readiness model for AI-agent networks.

This model is intentionally presented as an assumption-driven scenario tool.
It is not an empirical forecast. The scenario inputs live in
``data/forecast_scenarios.json`` so the assumptions can be audited directly.

VERSION 2 ENHANCEMENTS (2026-03-25):
- Latent capability scale: Transforms 0-100 pillars to logit scale
- Local linear trend model: State-space with stochastic growth rate
- Natural saturation: Sigmoid transform creates asymptotic approach to 100
- Uncertainty decomposition: Level, trend, regime, and shock components

Mathematical foundation:
    z_t = logit(y_t/100) = log(y_t / (100 - y_t))
    
    State equations (Model C - Local Linear Trend):
        z_t = z_{t-1} + g_t + eps_t      (level, eps_t ~ N(0, sigma_level))
        g_t = phi*g_{t-1} + (1-phi)*g_bar + eta_t  (growth, eta_t ~ N(0, sigma_growth))
    
    Where:
        z_t = latent capability level (logit scale)
        g_t = latent growth rate
        g_bar = long-run mean growth rate
        phi = persistence parameter (0.9)
        eps_t, eta_t = level and growth shocks
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"
DATA_PATH = ROOT / "data" / "forecast_scenarios.json"
SEED = 42


def to_logit(y: np.ndarray) -> np.ndarray:
    """Transform 0-100 scores to logit scale.
    
    Mathematical definition:
        z = log(y / (100 - y))
        
    This maps:
        y=50  → z=0
        y=90  → z≈2.2
        y=99  → z≈4.6
        y→100 → z→∞ (asymptotic saturation)
    """
    y_clipped = np.clip(y, 0.01, 99.99)
    return np.log(y_clipped / (100 - y_clipped))


def from_logit(z: np.ndarray) -> np.ndarray:
    """Transform logit scale back to 0-100 scores.
    
    Mathematical definition:
        y = 100 / (1 + exp(-z)) = 100 * sigmoid(z)
    """
    return 100.0 / (1.0 + np.exp(-z))


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
    growth_volatility: float = 0.02  # For local linear trend model


@dataclass(frozen=True)
class Scenario:
    """Container for one scenario's pillar assumptions."""
    name: str
    pillars: tuple[PillarConfig, ...]
    threshold: float
    floor_values: dict[str, float]
    min_consecutive_years: int


def load_config() -> dict[str, Any]:
    """Load the scenario configuration from disk."""
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def create_scenarios(config: dict[str, Any]) -> dict[str, Scenario]:
    """Build scenario objects from the JSON config."""
    weights = config["weights"]
    descriptions = config["pillar_descriptions"]
    
    # Scenario-specific growth volatility
    growth_vol_scenarios = {
        "Conservative": 0.03,
        "Base case": 0.02,
        "Accelerated": 0.015,
    }
    
    scenarios: dict[str, Scenario] = {}
    for scenario_data in config["scenarios"]:
        scenario_name = scenario_data["name"]
        growth_vol = growth_vol_scenarios.get(scenario_name, 0.02)
        
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
                growth_volatility=growth_vol,
            )
            for pillar in scenario_data["pillars"]
        )
        scenarios[scenario_name] = Scenario(
            name=scenario_name,
            pillars=pillars,
            threshold=float(config["threshold"]),
            floor_values={key: float(value) for key, value in config["floor_values"].items()},
            min_consecutive_years=int(config["min_consecutive_years"]),
        )
    return scenarios


class GrowthModel(ABC):
    """Abstract base class for growth dynamics models."""
    
    def __init__(self, rng: np.random.Generator):
        self.rng = rng
    
    @abstractmethod
    def simulate_pillar(
        self, 
        pillar: PillarConfig, 
        n_simulations: int, 
        n_years: int
    ) -> np.ndarray:
        """Simulate pillar evolution over time."""
        pass


class ModelA_FixedLogGrowth(GrowthModel):
    """Model A: Fixed log-growth on logit scale (backward compatible).
    
    Equation:
        z_t = z_{t-1} + growth_mu + N(0, volatility)
        y_t = sigmoid(z_t) * 100
    """
    
    def simulate_pillar(
        self, 
        pillar: PillarConfig, 
        n_simulations: int, 
        n_years: int
    ) -> np.ndarray:
        """Simulate with fixed growth rate on logit scale."""
        z_values = np.zeros((n_simulations, n_years))
        z_values[:, 0] = to_logit(pillar.initial_2026)
        
        for t in range(1, n_years):
            growth_shock = self.rng.normal(
                loc=pillar.growth_mu,
                scale=pillar.volatility,
                size=n_simulations,
            )
            shocks = self.rng.random(n_simulations) < pillar.neg_shock_prob
            growth_shock[shocks] += pillar.neg_shock_size
            z_values[:, t] = z_values[:, t - 1] + growth_shock
        
        return from_logit(z_values)


class ModelB_PiecewiseGrowth(GrowthModel):
    """Model B: Piecewise growth with breakpoint.
    
    Before breakpoint: growth rate g1
    After breakpoint: growth rate g2 (accelerated)
    """
    
    def __init__(self, rng: np.random.Generator, breakpoint_year: int = 2028):
        super().__init__(rng)
        self.breakpoint_year = breakpoint_year
    
    def simulate_pillar(
        self, 
        pillar: PillarConfig, 
        n_simulations: int, 
        n_years: int
    ) -> np.ndarray:
        """Simulate with piecewise growth rates."""
        years = np.arange(2026, 2026 + n_years)
        
        if self.breakpoint_year < 2026:
            growth_pre = pillar.growth_mu
            growth_post = pillar.growth_mu * 1.2
            in_pre_regime = np.zeros(n_years, dtype=bool)
        else:
            growth_pre = pillar.growth_mu
            growth_post = pillar.growth_mu * 1.3
            in_pre_regime = years < self.breakpoint_year
        
        z_values = np.zeros((n_simulations, n_years))
        z_values[:, 0] = to_logit(pillar.initial_2026)
        
        for t in range(1, n_years):
            mean_growth = growth_pre if in_pre_regime[t] else growth_post
            growth_shock = self.rng.normal(
                loc=mean_growth,
                scale=pillar.volatility,
                size=n_simulations,
            )
            shocks = self.rng.random(n_simulations) < pillar.neg_shock_prob
            growth_shock[shocks] += pillar.neg_shock_size
            z_values[:, t] = z_values[:, t - 1] + growth_shock
        
        return from_logit(z_values)


class ModelC_LocalLinearTrend(GrowthModel):
    """Model C: Local linear trend state-space model (DEFAULT).
    
    State equations on logit scale:
        z_t = z_{t-1} + g_t + eps_t      (level equation)
        g_t = phi*g_{t-1} + (1-phi)*g_bar + eta_t  (growth equation)
    
    Where:
        z_t = latent capability level
        g_t = latent growth rate (mean-reverting to g_bar)
        phi = persistence parameter (default 0.9)
        eps_t ~ N(0, sigma_level), eta_t ~ N(0, sigma_growth)
    """
    
    def __init__(self, rng: np.random.Generator, persistence: float = 0.9):
        super().__init__(rng)
        self.persistence = persistence  # phi
    
    def simulate_pillar(
        self, 
        pillar: PillarConfig, 
        n_simulations: int, 
        n_years: int
    ) -> np.ndarray:
        """Simulate with local linear trend on logit scale."""
        z_values = np.zeros((n_simulations, n_years))
        z_values[:, 0] = to_logit(pillar.initial_2026)
        
        # Initialize latent growth rate with uncertainty
        g_values = np.full(n_simulations, pillar.growth_mu) + self.rng.normal(
            0, 0.05, n_simulations
        )
        
        sigma_level = pillar.volatility
        sigma_growth = pillar.growth_volatility
        
        for t in range(1, n_years):
            # Growth equation with mean reversion
            g_values = (
                self.persistence * g_values 
                + (1 - self.persistence) * pillar.growth_mu 
                + self.rng.normal(0, sigma_growth, n_simulations)
            )
            
            # Level equation
            level_shock = self.rng.normal(0, sigma_level, n_simulations)
            shocks = self.rng.random(n_simulations) < pillar.neg_shock_prob
            level_shock[shocks] += pillar.neg_shock_size
            
            z_values[:, t] = z_values[:, t - 1] + g_values + level_shock
        
        return from_logit(z_values)


class AgentNetworkForecaster:
    """Monte Carlo forecaster for the readiness index.
    
    Uses Model C (Local Linear Trend) as default for enhanced accuracy.
    Set model_type='A' for backward compatibility with original fixed-growth model.
    """

    def __init__(
        self, 
        scenario: Scenario, 
        n_simulations: int = 10000, 
        seed: int = SEED,
        model_type: str = "C",  # "A", "B", or "C"
    ):
        self.scenario = scenario
        self.n_simulations = n_simulations
        self.years = np.arange(2026, 2041)
        self.rng = np.random.default_rng(seed)
        self.model_type = model_type
        
        # Create appropriate growth model
        if model_type == "A":
            self.model = ModelA_FixedLogGrowth(self.rng)
        elif model_type == "B":
            self.model = ModelB_PiecewiseGrowth(self.rng, breakpoint_year=2028)
        else:
            self.model = ModelC_LocalLinearTrend(self.rng, persistence=0.9)

    def _simulate_pillar(self, pillar: PillarConfig) -> np.ndarray:
        """Simulate one pillar over time using the selected growth model."""
        return self.model.simulate_pillar(pillar, self.n_simulations, len(self.years))

    def _calculate_readiness_index(self, pillar_values: dict[str, np.ndarray]) -> np.ndarray:
        """Calculate the weighted geometric mean readiness index."""
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
        """Determine the first year a simulation crosses and sustains the threshold."""
        active_threshold = self.scenario.threshold if threshold is None else threshold
        active_floors = self.scenario.floor_values if floor_values is None else floor_values
        crossing_years = np.full(self.n_simulations, np.nan)

        for sim_idx in range(self.n_simulations):
            consecutive = 0
            for year_idx, year in enumerate(self.years):
                floors_met = all(
                    pillar_values[code][sim_idx, year_idx] >= minimum
                    for code, minimum in active_floors.items()
                )
                if index[sim_idx, year_idx] >= active_threshold and floors_met:
                    consecutive += 1
                    if consecutive >= self.scenario.min_consecutive_years:
                        crossing_years[sim_idx] = year
                        break
                else:
                    consecutive = 0

        return crossing_years

    def run(self) -> dict[str, Any]:
        """Run the full simulation for the configured scenario."""
        pillar_values = {
            pillar.code: self._simulate_pillar(pillar) 
            for pillar in self.scenario.pillars
        }
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
        """Summarize the simulation results."""
        crossing_years = results["crossing_years"]
        if threshold is not None or floor_values is not None:
            crossing_years = self._check_threshold_crossing(
                results["index"],
                results["pillar_values"],
                threshold,
                floor_values,
            )
        valid = crossing_years[~np.isnan(crossing_years)]

        return {
            "p_by_2030": float(np.mean(crossing_years <= 2030)),
            "p_by_2035": float(np.mean(crossing_years <= 2035)),
            "p_by_2040": float(np.mean(crossing_years <= 2040)),
            "median_year": float(np.median(valid)) if len(valid) else np.nan,
            "p5_year": float(np.percentile(valid, 5)) if len(valid) else np.nan,
            "p95_year": float(np.percentile(valid, 95)) if len(valid) else np.nan,
            "never_crosses": float(np.mean(np.isnan(crossing_years))),
            "n_simulations": self.n_simulations,
            "year_probs": {int(year): float(np.mean(crossing_years <= year)) for year in self.years},
            "model_type": self.model_type,
        }


def run_all_scenarios(
    n_simulations: int = 10000,
    model_type: str = "C"
) -> dict[str, dict[str, Any]]:
    """Run all configured scenarios.
    
    Args:
        n_simulations: Number of Monte Carlo runs per scenario
        model_type: "A"=Fixed growth, "B"=Piecewise, "C"=Local Linear Trend (default)
    """
    config = load_config()
    scenarios = create_scenarios(config)
    all_results: dict[str, dict[str, Any]] = {}

    for idx, (name, scenario) in enumerate(scenarios.items()):
        print(f"\nRunning {name} scenario with Model {model_type}...")
        forecaster = AgentNetworkForecaster(
            scenario=scenario,
            n_simulations=n_simulations,
            seed=SEED + (idx * 100),
            model_type=model_type,
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
    """Run threshold sensitivity checks for the base scenario."""
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
    """Run floor sensitivity checks for the base scenario."""
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
    """Create the forecast visualization."""
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
    ax1.set_title("Readiness index trajectories (Model C: Local Linear Trend)")
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
    
    # Get model type from results
    model_used = base_stats.get("model_type", "C")
    model_desc = {
        "A": "Fixed Log-Growth (baseline)",
        "B": "Piecewise Growth",
        "C": "Local Linear Trend (state-space)",
    }.get(model_used, "Unknown")
    
    summary_lines = [
        "Base-case audit notes",
        f"Model: {model_desc}",
        "",
        f"- Median crossing year: {base_stats['median_year']:.0f}",
        f"- 90% interval among crossings: {base_stats['p5_year']:.0f}-{base_stats['p95_year']:.0f}",
        f"- Never crosses by 2040: {base_stats['never_crosses']:.1%}",
        "",
        "Mathematical enhancements:",
        "- Logit transform: z = log(y/(100-y))",
        "- Sigmoid saturation: natural flattening near 100",
        "- Local linear trend: g_t evolves stochastically",
        "- Mean reversion: phi=0.9 prevents explosive growth",
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
            "- In this parameterization the floor constraints bind before headline threshold",
            "- Logit transform creates natural saturation approaching 100",
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

    fig.suptitle("AI-agent network readiness model (v2 - Latent State-Space)", fontsize=16, fontweight="bold")
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
    """Print the audit-friendly forecast summary."""
    print("=" * 72)
    print("AI-AGENT NETWORK FORECAST (ENHANCED MODEL V2)")
    print("=" * 72)

    print("\nModel standard")
    print("-" * 72)
    first = next(iter(all_results.values()))
    scenario: Scenario = first["scenario"]
    model_type = first["stats"].get("model_type", "C")
    model_names = {"A": "Fixed Log-Growth", "B": "Piecewise", "C": "Local Linear Trend"}
    print(f"Growth model: Model {model_type} ({model_names.get(model_type, 'Unknown')})")
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

    print("\nMathematical foundation")
    print("-" * 72)
    print("The model uses a logit transform for natural saturation:")
    print("  z = logit(y/100) = log(y/(100-y))  [latent capability]")
    print("  y = 100 × sigmoid(z) = 100/(1+exp(-z))  [bounded score]")
    print("")
    print("Growth dynamics (Model C - Local Linear Trend):")
    print("  z_t = z_{t-1} + g_t + eps_t           (level)")
    print("  g_t = φ·g_{t-1} + (1-φ)·ḡ + η_t       (growth, φ=0.9)")
    print("")
    print("Where:")
    print("  z_t = latent capability (logit scale)")
    print("  g_t = time-varying growth rate")
    print("  eps_t ~ N(0, σ_level) = level shock")
    print("  η_t ~ N(0, σ_growth) = growth rate shock")

    print("\nInterpretation")
    print("-" * 72)
    print("This model is useful for structured discussion of assumptions.")
    print("It should not be presented as a data-derived point forecast.")
    print("In this parameterization, floor constraints bind before the headline threshold.")
    print("Scenario inputs and floor choices dominate the output.")
    print("\n" + "=" * 72)


def main() -> None:
    """Run the forecast model and save the figure."""
    import sys
    
    # Allow model selection via command line
    model_type = "C"  # Default to Local Linear Trend
    if len(sys.argv) > 1 and sys.argv[1] in ["A", "B", "C"]:
        model_type = sys.argv[1]
    
    print(f"Running with Model {model_type}")
    print("  A = Fixed Log-Growth (backward compatible)")
    print("  B = Piecewise Growth (breakpoint 2028)")
    print("  C = Local Linear Trend (default, recommended)")
    
    all_results = run_all_scenarios(model_type=model_type)
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
