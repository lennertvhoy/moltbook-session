"""Monte Carlo hazard model for AI-agent network emergence.

This model implements a discrete-time hazard rate approach with soft feasibility
functions for bounded-scope emergence forecasting.

VERSION 4 (SOFT FEASIBILITY - CANONICAL):
- Discrete-time hazard model: h(t) = baseline × capability_effect × feasibility
- Soft feasibility φ(y; θ, k): sigmoid function for gradual emergence
- Single event: bounded-scope emergence (first functional networks)
- Output: cumulative emergence probability over time
- No hard floors, no threshold crossing, no two-year rule

Mathematical model:
    h(t) = h0 × exp(λ_C·z_C + λ_E·z_E + λ_D·z_D + λ_M·z_M) 
           × φ_G(y_G) × φ_N(y_N) × φ_R(y_R)
    
    φ(y; θ, k) = 1 / (1 + exp(-k × (y - θ) / 10))
    
    P(emergent by year T) = 1 - exp(-Σ_{t=1}^{T} h(t))

Where:
    h(t) = hazard rate (instantaneous emergence probability)
    h0 = baseline hazard (calibration parameter)
    z_i = latent capability on logit scale
    y_i = observed score 0-100
    φ_i(y_i) = soft feasibility for governance, network, reliability
    θ_i = inflection point (where feasibility = 50%)
    k_i = steepness parameter
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
    growth_volatility: float = 0.02


@dataclass(frozen=True)
class SoftFeasibilityParams:
    """Parameters for soft feasibility function φ(y; θ, k)."""
    theta: float  # Inflection point (feasibility = 50%)
    k: float      # Steepness parameter


@dataclass(frozen=True)
class Scenario:
    """Container for one scenario's assumptions."""
    name: str
    pillars: tuple[PillarConfig, ...]
    h0: float  # Baseline hazard
    # Soft feasibility parameters for G, N, R
    feasibility_params: dict[str, SoftFeasibilityParams]


def to_logit(y: np.ndarray) -> np.ndarray:
    """Transform 0-100 scores to logit scale."""
    y_clipped = np.clip(y, 0.01, 99.99)
    return np.log(y_clipped / (100 - y_clipped))


def from_logit(z: np.ndarray) -> np.ndarray:
    """Transform logit scale back to 0-100 scores."""
    return 100.0 / (1.0 + np.exp(-z))


def soft_feasibility(y: float, theta: float, k: float) -> float:
    """Compute soft feasibility φ(y; θ, k).
    
    φ(y; θ, k) = 1 / (1 + exp(-k × (y - θ) / 10))
    
    Args:
        y: Observed score (0-100)
        theta: Inflection point where feasibility = 50%
        k: Steepness parameter (higher = sharper transition)
    
    Returns:
        Feasibility value between 0 and 1
    """
    return 1.0 / (1.0 + np.exp(-k * (y - theta) / 10.0))


def compute_hazard(
    pillars: dict[str, float],
    logit_pillars: dict[str, float],
    h0: float,
    loadings: dict[str, float],
    feasibility_params: dict[str, SoftFeasibilityParams],
) -> float:
    """Compute hazard rate h(t) for given pillar values.
    
    h(t) = h0 × exp(Σ λ_i × z_i) × Π φ_j(y_j)
    
    Args:
        pillars: Current pillar scores (0-100)
        logit_pillars: Current pillar scores on logit scale
        h0: Baseline hazard
        loadings: Loading factors (λ) for each pillar
        feasibility_params: Soft feasibility params for G, N, R
    
    Returns:
        Hazard rate h(t)
    """
    # Capability effect: exp(Σ λ_i × z_i)
    capability_contrib = 0.0
    for code in ["C", "E", "D", "M"]:
        capability_contrib += loadings[code] * logit_pillars[code]
    capability_effect = np.exp(capability_contrib)
    
    # Feasibility effects: Π φ_j(y_j)
    feasibility_effect = 1.0
    for code in ["G", "N", "R"]:
        params = feasibility_params[code]
        phi = soft_feasibility(pillars[code], params.theta, params.k)
        feasibility_effect *= phi
    
    return h0 * capability_effect * feasibility_effect


