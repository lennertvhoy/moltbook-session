"""
Token Usage Analysis for AI Agent Social Networks
Analyzes the cost of a single "social cycle" for an AI agent
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Pricing data (per 1M tokens)
PRICING = {
    "claude_opus_46": {"input": 5.0, "output": 25.0},
    "claude_sonnet_46": {"input": 3.0, "output": 15.0},
    "claude_haiku_37": {"input": 0.25, "output": 1.25},
    "gpt4o": {"input": 2.5, "output": 10.0},
    "minimax_m27": {"input": 0.30, "output": 1.20},
}


def calculate_context_loading_tokens():
    """Calculate tokens for context loading per action"""
    components = {
        "System prompt": 9600,
        "AGENTS.md": 1200,
        "Tool descriptions": 3000,
        "Agent persona": 1500,
        "Previous history": 5000,
    }
    return components


def calculate_social_cycle():
    """
    Calculate token usage for one "social cycle":
    1. Read timeline (10 posts)
    2. Generate reply to 1 post
    3. Make own post
    """
    context = calculate_context_loading_tokens()
    context_total = sum(context.values())
    
    # Per action (context loaded 3 times: read, reply, post)
    cycle = {
        "Context loading (3×)": {"input": context_total * 3, "output": 0},
        "Timeline read (10 posts)": {"input": 500 * 10, "output": 0},
        "Generate reply": {"input": 1500, "output": 800},
        "Make own post": {"input": 1000, "output": 600},
    }
    
    total_input = sum(v["input"] for v in cycle.values())
    total_output = sum(v["output"] for v in cycle.values())
    
    return cycle, total_input, total_output


def calculate_cost(tokens_input, tokens_output, model="claude_opus_46"):
    """Calculate cost in USD for given tokens"""
    pricing = PRICING[model]
    input_cost = (tokens_input / 1_000_000) * pricing["input"]
    output_cost = (tokens_output / 1_000_000) * pricing["output"]
    return input_cost, output_cost, input_cost + output_cost


def generate_cost_comparison():
    """Generate cost comparison across different models"""
    _, total_input, total_output = calculate_social_cycle()
    
    results = []
    for model, pricing in PRICING.items():
        input_cost, output_cost, total = calculate_cost(
            total_input, total_output, model
        )
        results.append({
            "Model": model,
            "Input ($)": round(input_cost, 4),
            "Output ($)": round(output_cost, 4),
            "Total ($)": round(total, 4),
        })
    
    return pd.DataFrame(results)


def generate_scale_comparison():
    """Generate cost at different scales"""
    _, total_input, total_output = calculate_social_cycle()
    _, _, cost_per_cycle = calculate_cost(total_input, total_output, "claude_opus_46")
    
    scales = [
        {"name": "Klein netwerk", "agents": 100, "cycles_per_day": 10},
        {"name": "Medium", "agents": 1000, "cycles_per_day": 10},
        {"name": "Moltbook-achtig", "agents": 10000, "cycles_per_day": 10},
        {"name": "Twitter-schaal", "agents": 100_000_000, "cycles_per_day": 10},
    ]
    
    results = []
    for scale in scales:
        daily = scale["agents"] * scale["cycles_per_day"] * cost_per_cycle
        results.append({
            "Scenario": scale["name"],
            "Agents": f"{scale['agents']:,}",
            "Cycli/dag": scale["cycles_per_day"],
            "Dagelijkse kosten": f"${daily:,.0f}",
            "Jaarlijkse kosten": f"${daily * 365:,.0f}",
        })
    
    return pd.DataFrame(results)


def plot_token_breakdown():
    """Create visualization of token breakdown"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Context loading components
    ax1 = axes[0, 0]
    context = calculate_context_loading_tokens()
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(context)))
    bars = ax1.barh(list(context.keys()), list(context.values()), color=colors)
    ax1.set_xlabel("Tokens")
    ax1.set_title("Context Loading Components (per action)")
    for bar, val in zip(bars, context.values()):
        ax1.text(val + 100, bar.get_y() + bar.get_height()/2, 
                f"{val:,}", va='center', fontsize=9)
    
    # 2. Social cycle breakdown
    ax2 = axes[0, 1]
    cycle, total_input, total_output = calculate_social_cycle()
    actions = list(cycle.keys())
    inputs = [v["input"] for v in cycle.values()]
    outputs = [v["output"] for v in cycle.values()]
    
    x = np.arange(len(actions))
    width = 0.35
    ax2.bar(x - width/2, inputs, width, label='Input tokens', color='steelblue')
    ax2.bar(x + width/2, outputs, width, label='Output tokens', color='coral')
    ax2.set_ylabel("Tokens")
    ax2.set_title("Token Usage per Social Cycle Component")
    ax2.set_xticks(x)
    ax2.set_xticklabels(actions, rotation=45, ha='right', fontsize=8)
    ax2.legend()
    
    # 3. Cost comparison by model
    ax3 = axes[1, 0]
    df_cost = generate_cost_comparison()
    models = df_cost["Model"]
    costs = df_cost["Total ($)"]
    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(models)))
    bars = ax3.bar(range(len(models)), costs, color=colors)
    ax3.set_xticks(range(len(models)))
    ax3.set_xticklabels(models, rotation=45, ha='right', fontsize=8)
    ax3.set_ylabel("Cost per cycle ($)")
    ax3.set_title("Cost Comparison Across Models")
    ax3.set_yscale('log')
    for bar, cost in zip(bars, costs):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.1, 
                f"${cost:.3f}", ha='center', va='bottom', fontsize=8)
    
    # 4. Scale costs
    ax4 = axes[1, 1]
    df_scale = generate_scale_comparison()
    scenarios = df_scale["Scenario"]
    # Extract numeric values from formatted strings
    daily_costs = [float(s.replace('$', '').replace(',', '')) for s in df_scale["Dagelijkse kosten"]]
    colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(scenarios)))
    bars = ax4.bar(range(len(scenarios)), daily_costs, color=colors)
    ax4.set_xticks(range(len(scenarios)))
    ax4.set_xticklabels(scenarios, rotation=45, ha='right', fontsize=9)
    ax4.set_ylabel("Daily cost ($)")
    ax4.set_title("Daily Cost at Different Scales (10 cycles/agent/day)")
    ax4.set_yscale('log')
    for bar, cost in zip(bars, daily_costs):
        label = f"${cost:,.0f}" if cost < 1_000_000 else f"${cost/1_000_000:.1f}M"
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.1, 
                label, ha='center', va='bottom', fontsize=8, rotation=0)
    
    plt.tight_layout()
    plt.savefig("../assets/token_breakdown.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Saved: assets/token_breakdown.png")


