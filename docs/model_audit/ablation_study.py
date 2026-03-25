#!/usr/bin/env python3
"""Comprehensive ablation study to identify which assumptions delay crossing.

This script tests:
1. Aggregation methods (geometric vs arithmetic vs CES vs softmin)
2. Floor architectures (with vs without, different levels)
3. Consecutive years rules (1, 2, 2-of-3, rolling)
4. Time horizons (2040, 2045, 2050)
5. Shock structures (iid, autocorrelated, regime-based)
"""

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

# Add parent dirs to path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analyses"))

from forecast_model import (
    AgentNetworkForecaster,
    create_scenarios,
    load_config,
    to_logit,
    from_logit,
    ModelC_LocalLinearTrend,
    GrowthModel,
)

SEED = 42
OUTPUT_DIR = Path(__file__).parent


# ============================================================================
# MODIFIED FORECASTER WITH CONFIGURABLE OPTIONS
# ============================================================================

class AblationForecaster(AgentNetworkForecaster):
    """Extended forecaster with configurable ablation options."""
    
    def __init__(
        self,
        scenario,
        n_simulations=10000,
        seed=SEED,
        model_type="C",
        # Ablation parameters
        aggregation="geometric",  # geometric, arithmetic, ces, softmin
        ces_rho=None,  # for CES aggregation
        use_floors=True,
        consecutive_rule="strict",  # strict, 2of3, rolling
        horizon_year=2040,
    ):
        super().__init__(scenario, n_simulations, seed, model_type)
        self.aggregation = aggregation
        self.ces_rho = ces_rho or -1.0  # rho < 1, lower = more penalty on lows
        self.use_floors = use_floors
        self.consecutive_rule = consecutive_rule
        self.horizon_year = horizon_year
        self.years = np.arange(2026, horizon_year + 1)
    
    def _calculate_readiness_index(self, pillar_values: dict[str, np.ndarray]) -> np.ndarray:
        """Calculate index with configurable aggregation."""
        n_sims = self.n_simulations
        n_years = len(self.years)
        
        if self.aggregation == "geometric":
            # Original: geometric mean
            index = np.ones((n_sims, n_years))
            for pillar in self.scenario.pillars:
                index *= (pillar_values[pillar.code] / 100.0) ** pillar.weight
            return index * 100.0
        
        elif self.aggregation == "arithmetic":
            # Simple weighted average
            index = np.zeros((n_sims, n_years))
            for pillar in self.scenario.pillars:
                index += pillar_values[pillar.code] * pillar.weight
            return index
        
        elif self.aggregation == "ces":
            # CES aggregator: (sum w_i * x_i^rho)^(1/rho)
            rho = self.ces_rho
            index = np.zeros((n_sims, n_years))
            for pillar in self.scenario.pillars:
                index += pillar.weight * (pillar_values[pillar.code] ** rho)
            return (index ** (1/rho))
        
        elif self.aggregation == "softmin":
            # Soft minimum: emphasizes lowest pillars
            # approx_min = -log(sum w_i * exp(-alpha * x_i)) / alpha
            alpha = 0.1  # higher = harder min
            index = np.zeros((n_sims, n_years))
            for pillar in self.scenario.pillars:
                index += pillar.weight * np.exp(-alpha * pillar_values[pillar.code])
            return -np.log(index) / alpha
        
        else:
            raise ValueError(f"Unknown aggregation: {self.aggregation}")
    
    def _check_threshold_crossing(
        self,
        index: np.ndarray,
        pillar_values: dict[str, np.ndarray],
        threshold: float | None = None,
        floor_values: dict[str, float] | None = None,
    ) -> np.ndarray:
        """Check crossing with configurable rules."""
        active_threshold = self.scenario.threshold if threshold is None else threshold
        
        if self.use_floors:
            active_floors = self.scenario.floor_values if floor_values is None else floor_values
        else:
            active_floors = {}  # No floors
        
        crossing_years = np.full(self.n_simulations, np.nan)
        
        for sim_idx in range(self.n_simulations):
            if self.consecutive_rule == "strict":
                # Original: 2 consecutive years
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
            
            elif self.consecutive_rule == "1year":
                # Just 1 year needed
                for year_idx, year in enumerate(self.years):
                    floors_met = all(
                        pillar_values[code][sim_idx, year_idx] >= minimum
                        for code, minimum in active_floors.items()
                    )
                    if index[sim_idx, year_idx] >= active_threshold and floors_met:
                        crossing_years[sim_idx] = year
                        break
            
            elif self.consecutive_rule == "2of3":
                # 2 out of 3 consecutive years
                satisfied = []
                for year_idx, year in enumerate(self.years):
                    floors_met = all(
                        pillar_values[code][sim_idx, year_idx] >= minimum
                        for code, minimum in active_floors.items()
                    )
                    satisfied.append(index[sim_idx, year_idx] >= active_threshold and floors_met)
                
                for i in range(len(self.years) - 2):
                    if sum(satisfied[i:i+3]) >= 2:
                        crossing_years[sim_idx] = self.years[i+2]  # End of window
                        break
            
            elif self.consecutive_rule == "rolling":
                # 2-year rolling average satisfies conditions
                satisfied = []
                for year_idx, year in enumerate(self.years):
                    floors_met = all(
                        pillar_values[code][sim_idx, year_idx] >= minimum
                        for code, minimum in active_floors.items()
                    )
                    satisfied.append(index[sim_idx, year_idx] >= active_threshold and floors_met)
                
                for i in range(len(self.years) - 1):
                    if sum(satisfied[i:i+2]) == 2:
                        crossing_years[sim_idx] = self.years[i+1]
                        break
        
        return crossing_years