def load_config() -> dict[str, Any]:
    """Load the scenario configuration from disk."""
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def create_scenarios(config: dict[str, Any]) -> dict[str, Scenario]:
    """Build scenario objects from the JSON config."""
    weights = config["weights"]
    descriptions = config["pillar_descriptions"]
    
    growth_vol_scenarios = {
        "Conservative": 0.03,
        "Base case": 0.02,
        "Accelerated": 0.015,
    }
    
    # Soft feasibility parameters (expert judgment ranges)
    feasibility_scenarios = {
        "Conservative": {
            "G": SoftFeasibilityParams(theta=45.0, k=0.12),
            "N": SoftFeasibilityParams(theta=50.0, k=0.12),
            "R": SoftFeasibilityParams(theta=55.0, k=0.12),
        },
        "Base case": {
            "G": SoftFeasibilityParams(theta=40.0, k=0.10),
            "N": SoftFeasibilityParams(theta=45.0, k=0.10),
            "R": SoftFeasibilityParams(theta=50.0, k=0.10),
        },
        "Accelerated": {
            "G": SoftFeasibilityParams(theta=35.0, k=0.08),
            "N": SoftFeasibilityParams(theta=40.0, k=0.08),
            "R": SoftFeasibilityParams(theta=45.0, k=0.08),
        },
    }
    
    # Baseline hazard per scenario
    h0_scenarios = {
        "Conservative": 0.03,   # Lower baseline emergence probability
        "Base case": 0.05,      # Moderate
        "Accelerated": 0.08,    # Higher
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
            h0=h0_scenarios[scenario_name],
            feasibility_params=feasibility_scenarios[scenario_name],
        )
    
    return scenarios


def simulate_trajectory(
    scenario: Scenario,
    years: np.ndarray,
    rng: np.random.Generator,
    phi: float = 0.9,
    enable_coupling: bool = True,
    regime_switch: str | None = None,
) -> dict[str, np.ndarray]:
    """Simulate one trajectory with local linear trend model.
    
    Includes light coupling (C/E → D → N) and optional regime switches.
    
    Args:
        scenario: Scenario configuration
        years: Array of years to simulate
        rng: Random number generator
        phi: Growth persistence parameter
        enable_coupling: If True, apply C/E → D → N feedback
        regime_switch: None, 'interop', or 'regulatory' for discrete boosts
    
    Returns dict with pillar trajectories and emergence probability.
    """
    n_years = len(years)
    
    # Initialize storage
    pillars: dict[str, np.ndarray] = {}
    logit_pillars: dict[str, np.ndarray] = {}
    
    # First pass: simulate base dynamics for all pillars
    for pillar in scenario.pillars:
        z = np.zeros(n_years)
        g = np.zeros(n_years)
        
        # Initial conditions
        y0 = pillar.initial_2026
        z[0] = to_logit(np.array([y0]))[0]
        g[0] = pillar.growth_mu
        
        for t in range(1, n_years):
            # Growth evolution with persistence
            g[t] = (
                phi * g[t-1]
                + (1 - phi) * pillar.growth_mu
                + rng.normal(0, pillar.growth_volatility)
            )
            
            # Level evolution
            level_shock = rng.normal(0, pillar.volatility)
            z[t] = z[t-1] + g[t] + level_shock
            
            # Negative shocks (regime events)
            if rng.random() < pillar.neg_shock_prob:
                z[t] -= pillar.neg_shock_size
        
        logit_pillars[pillar.code] = z
        pillars[pillar.code] = from_logit(z)
    
    # Second pass: apply coupling if enabled (C/E → D → N)
    if enable_coupling:
        for t in range(1, n_years):
            # Demand gets boost from Capability and Efficiency
            c_boost = 0.15 * (pillars["C"][t-1] - 50) / 50  # +15% effect
            e_boost = 0.15 * (pillars["E"][t-1] - 40) / 40
            total_d_boost = c_boost + e_boost
            
            # Apply demand boost (modest, capped)
            logit_pillars["D"][t] += total_d_boost * 0.3  # Dampened effect
            pillars["D"][t] = from_logit(logit_pillars["D"][t])
            
            # Network gets boost from Demand (standardization pressure)
            d_level = pillars["D"][t]
            if d_level > 45:  # Only when demand is substantial
                n_boost = 0.10 * (d_level - 45) / 55  # +10% at high demand
                logit_pillars["N"][t] += n_boost * 0.25
                pillars["N"][t] = from_logit(logit_pillars["N"][t])
    
    # Apply regime switches (discrete events)
    if regime_switch == "interop":
        # MCP/A2A adoption boost around 2028-2029
        for i, year in enumerate(years):
            if 2028 <= year <= 2029:
                # Network gets step boost from standardization
                logit_pillars["N"][i] += 0.3  # ~7 point boost on 0-100 scale
                pillars["N"][i] = from_logit(logit_pillars["N"][i])
    
    elif regime_switch == "regulatory":
        # AI Act phased implementation boosts Governance
        for i, year in enumerate(years):
            if year == 2026:
                logit_pillars["G"][i] += 0.15  # Entry into force
            elif year == 2027:
                logit_pillars["G"][i] += 0.25  # Full applicability
                pillars["G"][i] = from_logit(logit_pillars["G"][i])
    
    return {"pillars": pillars, "logit_pillars": logit_pillars}