def print_analysis():
    """Print full analysis report"""
    print("=" * 70)
    print("TOKEN USAGE ANALYSIS FOR AI AGENT SOCIAL NETWORKS")
    print("=" * 70)
    
    # Context loading
    print("\n1. CONTEXT LOADING BREAKDOWN (per action)")
    print("-" * 50)
    context = calculate_context_loading_tokens()
    for component, tokens in context.items():
        print(f"  {component:25}: {tokens:>8,} tokens")
    print(f"  {'TOTAL':25}: {sum(context.values()):>8,} tokens")
    
    # Social cycle
    print("\n2. SOCIAL CYCLE BREAKDOWN")
    print("-" * 50)
    cycle, total_input, total_output = calculate_social_cycle()
    for action, tokens in cycle.items():
        print(f"  {action:25}: {tokens['input']:>8,} in / {tokens['output']:>6,} out")
    print(f"  {'TOTAL':25}: {total_input:>8,} in / {total_output:>6,} out")
    print(f"  {'GRAND TOTAL':25}: {total_input + total_output:>8,} tokens")
    
    # Cost comparison
    print("\n3. COST COMPARISON BY MODEL")
    print("-" * 50)
    df_cost = generate_cost_comparison()
    print(df_cost.to_string(index=False))
    
    # Scale comparison
    print("\n4. COST AT SCALE (Claude Opus 4.6)")
    print("-" * 50)
    df_scale = generate_scale_comparison()
    print(df_scale.to_string(index=False))
    
    # Key insight
    print("\n5. KEY INSIGHT")
    print("-" * 50)
    _, _, cost_per_cycle = calculate_cost(total_input, total_output, "claude_opus_46")
    print(f"  Cost per social cycle: ${cost_per_cycle:.4f}")
    print(f"  For 10,000 agents doing 10 cycles/day: ${10000 * 10 * cost_per_cycle:,.0f}/day")
    print(f"  Annual cost at Twitter scale: ~${100_000_000 * 10 * cost_per_cycle * 365 / 1e9:.1f}B")
    print("\n  → Social interaction for agents is computationally MUCH more")
    print("    expensive than for humans (~$0 marginal cost per interaction)")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    print_analysis()
    plot_token_breakdown()
    print("\n✓ Token usage analysis complete!")
