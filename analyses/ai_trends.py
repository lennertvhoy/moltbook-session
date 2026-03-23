"""Sourced AI trend summary visuals for the Moltbook session.

The prior version of this script generated synthetic curves that looked empirical.
This replacement only charts explicit sourced metrics or clearly derived
normalizations based on sourced endpoints.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"
DATA_PATH = ROOT / "data" / "ai_trends_metrics.json"


def load_metrics() -> dict[str, Any]:
    """Load sourced AI trend metrics from disk.

    Returns:
        Parsed JSON payload containing trend inputs and source metadata.
    """
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def build_normalized_cost_curve(metrics: dict[str, Any]) -> tuple[pd.DatetimeIndex, np.ndarray]:
    """Create a normalized cost curve from sourced start and end points.

    Args:
        metrics: Parsed AI trends metrics JSON.

    Returns:
        A date index and a normalized cost series where the end point equals 1.
    """
    decline = metrics["inference_cost_decline"]
    dates = pd.date_range(decline["start_month"], decline["end_month"], freq="ME")
    steps = len(dates) - 1
    start = float(decline["reduction_factor"])
    end = 1.0
    values = np.geomspace(start, end, num=steps + 1)
    return dates, values


def build_growth_dataframe(metrics: dict[str, Any]) -> pd.DataFrame:
    """Build a small sourced trend table for the chart.

    Args:
        metrics: Parsed AI trends metrics JSON.

    Returns:
        DataFrame containing annual growth factors and doubling times.
    """
    epoch = metrics["epoch_trend_snapshot"]
    rows = [
        {
            "Metric": "Global compute stock",
            "Annual factor": epoch["compute_stock_growth_per_year"],
            "Doubling": f"{epoch['compute_stock_doubling_months']:.1f} mo",
        },
        {
            "Metric": "Training compute",
            "Annual factor": epoch["training_compute_growth_per_year"],
            "Doubling": f"{epoch['training_compute_doubling_months']:.1f} mo",
        },
        {
            "Metric": "Pretraining efficiency",
            "Annual factor": epoch["pretraining_efficiency_improvement_per_year"],
            "Doubling": f"{epoch['pretraining_efficiency_doubling_months']:.1f} mo",
        },
        {
            "Metric": "Chip perf per $",
            "Annual factor": epoch["chip_perf_per_dollar_growth_per_year"],
            "Doubling": f"{epoch['chip_perf_per_dollar_doubling_years']:.1f} yr",
        },
    ]
    return pd.DataFrame(rows)


def build_model_comparison_dataframe(metrics: dict[str, Any]) -> pd.DataFrame:
    """Build the official vendor comparison table used for audit notes.

    Args:
        metrics: Parsed AI trends metrics JSON.

    Returns:
        DataFrame with model comparison inputs.
    """
    rows = []
    for model in metrics["model_price_quality_snapshot"]["models"]:
        blended = (model["input_price_per_million"] + model["output_price_per_million"]) / 2
        row = {
            "Model": model["name"],
            "Configuration": model["configuration"],
            "Blended price": blended,
            "Terminal Bench": model["terminal_bench"],
        }
        if "swe_pro" in model:
            row["SWE-Pro"] = model["swe_pro"]
            row["VIBE-Pro"] = model["vibe_pro"]
            row["GDPval-AA Elo"] = model["gdpval_aa_elo"]
            row["Skill adherence"] = model["skill_adherence_pct"]
        if "osworld" in model:
            row["OSWorld"] = model["osworld"]
            row["Context note"] = model["context_window_note"]
        rows.append(row)
    return pd.DataFrame(rows)


def plot_ai_trends(metrics: dict[str, Any]) -> Path:
    """Create the sourced AI trends figure.

    Args:
        metrics: Parsed AI trends metrics JSON.

    Returns:
        Path to the saved PNG file.
    """
    jump_df = pd.DataFrame(metrics["benchmark_jumps"])
    dates, normalized_costs = build_normalized_cost_curve(metrics)
    growth_df = build_growth_dataframe(metrics)
    fig = plt.figure(figsize=(15.5, 6.8))
    grid = fig.add_gridspec(1, 3, wspace=0.28)

    ax1 = fig.add_subplot(grid[0, 0])
    bars = ax1.bar(
        jump_df["benchmark"],
        jump_df["improvement_points"],
        color=["#0f766e", "#2563eb", "#7c3aed"],
    )
    ax1.set_ylabel("Sprong in scorepunten")
    ax1.set_title("Sprongen op moeilijke benchmarks")
    for bar, value in zip(bars, jump_df["improvement_points"], strict=True):
        ax1.text(
            bar.get_x() + (bar.get_width() / 2),
            value + 1,
            f"+{value:.1f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    ax2 = fig.add_subplot(grid[0, 1])
    ax2.plot(dates, normalized_costs, color="#dc2626", linewidth=2.5)
    ax2.fill_between(dates, normalized_costs, color="#fecaca", alpha=0.55)
    ax2.set_yscale("log")
    ax2.set_ylabel("Relatieve kost (log-schaal)")
    ax2.set_title("Kost om GPT-3.5-niveau te halen")
    tick_positions = [dates[0], dates[6], dates[12], dates[18], dates[-1]]
    ax2.set_xticks(tick_positions)
    ax2.set_xticklabels([item.strftime("%Y-%m") for item in tick_positions], rotation=0)
    ax2.annotate(
        ">280x decline\nNov 2022 to Oct 2024",
        xy=(dates[len(dates) // 2], normalized_costs[len(normalized_costs) // 2]),
        xytext=(dates[len(dates) // 3], normalized_costs[0] / 7),
        arrowprops={"arrowstyle": "->", "color": "#7f1d1d"},
        fontsize=10,
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "#fff7ed", "edgecolor": "#fdba74"},
    )

    ax3 = fig.add_subplot(grid[0, 2])
    bars = ax3.bar(growth_df["Metric"], growth_df["Annual factor"], color="#334155")
    ax3.set_ylabel("Jaarfactor")
    ax3.set_title("Compute en efficiency")
    ax3.set_ylim(0, max(growth_df["Annual factor"]) + 1)
    ax3.tick_params(axis="x", rotation=20)
    for bar, factor, doubling in zip(
        bars,
        growth_df["Annual factor"],
        growth_df["Doubling"],
        strict=True,
    ):
        ax3.text(
            bar.get_x() + (bar.get_width() / 2),
            factor + 0.08,
            f"{factor:.2f}x/yr\n{doubling}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.suptitle("Brononderbouwde AI-trends", fontsize=18, fontweight="bold")
    fig.text(
        0.5,
        0.02,
        "Stanford HAI toont benchmarksprongen en >280x kostdaling. Epoch toont sterke compute- en efficiencygroei.",
        ha="center",
        fontsize=11,
        color="#334155",
    )
    fig.subplots_adjust(top=0.84, bottom=0.14)

    output_path = ASSETS_DIR / "ai_trends.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def print_trends_summary(metrics: dict[str, Any]) -> None:
    """Print the audit-friendly AI trends summary.

    Args:
        metrics: Parsed AI trends metrics JSON.
    """
    jump_df = pd.DataFrame(metrics["benchmark_jumps"])
    growth_df = build_growth_dataframe(metrics)
    model_df = build_model_comparison_dataframe(metrics)
    decline = metrics["inference_cost_decline"]
    eci = metrics["epoch_capability_context"]

    print("=" * 72)
    print("AI TRENDS SUMMARY (SOURCE-ANCHORED)")
    print("=" * 72)

    print("\nBenchmark jumps")
    print("-" * 72)
    for row in jump_df.itertuples(index=False):
        print(f"{row.benchmark:12} +{row.improvement_points:.1f} points")

    print("\nInference cost decline")
    print("-" * 72)
    print(
        f"Relative cost declined by >{decline['reduction_factor']:.0f}x "
        f"from {decline['start_month']} to {decline['end_month']}."
    )

    print("\nEpoch trend snapshot")
    print("-" * 72)
    for row in growth_df.itertuples(index=False):
        print(f"{row[0]:24} {row[1]:>5.2f}x/year   doubling: {row[2]}")

    print("\nECI methodology note")
    print("-" * 72)
    print(
        f"Epoch overview: {eci['overview_benchmark_count']} benchmarks; "
        f"data section: {eci['data_section_benchmark_count']} benchmarks."
    )
    print("Deck wording should therefore use 'dozens of benchmarks'.")

    print("\nModel comparison audit")
    print("-" * 72)
    comparison = metrics["model_price_quality_snapshot"]
    opus = comparison["models"][0]
    minimax = comparison["models"][1]
    print(
        f"{opus['name']:18} Terminal Bench {opus['terminal_bench']:>5.1f}%  "
        f"OSWorld {opus['osworld']:>5.1f}%  "
        f"price ${opus['input_price_per_million']:.1f}/${opus['output_price_per_million']:.1f} per 1M"
    )
    print(
        f"{minimax['name']:18} Terminal Bench {minimax['terminal_bench']:>5.1f}%  "
        f"SWE-Pro {minimax['swe_pro']:>5.2f}%  "
        f"price ${minimax['input_price_per_million']:.1f}/${minimax['output_price_per_million']:.1f} per 1M"
    )
    print(f"MiniMax highspeed tier: ${minimax['highspeed_input_price_per_million']:.1f}/${minimax['highspeed_output_price_per_million']:.1f} per 1M")
    print(f"MiniMax skill adherence: {minimax['skill_adherence_pct']:.0f}% across 40 complex skills")
    print(f"MiniMax MMClaw note: {minimax['mmclaw_note']}")
    print(f"Summary line: {comparison['summary_line']}")
    print(comparison["caveat"])

    print("\n" + "=" * 72)


def main() -> None:
    """Run the sourced trend analysis and save the figure."""
    metrics = load_metrics()
    print_trends_summary(metrics)
    output_path = plot_ai_trends(metrics)
    print(f"\nSaved figure: {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