def compute_emergence_probability(
    scenario: Scenario,
    years: np.ndarray,
    trajectory: dict[str, np.ndarray],
) -> np.ndarray:
    """Compute cumulative emergence probability from trajectory.
    
    Uses hazard rate accumulation:
        P(emergent by T) = 1 - exp(-Σ_{t=1}^{T} h(t))
    """
    n_years = len(years)
    pillars = trajectory["pillars"]
    logit_pillars = trajectory["logit_pillars"]
    
    # Loadings (weights, normalized)
    loadings = {p.code: p.weight for p in scenario.pillars}
    
    # Compute hazard rate each year
    hazards = np.zeros(n_years)
    for t in range(n_years):
        p_t = {code: pillars[code][t] for code in pillars}
        z_t = {code: logit_pillars[code][t] for code in logit_pillars}
        
        hazards[t] = compute_hazard(
            p_t, z_t, scenario.h0, loadings, scenario.feasibility_params
        )
    
    # Cumulative hazard and survival probability
    cum_hazard = np.cumsum(hazards)
    survival_prob = np.exp(-cum_hazard)
    emergence_prob = 1 - survival_prob
    
    return emergence_prob


def run_monte_carlo(
    scenario: Scenario,
    n_sims: int = 5000,
    years: np.ndarray | None = None,
    enable_coupling: bool = True,
    regime_switch: str | None = None,
) -> dict[str, Any]:
    """Run Monte Carlo simulation for a scenario.
    
    Args:
        scenario: Scenario configuration
        n_sims: Number of Monte Carlo simulations
        years: Years to simulate (default 2026-2040)
        enable_coupling: Enable C/E → D → N feedback
        regime_switch: None, 'interop', or 'regulatory'
    
    Returns emergence probability distributions over time.
    """
    if years is None:
        years = np.arange(2026, 2041)
    
    rng = np.random.default_rng(SEED)
    n_years = len(years)
    
    # Store emergence probabilities for all simulations
    all_probs = np.zeros((n_sims, n_years))
    
    for i in range(n_sims):
        trajectory = simulate_trajectory(
            scenario, years, rng,
            enable_coupling=enable_coupling,
            regime_switch=regime_switch
        )
        all_probs[i, :] = compute_emergence_probability(scenario, years, trajectory)
    
    return {
        "years": years,
        "mean": np.mean(all_probs, axis=0),
        "median": np.median(all_probs, axis=0),
        "p25": np.percentile(all_probs, 25, axis=0),
        "p75": np.percentile(all_probs, 75, axis=0),
        "p10": np.percentile(all_probs, 10, axis=0),
        "p90": np.percentile(all_probs, 90, axis=0),
        "individual": all_probs[:100],  # Store 100 trajectories for viz
    }


