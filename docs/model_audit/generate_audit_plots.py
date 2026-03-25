#!/usr/bin/env python3
"""Generate audit visualizations for model evaluation.

These plots help diagnose whether the model is working as intended
and where conservatism comes from.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
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
ASSETS_DIR = ROOT / "assets"


def plot_growth_curve_comparison():
    """Compare how the same growth rate behaves under old vs new model."""
    
    # Simulate a single pillar with fixed growth
    y0 = 30
    growth_mu = 0.15
    years = np.arange(2026, 2041)
    n_years = len(years)
    
    # Old model: exponential on raw scale
    y_old = np.zeros(n_years)
    y_old[0] = y0
    for t in range(1, n_years):
        y_old[t] = y_old[t-1] * np.exp(growth_mu)
        if y_old[t] > 100:
            y_old[t] = 100
    
    # New model: additive on logit scale
    z = np.zeros(n_years)
    z[0] = to_logit(np.array([y0]))[0]
    for t in range(1, n_years):
        z[t] = z[t-1] + growth_mu
    y_new = from_logit(z)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Trajectories
    ax = axes[0]
    ax.plot(years, y_old, 'b-', linewidth=2, label='Old model (exponential, clipped)')
    ax.plot(years, y_new, 'r-', linewidth=2, label='New model (logit, sigmoid)')
    ax.axhline(y=100, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(y=60, color='green', linestyle='--', alpha=0.3, label='Floor (60)')
    ax.axhline(y=75, color='orange', linestyle='--', alpha=0.3, label='Threshold (75)')
    ax.set_xlabel('Year')
    ax.set_ylabel('Pillar Score')
    ax.set_title(f'Single Pillar Growth Comparison\n(Initial={y0}, growth_mu={growth_mu})')
    ax.legend()
    ax.set_ylim(0, 105)
    
    # Plot 2: Year-over-year growth rate
    ax = axes[1]
    growth_old = np.diff(y_old)
    growth_new = np.diff(y_new)
    ax.bar(years[1:] - 0.2, growth_old, width=0.4, label='Old model', alpha=0.7)
    ax.bar(years[1:] + 0.2, growth_new, width=0.4, label='New model', alpha=0.7)
    ax.set_xlabel('Year')
    ax.set_ylabel('Year-over-Year Increase')
    ax.set_title('Effective Growth Rate Over Time')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(ASSETS_DIR / 'audit_growth_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: audit_growth_comparison.png")


def plot_sensitivity_tornado():
    """Create tornado diagram showing parameter sensitivities."""
    
    # Data from audit
    parameters = [
        ('Floor 50→60', 0.266 - 0.082),
        ('Floor 60→70', 0.082 - 0.010),
        ('Threshold 75→85', 0.082 - 0.006),
        ('Model A→B (accel)', 0.487 - 0.082),
        ('Threshold 75→80', 0.082 - 0.058),
        ('Floor 55→60', 0.171 - 0.082),
        ('Floor 60→65', 0.082 - 0.031),
        ('Model A→C', 0.090 - 0.082),
        ('phi 0.7→0.99', 0.085 - 0.081),
    ]
    
    params, effects = zip(*parameters)
    colors = ['red' if e > 0 else 'blue' for e in effects]
    
    fig, ax = plt.subplots(figsize=(10, 7))
    y_pos = np.arange(len(params))
    ax.barh(y_pos, [e * 100 for e in effects], color=colors, alpha=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(params)
    ax.axvline(x=0, color='black', linewidth=0.5)
    ax.set_xlabel('Change in P(cross by 2040) [% points]')
    ax.set_title('Parameter Sensitivity Analysis\n(Base case: 8.2% crossing probability)')
    
    # Add value labels
    for i, (param, effect) in enumerate(zip(params, effects)):
        ax.text(effect * 100 + 0.5 if effect > 0 else effect * 100 - 0.5, 
                i, f'{effect*100:+.1f}pp', 
                va='center', ha='left' if effect > 0 else 'right', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(ASSETS_DIR / 'audit_sensitivity_tornado.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: audit_sensitivity_tornado.png")


def plot_logit_saturation_demo():
    """Demonstrate how logit transform affects growth at different levels."""
    
    y_values = np.linspace(1, 99, 100)
    z_values = to_logit(y_values)
    
    # Fixed additive growth on logit scale
    z_after = z_values + 0.2
    y_after = from_logit(z_after)
    effective_growth = y_after - y_values
    
    # Linear growth for comparison
    linear_10pct = y_values * 0.10
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Transform mapping
    ax = axes[0, 0]
    ax.plot(y_values, z_values, 'b-', linewidth=2)
    ax.set_xlabel('Raw Score y (0-100)')
    ax.set_ylabel('Logit z = log(y/(100-y))')
    ax.set_title('Logit Transform')
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
    ax.axvline(x=50, color='gray', linestyle='--', alpha=0.3)
    
    # Plot 2: Inverse transform
    ax = axes[0, 1]
    z_range = np.linspace(-4, 6, 100)
    y_range = from_logit(z_range)
    ax.plot(z_range, y_range, 'r-', linewidth=2)
    ax.set_xlabel('Logit z')
    ax.set_ylabel('Raw Score y')
    ax.set_title('Sigmoid (Inverse) Transform')
    ax.axhline(y=50, color='gray', linestyle='--', alpha=0.3)
    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.3)
    
    # Plot 3: Effective growth comparison
    ax = axes[1, 0]
    ax.plot(y_values, effective_growth, 'b-', linewidth=2, label='Logit model (+0.2 on z)')
    ax.plot(y_values, linear_10pct, 'r--', linewidth=2, label='Linear model (+10% of y)')
    ax.set_xlabel('Starting Score y')
    ax.set_ylabel('Effective Score Increase')
    ax.set_title('Effective Growth: Logit vs Linear')
    ax.legend()
    ax.axvline(x=50, color='gray', linestyle=':', alpha=0.3)
    ax.axvline(x=80, color='orange', linestyle=':', alpha=0.3, label='80')
    ax.axvline(x=90, color='red', linestyle=':', alpha=0.3, label='90')
    
    # Plot 4: Growth ratio (logit/linear)
    ax = axes[1, 1]
    ratio = effective_growth / (linear_10pct + 0.001)  # avoid div by zero
    ax.plot(y_values, ratio, 'g-', linewidth=2)
    ax.axhline(y=1, color='black', linestyle='--', alpha=0.3, label='Equal growth')
    ax.set_xlabel('Starting Score y')
    ax.set_ylabel('Growth Ratio (Logit/Linear)')
    ax.set_title('Logit Growth Relative to Linear')
    ax.set_ylim(0, 3)
    
    plt.tight_layout()
    plt.savefig(ASSETS_DIR / 'audit_logit_saturation.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: audit_logit_saturation.png")


def plot_floor_binding_analysis():
    """Analyze which floors are most often the binding constraint."""
    
    config = load_config()
    scenarios = create_scenarios(config)
    scenario = scenarios["Base case"]
    
    forecaster = AgentNetworkForecaster(
        scenario=scenario,
        n_simulations=5000,
        seed=SEED,
        model_type="C",
    )
    results = forecaster.run()
    
    # Check which floors fail in years 2035-2040
    floor_codes = ['M', 'R', 'N', 'G']
    floor_failures = {code: 0 for code in floor_codes}
    total_checks = 0
    
    for year_idx, year in enumerate(forecaster.years):
        if year < 2035:
            continue
        for sim_idx in range(forecaster.n_simulations):
            total_checks += 1
            for code in floor_codes:
                if results['pillar_values'][code][sim_idx, year_idx] < 60:
                    floor_failures[code] += 1
    
    # Calculate failure rates
    failure_rates = {code: count / total_checks for code, count in floor_failures.items()}
    
    fig, ax = plt.subplots(figsize=(10, 6))
    codes = list(failure_rates.keys())
    rates = [failure_rates[c] * 100 for c in codes]
    colors = ['#1d4ed8', '#15803d', '#dc2626', '#9333ea']
    
    bars = ax.bar(codes, rates, color=colors, alpha=0.7)
    ax.set_ylabel('Failure Rate (%)')
    ax.set_xlabel('Pillar')
    ax.set_title('Floor Binding Analysis: Which Pillars Fail Most Often?\n(Years 2035-2040, simulations that don\'t cross)')
    
    # Add value labels
    for bar, rate in zip(bars, rates):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{rate:.1f}%',
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(ASSETS_DIR / 'audit_floor_binding.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: audit_floor_binding.png")
    print(f"Floor failure rates: {failure_rates}")


def main():
    """Generate all audit plots."""
    print("Generating audit visualizations...")
    
    plot_growth_curve_comparison()
    plot_sensitivity_tornado()
    plot_logit_saturation_demo()
    plot_floor_binding_analysis()
    
    print("\nAll audit plots saved to assets/")


if __name__ == "__main__":
    main()
