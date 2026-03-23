"""
Monte Carlo Forecasting Model for AI Agent Networks
Predicts when "Level-3 reality" (global social reality) is reached
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dataclasses import dataclass
from typing import Tuple, Dict, List

# Set random seed for reproducibility
np.random.seed(42)


@dataclass
class PillarConfig:
    """Configuration for one pillar of the readiness index"""
    name: str
    code: str
    initial_2026: float
    growth_mu: float  # Expected annual log growth
    volatility: float  # Annual volatility (sigma)
    neg_shock_prob: float  # Probability of negative shock
    neg_shock_size: float  # Size of negative shock (log scale)
    weight: float  # Weight in geometric mean


@dataclass
class Scenario:
    """A complete scenario configuration"""
    name: str
    pillars: List[PillarConfig]
    threshold: float = 75.0
    floor_values: Dict[str, float] = None
    min_consecutive_years: int = 2


class AgentNetworkForecaster:
    """Monte Carlo forecaster for AI agent network readiness"""
    
    def __init__(self, scenario: Scenario, n_simulations: int = 10000):
        self.scenario = scenario
        self.n_simulations = n_simulations
        self.years = np.arange(2026, 2041)  # 2026 to 2040
        
    def _simulate_pillar(self, pillar: PillarConfig) -> np.ndarray:
        """Simulate one pillar over time"""
        n_years = len(self.years)
        values = np.zeros((self.n_simulations, n_years))
        values[:, 0] = pillar.initial_2026
        
        for t in range(1, n_years):
            # Log-normal growth
            log_growth = np.random.normal(pillar.growth_mu, pillar.volatility, self.n_simulations)
            
            # Add occasional shocks
            shocks = np.random.random(self.n_simulations) < pillar.neg_shock_prob
            log_growth[shocks] += pillar.neg_shock_size
            
            # Update values
            values[:, t] = values[:, t-1] * np.exp(log_growth)
            
            # Cap at 100
            values[:, t] = np.clip(values[:, t], 0, 100)
            
        return values
    
    def _calculate_readiness_index(self, pillar_values: Dict[str, np.ndarray]) -> np.ndarray:
        """Calculate weighted geometric mean readiness index"""
        n_years = len(self.years)
        index = np.ones((self.n_simulations, n_years)) * 100.0
        
        for pillar in self.scenario.pillars:
            code = pillar.code
            weight = pillar.weight
            values = pillar_values[code]
            index *= (values / 100.0) ** weight
            
        index *= 100.0  # Scale back to 0-100
        return index
    
    def _check_threshold_crossing(self, index: np.ndarray, pillar_values: Dict[str, np.ndarray]) -> np.ndarray:
        """Check for each simulation when threshold is crossed and sustained"""
        crossing_years = np.full(self.n_simulations, np.nan)
        
        floor_codes = list(self.scenario.floor_values.keys()) if self.scenario.floor_values else []
        
        for i in range(self.n_simulations):
            consecutive = 0
            for t, year in enumerate(self.years):
                # Check main threshold
                above_threshold = index[i, t] >= self.scenario.threshold
                
                # Check floor constraints
                floors_met = all(
                    pillar_values[code][i, t] >= self.scenario.floor_values.get(code, 0)
                    for code in floor_codes
                )
                
                if above_threshold and floors_met:
                    consecutive += 1
                    if consecutive >= self.scenario.min_consecutive_years:
                        crossing_years[i] = year
                        break
                else:
                    consecutive = 0
                    
        return crossing_years
    
    def run_simulation(self) -> Dict:
        """Run full Monte Carlo simulation"""
        # Simulate all pillars
        pillar_values = {}
        for pillar in self.scenario.pillars:
            pillar_values[pillar.code] = self._simulate_pillar(pillar)
        
        # Calculate readiness index
        index = self._calculate_readiness_index(pillar_values)
        
        # Check threshold crossing
        crossing_years = self._check_threshold_crossing(index, pillar_values)
        
        return {
            'pillar_values': pillar_values,
            'index': index,
            'crossing_years': crossing_years
        }
    
    def calculate_statistics(self, results: Dict) -> Dict:
        """Calculate summary statistics from simulation results"""
        crossing_years = results['crossing_years']
        valid_crossings = crossing_years[~np.isnan(crossing_years)]
        
        stats = {
            'p_by_2030': np.mean(crossing_years <= 2030) if len(valid_crossings) > 0 else 0,
            'p_by_2035': np.mean(crossing_years <= 2035) if len(valid_crossings) > 0 else 0,
            'p_by_2040': np.mean(crossing_years <= 2040) if len(valid_crossings) > 0 else 0,
            'median_year': np.median(valid_crossings) if len(valid_crossings) > 0 else np.nan,
            'p5_year': np.percentile(valid_crossings, 5) if len(valid_crossings) > 0 else np.nan,
            'p95_year': np.percentile(valid_crossings, 95) if len(valid_crossings) > 0 else np.nan,
            'never_crosses': np.mean(np.isnan(crossing_years)),
            'n_simulations': self.n_simulations,
        }
        
        # Calculate year-by-year probabilities
        year_probs = {}
        for year in self.years:
            year_probs[year] = np.mean(crossing_years <= year) if len(valid_crossings) > 0 else 0
            
        stats['year_probs'] = year_probs
        
        return stats


def create_scenarios() -> Dict[str, Scenario]:
    """Create the three scenarios: Conservative, Base, Accelerated"""
    
    # Conservative scenario
    conservative_pillars = [
        PillarConfig("Capability", "C", 55, 0.12, 0.10, 0.08, -0.12, 0.20),
        PillarConfig("Efficiency", "E", 45, 0.20, 0.12, 0.06, -0.08, 0.20),
        PillarConfig("Memory", "M", 30, 0.08, 0.15, 0.12, -0.15, 0.15),
        PillarConfig("Reliability", "R", 28, 0.10, 0.15, 0.15, -0.18, 0.15),
        PillarConfig("Network", "N", 20, 0.08, 0.18, 0.18, -0.20, 0.12),
        PillarConfig("Governance", "G", 25, 0.04, 0.12, 0.20, -0.25, 0.10),
        PillarConfig("Demand", "D", 50, 0.08, 0.10, 0.08, -0.08, 0.08),
    ]
    
    # Base case scenario
    base_pillars = [
        PillarConfig("Capability", "C", 55, 0.18, 0.08, 0.05, -0.08, 0.20),
        PillarConfig("Efficiency", "E", 45, 0.28, 0.10, 0.04, -0.06, 0.20),
        PillarConfig("Memory", "M", 30, 0.14, 0.12, 0.08, -0.10, 0.15),
        PillarConfig("Reliability", "R", 28, 0.16, 0.12, 0.10, -0.12, 0.15),
        PillarConfig("Network", "N", 20, 0.15, 0.15, 0.12, -0.15, 0.12),
        PillarConfig("Governance", "G", 25, 0.08, 0.10, 0.15, -0.18, 0.10),
        PillarConfig("Demand", "D", 50, 0.12, 0.07, 0.05, -0.06, 0.08),
    ]
    
    # Accelerated scenario
    accelerated_pillars = [
        PillarConfig("Capability", "C", 55, 0.22, 0.06, 0.03, -0.05, 0.20),
        PillarConfig("Efficiency", "E", 45, 0.35, 0.08, 0.02, -0.04, 0.20),
        PillarConfig("Memory", "M", 30, 0.20, 0.10, 0.05, -0.06, 0.15),
        PillarConfig("Reliability", "R", 28, 0.22, 0.10, 0.06, -0.08, 0.15),
        PillarConfig("Network", "N", 20, 0.22, 0.12, 0.08, -0.10, 0.12),
        PillarConfig("Governance", "G", 25, 0.12, 0.08, 0.10, -0.12, 0.10),
        PillarConfig("Demand", "D", 50, 0.18, 0.06, 0.03, -0.04, 0.08),
    ]
    
    floor_values = {"M": 60, "R": 60, "N": 60, "G": 60}
    
    scenarios = {
        "Conservative": Scenario("Conservative", conservative_pillars, 75.0, floor_values, 2),
        "Base case": Scenario("Base case", base_pillars, 75.0, floor_values, 2),
        "Accelerated": Scenario("Accelerated", accelerated_pillars, 75.0, floor_values, 2),
    }
    
    return scenarios


def run_all_scenarios(n_simulations: int = 10000) -> Dict[str, Dict]:
    """Run all scenarios and collect results"""
    scenarios = create_scenarios()
    all_results = {}
    
    for name, scenario in scenarios.items():
        print(f"\nRunning {name} scenario...")
        forecaster = AgentNetworkForecaster(scenario, n_simulations)
        results = forecaster.run_simulation()
        stats = forecaster.calculate_statistics(results)
        all_results[name] = {
            'scenario': scenario,
            'forecaster': forecaster,
            'results': results,
            'stats': stats
        }
        
    return all_results


def plot_forecast_results(all_results: Dict[str, Dict]):
    """Create visualization of forecast results"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Readiness index trajectories
    ax1 = axes[0, 0]
    colors = {'Conservative': 'blue', 'Base case': 'green', 'Accelerated': 'red'}
    
    for scenario_name, data in all_results.items():
        index = data['results']['index']
        years = data['forecaster'].years
        
        # Plot median and confidence bands
        median = np.median(index, axis=0)
        p5 = np.percentile(index, 5, axis=0)
        p95 = np.percentile(index, 95, axis=0)
        p25 = np.percentile(index, 25, axis=0)
        p75 = np.percentile(index, 75, axis=0)
        
        color = colors[scenario_name]
        ax1.plot(years, median, color=color, linewidth=2, label=f"{scenario_name} (median)")
        ax1.fill_between(years, p25, p75, color=color, alpha=0.2)
        ax1.fill_between(years, p5, p95, color=color, alpha=0.1)
    
    ax1.axhline(y=75, color='black', linestyle='--', label='Threshold (75)')
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Readiness Index")
    ax1.set_title("Readiness Index Trajectories by Scenario")
    ax1.legend(loc='lower right')
    ax1.set_ylim(0, 100)
    ax1.grid(True, alpha=0.3)
    
    # 2. Cumulative probability of reaching threshold
    ax2 = axes[0, 1]
    
    for scenario_name, data in all_results.items():
        year_probs = data['stats']['year_probs']
        years = list(year_probs.keys())
        probs = list(year_probs.values())
        
        ax2.plot(years, probs, marker='o', linewidth=2, label=scenario_name, color=colors[scenario_name])
    
    ax2.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5)
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Cumulative Probability")
    ax2.set_title("P(Level-3 reached by year)")
    ax2.legend()
    ax2.set_ylim(0, 1)
    ax2.grid(True, alpha=0.3)
    
    # 3. Distribution of crossing years
    ax3 = axes[1, 0]
    
    crossing_data = []
    labels = []
    for scenario_name, data in all_results.items():
        crossing_years = data['results']['crossing_years']
        valid = crossing_years[~np.isnan(crossing_years)]
        if len(valid) > 0:
            crossing_data.append(valid)
            labels.append(f"{scenario_name}\n(n={len(valid)})")
    
    bp = ax3.boxplot(crossing_data, labels=labels, patch_artist=True)
    for patch, color in zip(bp['boxes'], colors.values()):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
    
    ax3.set_ylabel("Year")
    ax3.set_title("Distribution of Threshold Crossing Years")
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Summary statistics table
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    table_data = []
    for scenario_name in ['Conservative', 'Base case', 'Accelerated']:
        stats = all_results[scenario_name]['stats']
        table_data.append([
            scenario_name,
            f"{stats['p_by_2030']:.1%}",
            f"{stats['p_by_2035']:.1%}",
            f"{stats['p_by_2040']:.1%}",
            f"{stats['median_year']:.0f}" if not np.isnan(stats['median_year']) else "N/A",
            f"{stats['p5_year']:.0f}-{stats['p95_year']:.0f}" if not np.isnan(stats['p5_year']) else "N/A"
        ])
    
    table = ax4.table(
        cellText=table_data,
        colLabels=['Scenario', 'P(≤2030)', 'P(≤2035)', 'P(≤2040)', 'Median', '90% CI'],
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    
    # Color code rows
    for i, color in enumerate(['blue', 'green', 'red']):
        for j in range(6):
            table[(i+1, j)].set_facecolor(colors[list(colors.keys())[i]])
            table[(i+1, j)].set_alpha(0.2)
    
    ax4.set_title("Summary Statistics by Scenario", y=0.8, fontsize=12)
    
    plt.tight_layout()
    plt.savefig("../assets/forecast_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Saved: assets/forecast_distribution.png")


def print_forecast_report(all_results: Dict[str, Dict]):
    """Print comprehensive forecast report"""
    print("=" * 70)
    print("AI AGENT NETWORK FORECAST - MONTE CARLO SIMULATION")
    print("=" * 70)
    
    print("\nMODEL PARAMETERS")
    print("-" * 50)
    print(f"Simulations per scenario: {list(all_results.values())[0]['stats']['n_simulations']:,}")
    print(f"Threshold: 75 (Readiness Index)")
    print(f"Floor constraints: M≥60, R≥60, N≥60, G≥60")
    print(f"Minimum consecutive years: 2")
    
    print("\n7-PILLAR READINESS INDEX")
    print("-" * 50)
    print("C = Capability")
    print("E = Efficiency")
    print("M = Memory")
    print("R = Reliability")
    print("N = Network coordination")
    print("G = Governance")
    print("D = Demand")
    
    print("\nSCENARIO PARAMETERS (2026 baseline)")
    print("-" * 50)
    for scenario_name in ['Conservative', 'Base case', 'Accelerated']:
        scenario = all_results[scenario_name]['scenario']
        print(f"\n{scenario_name}:")
        for pillar in scenario.pillars:
            print(f"  {pillar.code} ({pillar.name:12}): {pillar.initial_2026:.0f} → μ={pillar.growth_mu:.2f}, σ={pillar.volatility:.2f}")
    
    print("\nRESULTS BY SCENARIO")
    print("-" * 50)
    for scenario_name in ['Conservative', 'Base case', 'Accelerated']:
        stats = all_results[scenario_name]['stats']
        print(f"\n{scenario_name}:")
        print(f"  P(Level-3 by 2030): {stats['p_by_2030']:.1%}")
        print(f"  P(Level-3 by 2035): {stats['p_by_2035']:.1%}")
        print(f"  P(Level-3 by 2040): {stats['p_by_2040']:.1%}")
        print(f"  Median arrival:     {stats['median_year']:.0f}" if not np.isnan(stats['median_year']) else "  Median arrival:     Never")
        print(f"  90% Credible Interval: {stats['p5_year']:.0f}-{stats['p95_year']:.0f}" if not np.isnan(stats['p5_year']) else "  90% CI: N/A")
        print(f"  Never reaches:      {stats['never_crosses']:.1%}")
    
    print("\nKEY INSIGHTS")
    print("-" * 50)
    base_stats = all_results['Base case']['stats']
    print(f"• Most likely scenario (base case): {base_stats['median_year']:.0f} median arrival")
    print(f"• Wide uncertainty: {base_stats['p5_year']:.0f}-{base_stats['p95_year']:.0f} 90% credible interval")
    print(f"• Technical feasibility (lower threshold) likely much earlier")
    print(f"• Governance (G) and Memory (M) are often the binding constraints")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Run all scenarios
    print("Running Monte Carlo forecast model...")
    print("This may take a moment...")
    
    all_results = run_all_scenarios(n_simulations=10000)
    
    # Generate outputs
    print_forecast_report(all_results)
    plot_forecast_results(all_results)
    
    print("\n✓ Forecast model analysis complete!")