# ============================================================================
# ABLATION TESTS
# ============================================================================

def ablation_aggregation():
    """Test different aggregation methods."""
    print("\n" + "="*70)
    print("ABLATION 1: AGGREGATION METHODS")
    print("="*70)
    
    config = load_config()
    scenarios = create_scenarios(config)
    scenario = scenarios["Base case"]
    
    results = {}
    
    for agg in ["geometric", "arithmetic", "ces", "softmin"]:
        forecaster = AblationForecaster(
            scenario=scenario,
            n_simulations=10000,
            seed=SEED,
            aggregation=agg,
            use_floors=True,
            consecutive_rule="strict",
            horizon_year=2040,
        )
        sim_results = forecaster.run()
        
        # Calculate crossing
        crossing = forecaster._check_threshold_crossing(
            sim_results["index"],
            sim_results["pillar_values"],
        )
        valid = crossing[~np.isnan(crossing)]
        
        p_cross = np.mean(~np.isnan(crossing))
        median_year = np.median(valid) if len(valid) > 0 else np.nan
        
        results[agg] = {
            "p_cross": p_cross,
            "median_year": median_year,
        }
        
        print(f"\n{agg:12s}: P(cross) = {p_cross:.1%}, median = {median_year:.0f}")
    
    return results


def ablation_floors():
    """Test with and without floors, at different levels."""
    print("\n" + "="*70)
    print("ABLATION 2: FLOOR ARCHITECTURES")
    print("="*70)
    
    config = load_config()
    scenarios = create_scenarios(config)
    scenario = scenarios["Base case"]
    
    results = {}
    
    tests = [
        ("no_floors", False, {}),
        ("floors_50", True, {k: 50 for k in scenario.floor_values}),
        ("floors_55", True, {k: 55 for k in scenario.floor_values}),
        ("floors_60", True, {k: 60 for k in scenario.floor_values}),
        ("floors_65", True, {k: 65 for k in scenario.floor_values}),
        ("index_only", False, {}),  # Will modify threshold check
    ]
    
    for name, use_floors, floor_override in tests:
        forecaster = AblationForecaster(
            scenario=scenario,
            n_simulations=10000,
            seed=SEED,
            aggregation="geometric",
            use_floors=use_floors,
            consecutive_rule="strict",
            horizon_year=2040,
        )
        sim_results = forecaster.run()
        
        crossing = forecaster._check_threshold_crossing(
            sim_results["index"],
            sim_results["pillar_values"],
            floor_values=floor_override if floor_override else None,
        )
        valid = crossing[~np.isnan(crossing)]
        
        p_cross = np.mean(~np.isnan(crossing))
        median_year = np.median(valid) if len(valid) > 0 else np.nan
        
        results[name] = {
            "p_cross": p_cross,
            "median_year": median_year,
        }
        
        print(f"\n{name:15s}: P(cross) = {p_cross:.1%}, median = {median_year:.0f}")
    
    return results


