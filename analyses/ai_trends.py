"""
AI Trends Analysis
Visualizes key AI capability and efficiency trends
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set style
plt.style.use('seaborn-v0_8-whitegrid')


def generate_eci_data():
    """Generate Epoch Capabilities Index data"""
    # Simulated ECI trend based on reported growth patterns
    years = np.arange(2015, 2026)
    # Roughly exponential growth
    eci = 20 * np.exp(0.25 * (years - 2015)) + np.random.normal(0, 2, len(years))
    eci = np.clip(eci, 0, 100)
    return years, eci


def generate_benchmark_jumps():
    """Generate benchmark jump data"""
    benchmarks = ["MMMU", "GPQA", "SWE-bench"]
    improvements = [18.8, 48.9, 67.3]
    return benchmarks, improvements


def generate_efficiency_trend():
    """Generate inference cost decline (GPT-3.5 level quality)"""
    # Nov 2022 to Oct 2024: 280x reduction
    dates = pd.date_range("2022-11", "2024-10", freq='ME')
    n_months = len(dates)
    # Exponential decay: 280x over 23 months
    costs = 280 * np.exp(-np.log(280) * np.arange(n_months) / (n_months - 1))
    return dates, costs


def generate_compute_growth():
    """Generate AI compute capacity growth"""
    years = np.arange(2022, 2026)
    # 3.3x per year = doubling every 7 months
    base = 1
    compute = [base * (3.3 ** (y - 2022)) for y in years]
    return years, compute


def generate_saturation_data():
    """Generate benchmark saturation curves"""
    years = np.arange(2020, 2026, 0.5)
    # Different saturation patterns
    # Fast saturation (MMLU-like)
    fast_sat = 100 / (1 + np.exp(-2 * (years - 2022)))
    # Slow saturation
    slow_sat = 60 / (1 + np.exp(-1 * (years - 2023)))
    # Linear growth
    linear = np.clip(30 + 10 * (years - 2020), 0, 95)
    return years, fast_sat, slow_sat, linear


def plot_ai_trends():
    """Create comprehensive AI trends visualization"""
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Epoch Capabilities Index (ECI)
    ax1 = fig.add_subplot(gs[0, :2])
    years, eci = generate_eci_data()
    ax1.plot(years, eci, 'b-', linewidth=2.5, marker='o', markersize=6)
    ax1.fill_between(years, eci, alpha=0.3)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("ECI Score")
    ax1.set_title("Epoch Capabilities Index (ECI)\nComposite of 37 benchmarks", fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(True, alpha=0.3)
    # Add annotation
    ax1.annotate("Combines 37 benchmarks\nto avoid saturation bias", 
                xy=(2023, 60), fontsize=9, ha='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # 2. Benchmark Jumps (new difficult benchmarks)
    ax2 = fig.add_subplot(gs[0, 2])
    benchmarks, improvements = generate_benchmark_jumps()
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    bars = ax2.bar(benchmarks, improvements, color=colors, edgecolor='black')
    ax2.set_ylabel("Point Increase (1 year)")
    ax2.set_title("Benchmark Jumps\n(New Difficult Tests)", fontsize=11, fontweight='bold')
    ax2.set_ylim(0, 80)
    for bar, imp in zip(bars, improvements):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f"+{imp}", ha='center', fontsize=10, fontweight='bold')
    
    # 3. Inference Cost Decline (log scale)
    ax3 = fig.add_subplot(gs[1, 0])
    dates, costs = generate_efficiency_trend()
    ax3.semilogy(dates, costs, 'r-', linewidth=2)
    ax3.fill_between(dates, costs, alpha=0.3, color='red')
    ax3.set_ylabel("Relative Cost (log scale)")
    ax3.set_title("Inference Cost Decline\n(GPT-3.5 level quality)", fontsize=11, fontweight='bold')
    ax3.set_ylim(1, 300)
    ax3.grid(True, alpha=0.3, which='both')
    ax3.annotate(">280× reduction\nNov 2022 - Oct 2024", 
                xy=(dates[11], 50), fontsize=9, ha='center',
                bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    
    # 4. AI Compute Capacity (log scale)
    ax4 = fig.add_subplot(gs[1, 1])
    years, compute = generate_compute_growth()
    ax4.semilogy(years, compute, 'g-', linewidth=2.5, marker='s', markersize=8)
    ax4.set_xlabel("Year")
    ax4.set_ylabel("Relative Compute (log scale)")
    ax4.set_title("AI Compute Capacity Growth\n(~3.3× per year)", fontsize=11, fontweight='bold')
    ax4.grid(True, alpha=0.3, which='both')
    ax4.annotate("Doubling every\n~7 months", 
                xy=(2023.5, 10), fontsize=9, ha='center',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    # 5. Benchmark Saturation
    ax5 = fig.add_subplot(gs[1, 2])
    years_sat, fast_sat, slow_sat, linear = generate_saturation_data()
    ax5.plot(years_sat, fast_sat, 'b-', linewidth=2, label='Fast saturation (e.g., MMLU)')
    ax5.plot(years_sat, slow_sat, 'g-', linewidth=2, label='Slow saturation')
    ax5.plot(years_sat, linear, 'r--', linewidth=2, label='Linear (still growing)')
    ax5.axhline(y=90, color='gray', linestyle=':', alpha=0.5, label='Saturation zone')
    ax5.set_xlabel("Year")
    ax5.set_ylabel("Score (%)")
    ax5.set_title("Benchmark Saturation Patterns", fontsize=11, fontweight='bold')
    ax5.legend(loc='lower right', fontsize=8)
    ax5.set_ylim(0, 100)
    
    # 6. Efficiency improvements (bar chart)
    ax6 = fig.add_subplot(gs[2, 0])
    metrics = ["Cost per\ncompute", "Energy\nefficiency", "Chip perf/\n$"]
    improvements = [30, 40, 37]  # % per year
    colors = plt.cm.Greens(np.linspace(0.4, 0.8, len(metrics)))
    bars = ax6.bar(metrics, improvements, color=colors, edgecolor='black')
    ax6.set_ylabel("Annual improvement (%)")
    ax6.set_title("Efficiency Trends\n(Annual % improvement)", fontsize=11, fontweight='bold')
    ax6.set_ylim(0, 50)
    for bar, imp in zip(bars, improvements):
        ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f"~{imp}%", ha='center', fontsize=10, fontweight='bold')
    
    # 7. Model comparison: MiniMax vs Opus
    ax7 = fig.add_subplot(gs[2, 1])
    models = ["Claude\nOpus 4.6", "MiniMax\nM2.7"]
    prices = [10.0, 0.53]  # blended $/1M tokens
    quality = [53, 50]  # Intelligence Index
    
    x = np.arange(len(models))
    width = 0.35
    
    ax7_twin = ax7.twinx()
    bars1 = ax7.bar(x - width/2, prices, width, label='Price ($/1M tokens)', color='coral')
    bars2 = ax7_twin.bar(x + width/2, quality, width, label='Quality (Index)', color='steelblue')
    
    ax7.set_ylabel("Price ($/1M)", color='coral')
    ax7_twin.set_ylabel("Intelligence Index", color='steelblue')
    ax7.set_title("MiniMax vs Claude Opus\nPrice vs Quality", fontsize=11, fontweight='bold')
    ax7.set_xticks(x)
    ax7.set_xticklabels(models)
    ax7.set_yscale('log')
    
    # Add value labels
    for bar, price in zip(bars1, prices):
        ax7.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.2, 
                f"${price}", ha='center', fontsize=9, color='coral', fontweight='bold')
    for bar, q in zip(bars2, quality):
        ax7_twin.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f"{q}", ha='center', fontsize=9, color='steelblue', fontweight='bold')
    
    # Annotation
    ax7.annotate("~19× cheaper\nwith ~6% quality diff", 
                xy=(0.5, 2), fontsize=9, ha='center',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    # 8. Summary text
    ax8 = fig.add_subplot(gs[2, 2])
    ax8.axis('off')
    summary_text = """
    KEY TRENDS
    
    1. CAPABILITY
    • ECI shows consistent growth
    • New benchmarks jump fast
    • Old benchmarks saturate
    
    2. EFFICIENCY ⭐
    • 280× cost reduction in 2yr
    • ~30-40% annual improvement
    • Best exponential trend
    
    3. COMPUTE
    • 3.3× growth per year
    • Doubling every 7 months
    • Infrastructure scaling fast
    
    4. PRICE/PERFORMANCE
    • Frontier still advancing
    • Usable capacity cheaper
    • MiniMax = new efficiency
    
    CONCLUSION:
    "Usable agent capacity 
    getting cheaper faster than 
    raw capability improves"
    """
    ax8.text(0.05, 0.95, summary_text, transform=ax8.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    plt.suptitle("AI Trends: Capability, Efficiency & Cost", fontsize=16, fontweight='bold', y=0.98)
    plt.savefig("../assets/ai_trends.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Saved: assets/ai_trends.png")


def print_trends_summary():
    """Print summary of trends"""
    print("=" * 70)
    print("AI TRENDS SUMMARY")
    print("=" * 70)
    
    print("\n1. EPOCH CAPABILITIES INDEX (ECI)")
    print("-" * 50)
    years, eci = generate_eci_data()
    print(f"   2015: {eci[0]:.1f}")
    print(f"   2025: {eci[-1]:.1f}")
    print(f"   Growth: ~{((eci[-1]/eci[0]) ** (1/10) - 1) * 100:.1f}% per year")
    
    print("\n2. BENCHMARK JUMPS (new difficult tests)")
    print("-" * 50)
    benchmarks, improvements = generate_benchmark_jumps()
    for b, i in zip(benchmarks, improvements):
        print(f"   {b}: +{i} points in 1 year")
    
    print("\n3. EFFICIENCY TRENDS")
    print("-" * 50)
    print("   Inference cost reduction (GPT-3.5 level): >280×")
    print("   Annual improvement in cost/compute: ~30%")
    print("   Annual improvement in energy efficiency: ~40%")
    print("   AI chip performance per $: ~37%/year")
    
    print("\n4. COMPUTE GROWTH")
    print("-" * 50)
    years, compute = generate_compute_growth()
    print(f"   2022: baseline")
    print(f"   2025: {compute[-1]:.1f}×")
    print(f"   Growth rate: ~{((compute[-1]/compute[0]) ** (1/3)):.1f}× per year")
    print(f"   Doubling time: ~7 months")
    
    print("\n5. MINIMAX vs CLAUDE OPUS")
    print("-" * 50)
    print("   Intelligence Index:")
    print("     Claude Opus 4.6: 53")
    print("     MiniMax M2.7: 50")
    print("   Blended price per 1M tokens:")
    print("     Claude Opus 4.6: $10")
    print("     MiniMax M2.7: $0.53")
    print("   Price advantage: ~18.9× cheaper")
    print("   Quality difference: ~6%")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    print_trends_summary()
    plot_ai_trends()
    print("\n✓ AI trends analysis complete!")
