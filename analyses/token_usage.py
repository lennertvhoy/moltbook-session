"""Token usage analysis for an illustrative AI-agent social cycle.

This script intentionally separates sourced context anchors from presentation
assumptions. The resulting cost estimates are therefore reproducible arithmetic,
but they are still scenario outputs rather than observed Moltbook measurements.
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
DATA_PATH = ROOT / "data" / "token_usage_assumptions.json"


def load_assumptions() -> dict[str, Any]:
    """Load the token usage assumptions and pricing metadata.

    Returns:
        Parsed JSON payload describing documented anchors, assumptions, and
        pricing inputs.
    """
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def calculate_context_loading_tokens(assumptions: dict[str, Any]) -> dict[str, int]:
    """Return per-action context loading assumptions.

    Args:
        assumptions: Parsed token usage assumptions JSON.

    Returns:
        Mapping from component label to token count.
    """
    components = assumptions["social_cycle_assumptions"]["context_components_per_action"]
    return {component["name"]: int(component["tokens"]) for component in components}


def calculate_social_cycle(assumptions: dict[str, Any]) -> tuple[dict[str, dict[str, int]], int, int]:
    """Calculate token usage for one illustrative social cycle.

    Args:
        assumptions: Parsed token usage assumptions JSON.

    Returns:
        Tuple of cycle breakdown, total input tokens, and total output tokens.
    """
    context = calculate_context_loading_tokens(assumptions)
    context_total = sum(context.values())
    social = assumptions["social_cycle_assumptions"]

    timeline_tokens = social["timeline_posts"] * social["timeline_tokens_per_post"]
    cycle = {
        "Context loading (3x)": {"input": context_total * 3, "output": 0},
        "Timeline read": {"input": timeline_tokens, "output": 0},
        "Generate reply": {
            "input": social["reply_context_tokens"],
            "output": social["reply_output_tokens"],
        },
        "Create post": {
            "input": social["post_context_tokens"],
            "output": social["post_output_tokens"],
        },
    }

    total_input = sum(item["input"] for item in cycle.values())
    total_output = sum(item["output"] for item in cycle.values())
    return cycle, total_input, total_output


def build_pricing_lookup(assumptions: dict[str, Any]) -> dict[str, dict[str, float]]:
    """Build a lookup of token pricing by model key.

    Args:
        assumptions: Parsed token usage assumptions JSON.

    Returns:
        Mapping from model key to input/output pricing.
    """
    return {
        item["key"]: {
            "model": item["model"],
            "input": float(item["input_price_per_million"]),
            "output": float(item["output_price_per_million"]),
            "source_id": item["source_id"],
        }
        for item in assumptions["pricing"]
    }


def calculate_cost(
    token_input: int,
    token_output: int,
    pricing: dict[str, dict[str, float]],
    model_key: str,
) -> tuple[float, float, float]:
    """Calculate the input, output, and total cost for one cycle.

    Args:
        token_input: Input tokens.
        token_output: Output tokens.
        pricing: Pricing lookup keyed by model name.
        model_key: Model key to use.

    Returns:
        Tuple of input cost, output cost, and total cost in USD.
    """
    model_pricing = pricing[model_key]
    input_cost = (token_input / 1_000_000) * model_pricing["input"]
    output_cost = (token_output / 1_000_000) * model_pricing["output"]
    return input_cost, output_cost, input_cost + output_cost


def generate_cost_comparison(assumptions: dict[str, Any]) -> pd.DataFrame:
    """Generate a cost comparison across the supported model set.

    Args:
        assumptions: Parsed token usage assumptions JSON.

    Returns:
        DataFrame with per-cycle costs by model.
    """
    pricing = build_pricing_lookup(assumptions)
    _, total_input, total_output = calculate_social_cycle(assumptions)

    rows: list[dict[str, Any]] = []
    for model_key, model_pricing in pricing.items():
        input_cost, output_cost, total_cost = calculate_cost(
            total_input,
            total_output,
            pricing,
            model_key,
        )
        rows.append(
            {
                "Model": model_pricing["model"],
                "Input ($)": round(input_cost, 4),
                "Output ($)": round(output_cost, 4),
                "Total ($)": round(total_cost, 4),
                "Source": model_pricing["source_id"],
            }
        )

    return pd.DataFrame(rows).sort_values("Total ($)", ascending=False)


def generate_scale_comparison(assumptions: dict[str, Any], model_key: str) -> pd.DataFrame:
    """Generate daily and annual costs at different network scales.

    Args:
        assumptions: Parsed token usage assumptions JSON.
        model_key: Pricing model used for the scale comparison.

    Returns:
        DataFrame containing daily and annualized costs.
    """
    pricing = build_pricing_lookup(assumptions)
    _, total_input, total_output = calculate_social_cycle(assumptions)
    _, _, cycle_cost = calculate_cost(total_input, total_output, pricing, model_key)

    rows: list[dict[str, Any]] = []
    for scenario in assumptions["scale_scenarios"]:
        daily_cost = scenario["agents"] * scenario["cycles_per_day"] * cycle_cost
        rows.append(
            {
                "Scenario": scenario["name"],
                "Agents": scenario["agents"],
                "Cycles/day": scenario["cycles_per_day"],
                "Daily cost ($)": daily_cost,
                "Annual cost ($)": daily_cost * 365,
            }
        )

    return pd.DataFrame(rows)


def plot_token_breakdown(assumptions: dict[str, Any]) -> Path:
    """Create the presentation-quality token usage figure.

    Args:
        assumptions: Parsed token usage assumptions JSON.

    Returns:
        Path to the saved PNG file.
    """
    context = calculate_context_loading_tokens(assumptions)
    cycle, _, _ = calculate_social_cycle(assumptions)
    cost_df = generate_cost_comparison(assumptions)
    scale_df = generate_scale_comparison(assumptions, "claude_opus_46")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    ax1 = axes[0, 0]
    colors = plt.cm.Blues(np.linspace(0.45, 0.9, len(context)))
    bars = ax1.barh(list(context.keys()), list(context.values()), color=colors)
    ax1.set_title("Illustrative per-action context load")
    ax1.set_xlabel("Tokens")
    for bar, value in zip(bars, context.values(), strict=True):
        ax1.text(value + 100, bar.get_y() + (bar.get_height() / 2), f"{value:,}", va="center", fontsize=9)

    ax2 = axes[0, 1]
    actions = list(cycle.keys())
    input_tokens = [item["input"] for item in cycle.values()]
    output_tokens = [item["output"] for item in cycle.values()]
    x = np.arange(len(actions))
    width = 0.35
    ax2.bar(x - width / 2, input_tokens, width, label="Input tokens", color="#0f766e")
    ax2.bar(x + width / 2, output_tokens, width, label="Output tokens", color="#f97316")
    ax2.set_xticks(x)
    ax2.set_xticklabels(actions, rotation=20, ha="right")
    ax2.set_ylabel("Tokens")
    ax2.set_title("One social cycle under stated assumptions")
    ax2.legend()

    ax3 = axes[1, 0]
    ax3.bar(cost_df["Model"], cost_df["Total ($)"], color=["#7f1d1d", "#9a3412", "#15803d"])
    ax3.set_yscale("log")
    ax3.set_ylabel("Cost per cycle ($, log scale)")
    ax3.set_title("Per-cycle cost by model")
    ax3.tick_params(axis="x", rotation=20)
    for idx, value in enumerate(cost_df["Total ($)"]):
        ax3.text(idx, value * 1.1, f"${value:.3f}", ha="center", va="bottom", fontsize=9)

    ax4 = axes[1, 1]
    ax4.axis("off")
    documented = assumptions["documented_openclaw_example"]
    callout = (
        "Audit notes\n\n"
        f"- OpenClaw docs example: ~{documented['session_tokens_total']:,} total session tokens\n"
        f"- System prompt anchor: ~{documented['system_prompt_tokens']:,} tokens\n"
        "- Presentation cycle is an assumption-driven scenario, not a measured Moltbook trace\n"
        "- Main conclusion is directional: repeated context loading dominates cost\n\n"
        "Selected scale outputs (Opus 4.6)\n"
    )
    for row in scale_df.itertuples(index=False):
        daily_cost = f"${row[3]:,.0f}"
        annual_cost = f"${row[4]:,.0f}"
        callout += f"- {row[0]}: {daily_cost}/day, {annual_cost}/year\n"
    ax4.text(
        0.02,
        0.98,
        callout,
        va="top",
        ha="left",
        fontsize=10,
        family="monospace",
        bbox={"boxstyle": "round,pad=0.6", "facecolor": "#f8fafc", "edgecolor": "#cbd5e1"},
    )

    fig.suptitle("AI-agent social cycle cost model", fontsize=16, fontweight="bold")
    fig.tight_layout()

    output_path = ASSETS_DIR / "token_breakdown.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def print_analysis(assumptions: dict[str, Any]) -> None:
    """Print the audit-friendly token usage summary.

    Args:
        assumptions: Parsed token usage assumptions JSON.
    """
    context = calculate_context_loading_tokens(assumptions)
    cycle, total_input, total_output = calculate_social_cycle(assumptions)
    pricing = build_pricing_lookup(assumptions)
    cost_df = generate_cost_comparison(assumptions)
    scale_df = generate_scale_comparison(assumptions, "claude_opus_46")
    _, _, cycle_cost = calculate_cost(total_input, total_output, pricing, "claude_opus_46")

    print("=" * 72)
    print("TOKEN USAGE ANALYSIS (ILLUSTRATIVE, ASSUMPTION-DRIVEN)")
    print("=" * 72)
    print("\nDocumented OpenClaw anchor")
    print("-" * 72)
    documented = assumptions["documented_openclaw_example"]
    print(
        "OpenClaw docs example:"
        f" system prompt ~{documented['system_prompt_tokens']:,},"
        f" AGENTS.md ~{documented['agents_md_tokens']:,},"
        f" total session tokens ~{documented['session_tokens_total']:,}"
    )

    print("\nPresentation scenario inputs")
    print("-" * 72)
    for component, tokens in context.items():
        print(f"{component:30} {tokens:>8,}")
    print(f"{'Per-action context total':30} {sum(context.values()):>8,}")

    print("\nOne social cycle")
    print("-" * 72)
    for action, tokens in cycle.items():
        print(f"{action:30} {tokens['input']:>8,} in / {tokens['output']:>6,} out")
    print(f"{'TOTAL':30} {total_input:>8,} in / {total_output:>6,} out")
    print(f"{'GRAND TOTAL':30} {total_input + total_output:>8,} tokens")

    print("\nCost comparison")
    print("-" * 72)
    print(cost_df.drop(columns=["Source"]).to_string(index=False))

    print("\nScale comparison (Claude Opus 4.6)")
    print("-" * 72)
    for row in scale_df.itertuples(index=False):
        print(
            f"{row[0]:20} "
            f"{row[1]:>10,} agents  "
            f"{row[2]:>3} cycles/day  "
            f"${row[3]:>13,.0f}/day  "
            f"${row[4]:>15,.0f}/year"
        )

    print("\nInterpretation")
    print("-" * 72)
    print(f"Cost per illustrative social cycle on Claude Opus 4.6: ${cycle_cost:.4f}")
    print("This is not a direct Moltbook measurement.")
    print("It is a transparent scenario showing how quickly repeated context loading dominates cost.")
    print("\n" + "=" * 72)


def main() -> None:
    """Run the token usage analysis and save the visualization."""
    assumptions = load_assumptions()
    print_analysis(assumptions)
    output_path = plot_token_breakdown(assumptions)
    print(f"\nSaved figure: {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