def ablation_consecutive():
    """Test different consecutive year rules."""
    print("\n" + "="*70)
    print("ABLATION 3: CONSECUTIVE YEARS RULES")
    print("="*70)
    
    config = load_config()
    scenarios = create_scenarios(config)
    scenario = scenarios["Base case"]
    
    results = {}
    
    for rule in ["1year", "strict", "2of3", "rolling"]:
        forecaster = AblationForecaster(
            scenario=scenario,
            n_simulations=10000,
            seed=SEED,
            aggregation="geometric",
            use_floors=True,
            consecutive_rule=rule,
            horizon_year=2040,
        )
        sim_results = forecaster.run()
        
        crossing = forecaster._check_threshold_crossing(
            sim_results["index"],
            sim_results["pillar_values"],
        )
        valid = crossing[~np.isnan(crossing)]
        
        p_cross = np.mean(~np.isnan(crossing))
        median_year = np.median(valid) if len(valid) > 0 else np.nan
        
        results[rule] = {
            "p_cross": p_cross,
            "median_year": median_year,
        }
        
        print(f"\n{rule:12s}: P(cross) = {p_cross:.1%}, median = {median_year:.0f}")
    
    return results


def ablation_horizon():
    """Test different time horizons."""
    print("\n" + "="*70)
    print("ABLATION 4: TIME HORIZON")
    print("="*70)
    
    config = load_config()
    scenarios = create_scenarios(config)
    scenario = scenarios["Base case"]
    
    results = {}
    
    for horizon in [2040, 2045, 2050, 2060]:
        forecaster = AblationForecaster(
            scenario=scenario,
            n_simulations=10000,
            seed=SEED,
            aggregation="geometric",
            use_floors=True,
            consecutive_rule="strict",
            horizon_year=horizon,
        )
        sim_results = forecaster.run()
        
        crossing = forecaster._check_threshold_crossing(
            sim_results["index"],
            sim_results["pillar_values"],
        )
        valid = crossing[~np.isnan(crossing)]
        
        p_cross = np.mean(~np.isnan(crossing))
        median_year = np.median(valid) if len(valid) > 0 else np.nan
        p_by_2040 = np.mean(crossing <= 2040) if len(valid) > 0 else 0
        
        results[horizon] = {
            "p_cross": p_cross,
            "median_year": median_year,
            "p_by_2040": p_by_2040,
        }
        
        print(f"\nhorizon {horizon}: P(cross by {horizon}) = {p_cross:.1%}, "
              f"median = {median_year:.0f}, P(by 2040) = {p_by_2040:.1%}")
    
    return results