def plot_scenario_comparison(results: dict[str, Any]) -> None:
    """Plot emergence probability comparison across scenarios."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = {
        "Conservative": "#e74c3c",
        "Base case": "#3498db",
        "Accelerated": "#2ecc71",
    }
    
    for scenario_name, data in results.items():
        years = data["years"]
        color = colors.get(scenario_name, "gray")
        
        # Plot median
        ax.plot(years, data["median"] * 100, 
                label=scenario_name, color=color, linewidth=2)
        
        # Plot 25-75 percentile band
        ax.fill_between(years, 
                        data["p25"] * 100, 
                        data["p75"] * 100,
                        alpha=0.2, color=color)
    
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Cumulative Emergence Probability (%)", fontsize=12)
    ax.set_title("Bounded-Scope Emergence Forecast\nFirst functional agent networks", 
                 fontsize=14, fontweight="bold")
    ax.legend(loc="upper left")
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(ASSETS_DIR / "forecast_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {ASSETS_DIR / 'forecast_distribution.png'}")


def print_summary_table(results: dict[str, Any]) -> None:
    """Print summary table of emergence probabilities."""
    print("\n" + "=" * 80)
    print("BOUNDED-SCOPE EMERGENCE FORECAST")
    print("First functional agent networks (Moltbook-like)")
    print("=" * 80)
    print("\nCumulative emergence probability by year:")
    print("-" * 60)
    print(f"{'Year':<8} {'Conservative':<15} {'Base case':<15} {'Accelerated':<15}")
    print("-" * 60)
    
    years = list(results.values())[0]["years"]
    for i, year in enumerate(years):
        if year % 2 == 0:  # Print every 2 years
            row = f"{year:<8}"
            for scenario in ["Conservative", "Base case", "Accelerated"]:
                if scenario in results:
                    prob = results[scenario]["median"][i] * 100
                    row += f"{prob:>6.1f}%        "
                else:
                    row += f"{'N/A':>15}"
            print(row)
    
    print("-" * 60)
    print("\nKey years (50% median emergence probability):")
    for scenario_name, data in results.items():
        median_probs = data["median"]
        years = data["years"]
        # Find first year where median >= 0.5
        above_50 = np.where(median_probs >= 0.5)[0]
        if len(above_50) > 0:
            year_50 = years[above_50[0]]
            print(f"  {scenario_name}: ~{year_50}")
        else:
            print(f"  {scenario_name}: >2040 (not reached in forecast horizon)")
    
    print("\n" + "=" * 80)
    print("Model: Discrete-time hazard with soft feasibility")
    print("φ(y; θ, k) = 1 / (1 + exp(-k × (y - θ) / 10))")
    print("=" * 80 + "\n")


def print_regime_comparison_table(baseline: dict, interop: dict) -> None:
    """Print comparison between baseline and interop regime scenarios."""
    print("\n" + "=" * 80)
    print("REGIME SWITCH COMPARISON (Base case)")
    print("=" * 80)
    print("\nEffect of 'interop convergence' regime (MCP/A2A standardization 2028-2029):")
    print("-" * 70)
    print(f"{'Year':<8} {'Baseline':<20} {'+Interop':<20} {'Difference':<20}")
    print("-" * 70)
    
    years = baseline["years"]
    for i, year in enumerate(years):
        if year % 2 == 0:
            base_prob = baseline["median"][i] * 100
            interop_prob = interop["median"][i] * 100
            diff = interop_prob - base_prob
            print(f"{year:<8} {base_prob:>6.1f}%{'':<13} {interop_prob:>6.1f}%{'':<13} +{diff:>5.1f}%")
    
    print("-" * 70)
    print("\nNote: Interop regime assumes successful MCP/A2A adoption around 2028-2029")
    print("=" * 80 + "\n")


def main() -> None:
    """Run the full forecast analysis with structural improvements."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    config = load_config()
    scenarios = create_scenarios(config)
    
    years = np.arange(2026, 2041)
    
    print("=" * 80)
    print("BOUNDED-SCOPE EMERGENCE FORECAST")
    print("Model: Hazard rate with soft feasibility + light coupling + regime switches")
    print("=" * 80)
    print("\nStructural features:")
    print("  • Soft feasibility: φ(y; θ, k) — gradual emergence, no hard floors")
    print("  • Light coupling: C/E → D → N (capability drives demand drives network)")
    print("  • Regime switches: Optional discrete boosts for standards/regulation")
    print("=" * 80 + "\n")
    
    # Run baseline scenarios (with coupling, no regime switches)
    print("Running BASELINE scenarios (with coupling)...")
    results = {}
    for scenario_name, scenario in scenarios.items():
        print(f"  Running {scenario_name}...")
        results[scenario_name] = run_monte_carlo(
            scenario, n_sims=5000, years=years,
            enable_coupling=True, regime_switch=None
        )
    
    # Run interop regime scenario for comparison
    print("\nRunning INTEROP REGIME scenario (Base case + MCP/A2A boost)...")
    interop_result = run_monte_carlo(
        scenarios["Base case"], n_sims=5000, years=years,
        enable_coupling=True, regime_switch="interop"
    )
    
    plot_scenario_comparison(results)
    print_summary_table(results)
    print_regime_comparison_table(results["Base case"], interop_result)
    
    print("\n✓ Forecast analysis complete")
    print("\nNote: This is a simplified structural model, not a fully calibrated forecast.")
    print("      See content/06-forecast.md Section 7 for limitations.")


if __name__ == "__main__":
    main()
