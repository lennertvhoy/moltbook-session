#!/usr/bin/env python3
"""Generate audit data for model comparison and ablation study.

This script runs all model variants and collects detailed statistics
for the audit document. It does NOT modify the models - only collects data.
"""

import json
import sys
from pathlib import Path

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
)

SEED = 42


def run_ablation_study():
    """Run ablation study: isolate effect of each model change."""
    config = load_config()
    scenarios = create_scenarios(config)
    
    results = {}
    
    for scenario_name in ["Base case"]:
        scenario = scenarios[scenario_name]
        scenario_results = {}
        
        # Run all three models
        for model_type in ["A", "B", "C"]:
            forecaster = AgentNetworkForecaster(
                scenario=scenario,
                n_simulations=10000,
                seed=SEED,
                model_type=model_type,
            )
            sim_results = forecaster.run()
            stats = forecaster.calculate_statistics(sim_results)
            
            scenario_results[model_type] = {
                "p_by_2040": stats["p_by_2040"],
                "median_year": stats["median_year"],
                "never_crosses": stats["never_crosses"],
                "model_type": model_type,
            }
        
        results[scenario_name] = scenario_results
    
    return results


def analyze_parameter_sensitivity():
    """Analyze sensitivity to key parameters."""
    config = load_config()
    scenarios = create_scenarios(config)
    scenario = scenarios["Base case"]
    
    sensitivities = {}
    
    # Test different persistence values (phi)
    phi_values = [0.7, 0.8, 0.9, 0.95, 0.99]
    phi_results = []
    
    for phi in phi_values:
        forecaster = AgentNetworkForecaster(
            scenario=scenario,
            n_simulations=5000,
            seed=SEED,
            model_type="C",
        )
        # Override persistence
        forecaster.model.persistence = phi
        
        sim_results = forecaster.run()
        stats = forecaster.calculate_statistics(sim_results)
        phi_results.append({
            "phi": phi,
            "p_by_2040": stats["p_by_2040"],
            "median_year": stats["median_year"],
        })
    
    sensitivities["persistence_phi"] = phi_results
    
    # Test different thresholds
    threshold_values = [70, 75, 80, 85]
    threshold_results = []
    
    forecaster = AgentNetworkForecaster(
        scenario=scenario,
        n_simulations=5000,
        seed=SEED,
        model_type="C",
    )
    sim_results = forecaster.run()
    
    for threshold in threshold_values:
        stats = forecaster.calculate_statistics(sim_results, threshold=threshold)
        threshold_results.append({
            "threshold": threshold,
            "p_by_2040": stats["p_by_2040"],
            "median_year": stats["median_year"],
        })
    
    sensitivities["threshold"] = threshold_results
    
    # Test different floor values
    floor_values = [50, 55, 60, 65, 70]
    floor_results = []
    
    for floor in floor_values:
        floor_dict = {code: floor for code in scenario.floor_values}
        stats = forecaster.calculate_statistics(sim_results, floor_values=floor_dict)
        floor_results.append({
            "floor": floor,
            "p_by_2040": stats["p_by_2040"],
            "median_year": stats["median_year"],
        })
    
    sensitivities["floors"] = floor_results
    
    return sensitivities


def analyze_saturation_effect():
    """Analyze how logit/sigmoid transformation affects growth."""
    # Show mapping at different points
    y_values = np.array([20, 30, 40, 50, 60, 70, 80, 90, 95, 99])
    z_values = to_logit(y_values)
    
    # Growth rate comparison
    # On linear scale: 10% growth from different starting points
    linear_growth = y_values * 0.10
    
    # On logit scale: same additive growth
    z_growth = 0.2  # typical growth_mu
    y_after_logit = from_logit(z_values + z_growth)
    logit_effective_growth = y_after_logit - y_values
    
    return {
        "y_values": y_values.tolist(),
        "z_values": z_values.tolist(),
        "linear_growth_10%": linear_growth.tolist(),
        "logit_effective_growth": logit_effective_growth.tolist(),
    }


def main():
    """Generate all audit data."""
    print("Generating audit data...")
    
    audit_data = {
        "ablation_study": run_ablation_study(),
        "parameter_sensitivity": analyze_parameter_sensitivity(),
        "saturation_analysis": analyze_saturation_effect(),
    }
    
    output_path = Path(__file__).parent / "audit_data.json"
    with open(output_path, "w") as f:
        json.dump(audit_data, f, indent=2)
    
    print(f"Audit data saved to {output_path}")
    
    # Print summary
    print("\n=== ABLATION STUDY RESULTS ===")
    for scenario, models in audit_data["ablation_study"].items():
        print(f"\n{scenario}:")
        for model_type, stats in models.items():
            print(f"  Model {model_type}: P(cross by 2040) = {stats['p_by_2040']:.1%}, "
                  f"median = {stats['median_year']:.0f}, "
                  f"never crosses = {stats['never_crosses']:.1%}")
    
    print("\n=== PHI SENSITIVITY ===")
    for result in audit_data["parameter_sensitivity"]["persistence_phi"]:
        print(f"  phi={result['phi']}: P(cross by 2040) = {result['p_by_2040']:.1%}, "
              f"median = {result['median_year']:.0f}")


if __name__ == "__main__":
    main()