def ablation_deterministic():
    """Calculate deterministic path (no noise) to establish baseline."""
    print("\n" + "="*70)
    print("ABLATION 5: DETERMINISTIC BASELINE")
    print("="*70)
    
    config = load_config()
    scenarios = create_scenarios(config)
    scenario = scenarios["Base case"]
    
    # Simulate deterministically (no shocks, median growth)
    years = np.arange(2026, 2041)
    n_years = len(years)
    
    print("\nDeterministic pillar trajectories (no shocks, median growth):")
    print(f"{'Year':<6}", end="")
    for p in scenario.pillars:
        print(f"{p.code:>8}", end="")
    print(f"{'Index':>8} {'Floors':>8}")
    print("-" * 80)
    
    pillar_values = {}
    for pillar in scenario.pillars:
        y = np.zeros(n_years)
        y[0] = pillar.initial_2026
        z = to_logit(np.array([y[0]]))[0]
        
        for t in range(1, n_years):
            z = z + pillar.growth_mu  # No noise, just median growth
            y[t] = from_logit(np.array([z]))[0]
        
        pillar_values[pillar.code] = y
    
    # Calculate index
    index = np.ones(n_years) * 100.0
    for pillar in scenario.pillars:
        index *= (pillar_values[pillar.code] / 100.0) ** pillar.weight
    index *= 100.0
    
    crossing_year = None
    for t, year in enumerate(years):
        floors_met = all(pillar_values[code][t] >= 60 for code in scenario.floor_values)
        status = "OK" if floors_met and index[t] >= 75 else ""
        if floors_met and index[t] >= 75 and crossing_year is None:
            crossing_year = year
        
        print(f"{year:<6}", end="")
        for p in scenario.pillars:
            print(f"{pillar_values[p.code][t]:>8.1f}", end="")
        print(f"{index[t]:>8.1f} {'FLOORS' if not floors_met else ('X' if crossing_year == year else ''):>8}")
    
    print(f"\nDeterministic crossing year: {crossing_year}")
    print(f"Deterministic years to cross from 2026: {crossing_year - 2026 if crossing_year else 'N/A'}")
    
    return {"crossing_year": crossing_year}


def main():
    """Run all ablation studies."""
    print("="*70)
    print("COMPREHENSIVE ABLATION STUDY")
    print("="*70)
    
    all_results = {
        "aggregation": ablation_aggregation(),
        "floors": ablation_floors(),
        "consecutive": ablation_consecutive(),
        "horizon": ablation_horizon(),
        "deterministic": ablation_deterministic(),
    }
    
    # Save results
    output_file = OUTPUT_DIR / "ablation_results.json"
    def convert_to_serializable(obj):
        if isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_to_serializable(x) for x in obj]
        return obj
    
    serializable_results = convert_to_serializable(all_results)
    with open(output_file, "w") as f:
        json.dump(serializable_results, f, indent=2)
    
    print(f"\n\nResults saved to {output_file}")
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY: WHAT DELAYS CROSSING MOST?")
    print("="*70)
    
    baseline_p = all_results["aggregation"]["geometric"]["p_cross"]
    baseline_med = all_results["aggregation"]["geometric"]["median_year"]
    
    print(f"\nBaseline (geometric + floors + 2-year rule, horizon 2040):")
    print(f"  P(cross) = {baseline_p:.1%}, median year = {baseline_med:.0f}")
    
    print("\nKey findings:")
    print(f"  - No floors:        P(cross) = {all_results['floors']['no_floors']['p_cross']:.1%} "
          f"(+{all_results['floors']['no_floors']['p_cross'] - baseline_p:.1%})")
    print(f"  - 1-year rule:      P(cross) = {all_results['consecutive']['1year']['p_cross']:.1%} "
          f"(+{all_results['consecutive']['1year']['p_cross'] - baseline_p:.1%})")
    print(f"  - Arithmetic mean:  P(cross) = {all_results['aggregation']['arithmetic']['p_cross']:.1%} "
          f"(+{all_results['aggregation']['arithmetic']['p_cross'] - baseline_p:.1%})")
    print(f"  - Horizon 2050:     P(cross) = {all_results['horizon'][2050]['p_cross']:.1%} "
          f"(+{all_results['horizon'][2050]['p_cross'] - baseline_p:.1%})")
    
    det_cross = all_results["deterministic"]["crossing_year"]
    if det_cross:
        print(f"\n  - Deterministic:    crossing at {det_cross:.0f} "
              f"({baseline_med - det_cross:.0f} years earlier than stochastic median)")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
