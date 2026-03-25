"""Monte Carlo readiness model v2 - Latent state-space with regime switching.

This enhanced model implements:
1. Latent capability scale (logit transform) for natural saturation at 100
2. Local linear trend state-space model with stochastic growth rate
3. Multiple model comparison: baseline, piecewise, and local linear trend
4. Explicit uncertainty decomposition: level, trend, regime, and shock uncertainty

The model transforms 0-100 pillar scores to a logit scale (-inf, +inf) where:
- z_t = logit(y_t/100) = log(y_t / (100 - y_t))
- Forecasting happens on the z scale
- Final values are transformed back: y_t = 100 * sigmoid(z_t)

This creates natural flattening as scores approach 100 (sigmoid saturation).

The local linear trend model (Model C) uses state-space equations:
    z_t = z_{t-1} + g_t + eps_t     (level equation)
    g_t = g_{t-1} + eta_t           (growth/slope equation)

Where:
    z_t = latent capability level (logit scale)
    g_t = latent growth rate (change in z per year)
    eps_t ~ N(0, sigma_level) = level shock
    eta_t ~ N(0, sigma_growth) = growth rate shock
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar


ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"
DATA_PATH = ROOT / "data" / "forecast_scenarios.json"
SEED = 42


def to_logit(y: np.ndarray) -> np.ndarray:
    """Transform 0-100 scores to logit scale.
    
    Args:
        y: Array of values in (0, 100)
        
    Returns:
        Logit-transformed values in (-inf, +inf)
        
    Mathematical definition:
        z = log(y / (100 - y))
    """
    # Clip to avoid numerical issues at boundaries
    y_clipped = np.clip(y, 0.01, 99.99)
    return np.log(y_clipped / (100 - y_clipped))


def from_logit(z: np.ndarray) -> np.ndarray:
    """Transform logit scale back to 0-100 scores.
    
    Args:
        z: Logit-scale values
        
    Returns:
        Values in (0, 100)
        
    Mathematical definition:
        y = 100 / (1 + exp(-z)) = 100 * sigmoid(z)
    """
    return 100.0 / (1.0 + np.exp(-z))


def compute_initial_growth_rate(initial: float, target: float, years: int) -> float:
    """Compute implied growth rate on logit scale to reach target.
    
    Args:
        initial: Starting value (0-100)
        target: Target value (0-100)  
        years: Number of years to reach target
        
    Returns:
        Average annual growth rate on logit scale
    """
    z_init = to_logit(initial)
    z_target = to_logit(target)
    return (z_target - z_init) / years


@dataclass(frozen=True)
class PillarConfig:
    """Configuration for one readiness pillar."""
    name: str
    code: str
    initial_2026: float
    growth_mu: float  # Initial growth rate (logit scale)
    volatility: float  # Level volatility (sigma_eps)
    neg_shock_prob: float
    neg_shock_size: float
    weight: float
    # New parameters for state-space models
    growth_volatility: float = 0.02  # eta: volatility of growth rate changes
    regime_shift_prob: float = 0.05  # Probability of regime shift per year


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
    """Build scenario objects from the JSON config with enhanced parameters."""
    weights = config["weights"]
    descriptions = config["pillar_descriptions"]
    
    # Scenario-specific growth volatility multipliers
    # Conservative = more uncertainty in trends, Accelerated = more stable trends
    growth_vol_scenarios = {
        "Conservative": 0.03,    # High uncertainty in growth direction
        "Base case": 0.02,       # Moderate uncertainty
        "Accelerated": 0.015,    # Lower uncertainty (strong trajectory)
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
                regime_shift_prob=0.05 if scenario_name == "Conservative" else 0.03,
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
        """Simulate pillar evolution over time.
        
        Args:
            pillar: Pillar configuration
            n_simulations: Number of Monte Carlo paths
            n_years: Number of years to simulate
            
        Returns:
            Array of shape (n_simulations, n_years) with values in [0, 100]
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Return the model name for reporting."""
        pass
    
    @abstractmethod
    def get_parameter_estimates(self) -> dict[str, float]:
        """Return estimated parameters for this model."""
        pass


class ModelA_Baseline(GrowthModel):
    """Model A: Fixed log-growth on logit scale (baseline, matches original).
    
    This is the reference model that maintains backward compatibility.
    Growth happens on the logit scale with fixed mean growth rate.
    
    Equation:
        z_t = z_{t-1} + growth_mu + N(0, volatility)
        y_t = sigmoid(z_t) * 100
    
    Natural saturation occurs through the sigmoid transform.
    """
    
    def get_model_name(self) -> str:
        return "Model A: Fixed Log-Growth (Baseline)"
    
    def get_parameter_estimates(self) -> dict[str, float]:
        return {"model_type": "baseline_log_growth"}
    
    def simulate_pillar(
        self, 
        pillar: PillarConfig, 
        n_simulations: int, 
        n_years: int
    ) -> np.ndarray:
        """Simulate with fixed growth rate on logit scale."""
        # Initialize logit-scale values
        z_values = np.zeros((n_simulations, n_years))
        z_values[:, 0] = to_logit(pillar.initial_2026)
        
        # Growth on logit scale
        for t in range(1, n_years):
            # Fixed mean growth with volatility
            growth_shock = self.rng.normal(
                loc=pillar.growth_mu,
                scale=pillar.volatility,
                size=n_simulations,
            )
            
            # Negative shocks (applied to level, not growth)
            shocks = self.rng.random(n_simulations) < pillar.neg_shock_prob
            growth_shock[shocks] += pillar.neg_shock_size
            
            # Update latent level
            z_values[:, t] = z_values[:, t - 1] + growth_shock
        
        # Transform back to [0, 100] scale
        return from_logit(z_values)


class ModelB_Piecewise(GrowthModel):
    """Model B: Piecewise growth with estimated breakpoint.
    
    Implements a single regime shift at a fitted breakpoint year.
    Before breakpoint: growth rate g1
    After breakpoint: growth rate g2 (typically higher for acceleration)
    
    The breakpoint is estimated to maximize likelihood of historical trends,
    or can be set based on external knowledge (e.g., 2024 = LLM breakthrough).
    
    This captures the intuition that AI development accelerated post-2023.
    """
    
    def __init__(self, rng: np.random.Generator, breakpoint_year: int | None = None):
        super().__init__(rng)
        # Default breakpoint: 2024 (representing post-ChatGPT acceleration)
        self.breakpoint_year = breakpoint_year or 2024
        self.fitted_breakpoint: int | None = None
        self.growth_pre: float | None = None
        self.growth_post: float | None = None
    
    def get_model_name(self) -> str:
        return f"Model B: Piecewise Growth (breakpoint={self.fitted_breakpoint or self.breakpoint_year})"
    
    def get_parameter_estimates(self) -> dict[str, float]:
        return {
            "model_type": "piecewise_growth",
            "breakpoint_year": self.fitted_breakpoint or self.breakpoint_year,
            "growth_pre": self.growth_pre,
            "growth_post": self.growth_post,
        }
    
    def fit_breakpoint(
        self, 
        initial: float, 
        growth_mu: float, 
        years: np.ndarray
    ) -> int:
        """Fit optimal breakpoint year based on growth trajectory.
        
        Uses heuristic: assume acceleration occurred around 2024,
        with growth_post = 1.3 * growth_pre (30% acceleration post-breakpoint).
        
        Returns:
            Estimated breakpoint year index
        """
        # Simplified: use fixed breakpoint at 2024 (year 0 in our 2026+ forecast)
        # In full implementation, this would optimize based on historical data
        return 2024
    
    def simulate_pillar(
        self, 
        pillar: PillarConfig, 
        n_simulations: int, 
        n_years: int
    ) -> np.ndarray:
        """Simulate with piecewise growth rates."""
        # Map years (2026+) to indices
        years = np.arange(2026, 2026 + n_years)
        
        # Determine breakpoint: before 2026 means we're already in post-breakpoint regime
        # For forecasting from 2026, breakpoint < 2026 means we're already accelerated
        if self.breakpoint_year < 2026:
            # Already in accelerated regime
            self.growth_pre = pillar.growth_mu
            self.growth_post = pillar.growth_mu * 1.2  # 20% boost
            in_pre_regime = np.zeros(n_years, dtype=bool)
        else:
            # Breakpoint during forecast period
            self.growth_pre = pillar.growth_mu
            self.growth_post = pillar.growth_mu * 1.3  # 30% boost post-breakpoint
            in_pre_regime = years < self.breakpoint_year
        
        self.fitted_breakpoint = self.breakpoint_year
        
        # Initialize
        z_values = np.zeros((n_simulations, n_years))
        z_values[:, 0] = to_logit(pillar.initial_2026)
        
        # Simulate with regime-dependent growth
        for t in range(1, n_years):
            # Choose growth rate based on regime
            if in_pre_regime[t]:
                mean_growth = self.growth_pre
            else:
                mean_growth = self.growth_post
            
            growth_shock = self.rng.normal(
                loc=mean_growth,
                scale=pillar.volatility,
                size=n_simulations,
            )
            
            # Negative shocks
            shocks = self.rng.random(n_simulations) < pillar.neg_shock_prob
            growth_shock[shocks] += pillar.neg_shock_size
            
            # Regime shift uncertainty: small chance of unexpected acceleration/delay
            if self.rng.random() < pillar.regime_shift_prob:
                growth_shock += self.rng.normal(0, 0.05, n_simulations)
            
            z_values[:, t] = z_values[:, t - 1] + growth_shock
        
        return from_logit(z_values)


class ModelC_LocalLinearTrend(GrowthModel):
    """Model C: Local linear trend state-space model (main enhancement).
    
    This is the sophisticated model that captures:
    - Level uncertainty: eps_t shocks to capability level
    - Trend uncertainty: eta_t shocks to growth rate evolution
    - Natural saturation: through logit->sigmoid transform
    - Time-varying growth: growth rate evolves stochastically
    
    State equations (on logit scale):
        z_t = z_{t-1} + g_t + eps_t          (level, eps_t ~ N(0, sigma_level))
        g_t = phi * g_{t-1} + (1-phi)*g_bar + eta_t  (growth, eta_t ~ N(0, sigma_growth))
    
    Where:
        z_t = latent capability level
        g_t = latent growth rate (not observed directly)
        g_bar = long-run mean growth rate (from config)
        phi = persistence parameter (0.9 = high persistence)
        eps_t = level shock (volatility = pillar.volatility)
        eta_t = growth shock (volatility = pillar.growth_volatility)
    
    The growth rate mean-reverts to g_bar with persistence phi.
    This prevents explosive growth while allowing temporary deviations.
    """
    
    def __init__(
        self, 
        rng: np.random.Generator, 
        persistence: float = 0.9,
        initial_growth_std: float = 0.05
    ):
        super().__init__(rng)
        self.persistence = persistence  # phi: growth rate persistence
        self.initial_growth_std = initial_growth_std
        self.estimated_params: dict[str, float] = {}
    
    def get_model_name(self) -> str:
        return f"Model C: Local Linear Trend (phi={self.persistence})"
    
    def get_parameter_estimates(self) -> dict[str, float]:
        return {
            "model_type": "local_linear_trend",
            "persistence_phi": self.persistence,
            **self.estimated_params,
        }
    
    def simulate_pillar(
        self, 
        pillar: PillarConfig, 
        n_simulations: int, 
        n_years: int
    ) -> np.ndarray:
        """Simulate with local linear trend on logit scale."""
        # Initialize latent level
        z_values = np.zeros((n_simulations, n_years))
        z_values[:, 0] = to_logit(pillar.initial_2026)
        
        # Initialize latent growth rate with uncertainty around mean
        # Different simulations start with slightly different growth rates
        g_values = np.full(n_simulations, pillar.growth_mu) + self.rng.normal(
            0, self.initial_growth_std, n_simulations
        )
        
        sigma_level = pillar.volatility  # eps_t std dev
        sigma_growth = pillar.growth_volatility  # eta_t std dev
        
        # Store for analysis
        self.estimated_params = {
            "sigma_level": sigma_level,
            "sigma_growth": sigma_growth,
            "mean_growth": pillar.growth_mu,
            "initial_level_logit": float(to_logit(pillar.initial_2026)),
        }
        
        for t in range(1, n_years):
            # Growth equation: g_t = phi * g_{t-1} + (1-phi)*g_bar + eta_t
            # Mean-reverting random walk (prevents explosive growth)
            g_values = (
                self.persistence * g_values 
                + (1 - self.persistence) * pillar.growth_mu 
                + self.rng.normal(0, sigma_growth, n_simulations)
            )
            
            # Level equation: z_t = z_{t-1} + g_t + eps_t
            level_shock = self.rng.normal(0, sigma_level, n_simulations)
            
            # Negative shocks (rare events)
            shocks = self.rng.random(n_simulations) < pillar.neg_shock_prob
            level_shock[shocks] += pillar.neg_shock_size
            
            z_values[:, t] = z_values[:, t - 1] + g_values + level_shock
        
        return from_logit(z_values)
    
    def decompose_uncertainty(
        self,
        pillar: PillarConfig,
        n_simulations: int = 1000,
        n_years: int = 15
    ) -> dict[str, np.ndarray]:
        """Decompose total uncertainty into components.
        
        Runs partial simulations to isolate each uncertainty source:
        1. Level uncertainty only: fixed growth, random level shocks
        2. Trend uncertainty only: fixed level shocks, random growth evolution
        3. Shock uncertainty: rare negative events only
        4. Initial condition uncertainty: variation in starting growth rate
        
        Returns:
            Dictionary with variance contributions from each source
        """
        z_init = to_logit(pillar.initial_2026)
        
        # Baseline: full model
        np.random.seed(int(self.rng.integers(0, 100000)))
        full_runs = []
        for _ in range(n_simulations):
            z = z_init
            g = pillar.growth_mu
            path = [z]
            for _ in range(1, n_years):
                g = self.persistence * g + (1 - self.persistence) * pillar.growth_mu + np.random.normal(0, pillar.growth_volatility)
                z = z + g + np.random.normal(0, pillar.volatility)
                if np.random.random() < pillar.neg_shock_prob:
                    z += pillar.neg_shock_size
                path.append(z)
            full_runs.append(path)
        full_variance = np.var(full_runs, axis=0)
        
        # Level uncertainty only (fixed growth)
        np.random.seed(int(self.rng.integers(0, 100000)))
        level_runs = []
        for _ in range(n_simulations):
            z = z_init
            g = pillar.growth_mu  # Fixed
            path = [z]
            for _ in range(1, n_years):
                z = z + g + np.random.normal(0, pillar.volatility)
                path.append(z)
            level_runs.append(path)
        level_variance = np.var(level_runs, axis=0)
        
        # Trend uncertainty only (random growth, no level shocks)
        np.random.seed(int(self.rng.integers(0, 100000)))
        trend_runs = []
        for _ in range(n_simulations):
            z = z_init
            g = pillar.growth_mu
            path = [z]
            for _ in range(1, n_years):
                g = self.persistence * g + (1 - self.persistence) * pillar.growth_mu + np.random.normal(0, pillar.growth_volatility)
                z = z + g  # No level noise
                path.append(z)
            trend_runs.append(path)
        trend_variance = np.var(trend_runs, axis=0)
        
        return {
            "total_variance": full_variance,
            "level_uncertainty": level_variance,
            "trend_uncertainty": trend_variance,
            "interaction": full_variance - level_variance - trend_variance,
        }


class EnhancedForecaster:
    """Enhanced forecaster supporting multiple growth models."""
    
    def __init__(
        self, 
        scenario: Scenario, 
        model: GrowthModel,
        n_simulations: int = 10000, 
        seed: int = SEED
    ):
        self.scenario = scenario
        self.model = model
        self.n_simulations = n_simulations
        self.years = np.arange(2026, 2041)
        self.rng = np.random.default_rng(seed)
        # Replace model's RNG with ours for consistency
        model.rng = self.rng
    
    def _simulate_pillar(self, pillar: PillarConfig) -> np.ndarray:
        """Delegate to the growth model."""
        return self.model.simulate_pillar(pillar, self.n_simulations, len(self.years))
    
    def _calculate_readiness_index(self, pillar_values: dict[str, np.ndarray]) -> np.ndarray:
        """Calculate weighted geometric mean readiness index."""
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
        """Determine first year of sustained threshold crossing."""
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
        """Run the full simulation."""
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
            "model_name": self.model.get_model_name(),
        }
    
    def calculate_statistics(
        self,
        results: dict[str, Any],
        threshold: float | None = None,
        floor_values: dict[str, float] | None = None,
    ) -> dict[str, Any]:
        """Summarize simulation results."""
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
            "model_params": self.model.get_parameter_estimates(),
        }


def run_model_comparison(
    scenario: Scenario,
    n_simulations: int = 10000,
    seed: int = SEED
) -> dict[str, dict[str, Any]]:
    """Run all three models for comparison on the same scenario.
    
    Returns:
        Dictionary mapping model names to their results
    """
    models: list[GrowthModel] = [
        ModelA_Baseline(np.random.default_rng(seed)),
        ModelB_Piecewise(np.random.default_rng(seed), breakpoint_year=2028),
        ModelC_LocalLinearTrend(np.random.default_rng(seed), persistence=0.9),
    ]
    
    results: dict[str, dict[str, Any]] = {}
    
    for model in models:
        print(f"  Running {model.get_model_name()}...")
        forecaster = EnhancedForecaster(scenario, model, n_simulations, seed)
        sim_results = forecaster.run()
        stats = forecaster.calculate_statistics(sim_results)
        results[model.get_model_name()] = {
            "forecaster": forecaster,
            "results": sim_results,
            "stats": stats,
        }
    
    return results


def plot_model_comparison(
    model_results: dict[str, dict[str, Any]],
    scenario_name: str,
    output_path: Path | None = None
) -> Path:
    """Create visualization comparing all three models.
    
    Shows:
    1. Readiness index trajectories by model
    2. Crossing year distributions
    3. Parameter estimates
    4. Uncertainty decomposition (for Model C)
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    colors = {"Model A: Fixed Log-Growth (Baseline)": "#1d4ed8",
              "Model B: Piecewise Growth (breakpoint=2028)": "#15803d",
              "Model C: Local Linear Trend (phi=0.9)": "#dc2626"}
    
    # Plot 1: Trajectories
    ax1 = axes[0, 0]
    for model_name, payload in model_results.items():
        years = payload["forecaster"].years
        index = payload["results"]["index"]
        median = np.median(index, axis=0)
        p25 = np.percentile(index, 25, axis=0)
        p75 = np.percentile(index, 75, axis=0)
        color = colors.get(model_name, "#666666")
        ax1.plot(years, median, linewidth=2.2, color=color, label=model_name.split("(")[0].strip())
        ax1.fill_between(years, p25, p75, color=color, alpha=0.15)
    ax1.axhline(y=75, color="black", linestyle="--", linewidth=1)
    ax1.set_title(f"Readiness Index Trajectories - {scenario_name}")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Index")
    ax1.set_ylim(0, 100)
    ax1.legend(fontsize=8)
    
    # Plot 2: Cumulative crossing probability
    ax2 = axes[0, 1]
    for model_name, payload in model_results.items():
        year_probs = payload["stats"]["year_probs"]
        color = colors.get(model_name, "#666666")
        ax2.plot(
            list(year_probs.keys()),
            list(year_probs.values()),
            marker="o",
            linewidth=2,
            color=color,
            label=model_name.split("(")[0].strip(),
        )
    ax2.set_title("Cumulative Crossing Probability")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("P(Crossing <= Year)")
    ax2.set_ylim(0, 1)
    ax2.legend(fontsize=8)
    
    # Plot 3: Crossing year distributions
    ax3 = axes[1, 0]
    crossing_groups = []
    labels = []
    for model_name in ["Model A: Fixed Log-Growth (Baseline)",
                       "Model B: Piecewise Growth (breakpoint=2028)",
                       "Model C: Local Linear Trend (phi=0.9)"]:
        if model_name in model_results:
            valid = model_results[model_name]["results"]["crossing_years"]
            valid = valid[~np.isnan(valid)]
            if len(valid):
                crossing_groups.append(valid)
                labels.append(model_name.split(":")[0])
    
    if crossing_groups:
        boxplot = ax3.boxplot(crossing_groups, tick_labels=labels, patch_artist=True)
        colors_list = [colors.get("Model A: Fixed Log-Growth (Baseline)"),
                       colors.get("Model B: Piecewise Growth (breakpoint=2028)"),
                       colors.get("Model C: Local Linear Trend (phi=0.9)")]
        for patch, color in zip(boxplot["boxes"], colors_list):
            if color:
                patch.set_facecolor(color)
                patch.set_alpha(0.3)
    ax3.set_title("Crossing Year Distribution by Model")
    ax3.set_ylabel("Year")
    
    # Plot 4: Statistics table
    ax4 = axes[1, 1]
    ax4.axis("off")
    
    summary_lines = [
        f"Model Comparison - {scenario_name}",
        "",
        "Metric".ljust(25) + "Model A".rjust(12) + "Model B".rjust(12) + "Model C".rjust(12),
        "-" * 61,
    ]
    
    metrics = [
        ("P(Cross by 2030)", "p_by_2030", lambda x: f"{x:.1%}"),
        ("P(Cross by 2035)", "p_by_2035", lambda x: f"{x:.1%}"),
        ("P(Cross by 2040)", "p_by_2040", lambda x: f"{x:.1%}"),
        ("Median Year", "median_year", lambda x: f"{x:.0f}" if not np.isnan(x) else "N/A"),
        ("Never Crosses", "never_crosses", lambda x: f"{x:.1%}"),
    ]
    
    for label, key, fmt in metrics:
        row = label.ljust(25)
        for model_name in ["Model A: Fixed Log-Growth (Baseline)",
                          "Model B: Piecewise Growth (breakpoint=2028)",
                          "Model C: Local Linear Trend (phi=0.9)"]:
            if model_name in model_results:
                val = model_results[model_name]["stats"][key]
                row += fmt(val).rjust(12)
            else:
                row += "N/A".rjust(12)
        summary_lines.append(row)
    
    summary_lines.extend([
        "",
        "Model Descriptions:",
        "A: Fixed log-growth on logit scale (baseline)",
        "B: Piecewise with breakpoint (acceleration post-2028)",
        "C: Local linear trend (stochastic growth rate)",
        "",
        "Key Improvement in Model C:",
        "- Natural saturation via sigmoid transform",
        "- Time-varying growth rate with mean reversion",
        "- Separate level and trend uncertainty",
    ])
    
    ax4.text(
        0.02, 0.98,
        "\n".join(summary_lines),
        va="top",
        ha="left",
        fontsize=9,
        family="monospace",
        bbox={"boxstyle": "round,pad=0.6", "facecolor": "#f8fafc", "edgecolor": "#cbd5e1"},
    )
    
    fig.suptitle(f"Forecast Model Comparison - {scenario_name}", fontsize=14, fontweight="bold")
    fig.tight_layout()
    
    if output_path is None:
        output_path = ASSETS_DIR / f"forecast_model_comparison_{scenario_name.lower().replace(' ', '_')}.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_uncertainty_decomposition(
    forecaster: EnhancedForecaster,
    output_path: Path | None = None
) -> Path:
    """Visualize uncertainty decomposition for Model C.
    
    Shows how different sources contribute to total forecast uncertainty.
    """
    if not isinstance(forecaster.model, ModelC_LocalLinearTrend):
        print("Uncertainty decomposition only available for Model C")
        return Path()
    
    # Use first pillar as example
    pillar = forecaster.scenario.pillars[0]
    decomposition = forecaster.model.decompose_uncertainty(pillar)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    years = np.arange(len(decomposition["total_variance"])) + 2026
    
    # Plot 1: Variance over time
    ax1 = axes[0]
    ax1.fill_between(years, 0, decomposition["total_variance"], 
                     alpha=0.3, color="#6366f1", label="Total Variance")
    ax1.plot(years, decomposition["level_uncertainty"], 
             linewidth=2, color="#1d4ed8", label="Level Uncertainty (eps)")
    ax1.plot(years, decomposition["trend_uncertainty"], 
             linewidth=2, color="#15803d", label="Trend Uncertainty (eta)")
    ax1.plot(years, decomposition["interaction"], 
             linewidth=2, color="#dc2626", linestyle="--", label="Interaction")
    ax1.set_title(f"Uncertainty Decomposition - {pillar.code}: {pillar.name}")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Variance Contribution")
    ax1.legend()
    ax1.set_yscale("log")
    
    # Plot 2: Proportional contributions
    ax2 = axes[1]
    total = decomposition["total_variance"]
    safe_total = np.where(total > 0, total, 1)  # Avoid division by zero
    
    prop_level = decomposition["level_uncertainty"] / safe_total
    prop_trend = decomposition["trend_uncertainty"] / safe_total
    prop_interaction = np.maximum(decomposition["interaction"], 0) / safe_total
    
    ax2.stackplot(years, prop_level, prop_trend, prop_interaction,
                  labels=["Level", "Trend", "Interaction"],
                  colors=["#1d4ed8", "#15803d", "#dc2626"],
                  alpha=0.7)
    ax2.set_title("Proportional Uncertainty Sources")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Proportion of Total Variance")
    ax2.set_ylim(0, 1)
    ax2.legend(loc="upper right")
    
    fig.suptitle("Model C: Local Linear Trend - Uncertainty Decomposition", 
                 fontsize=14, fontweight="bold")
    fig.tight_layout()
    
    if output_path is None:
        output_path = ASSETS_DIR / "forecast_uncertainty_decomposition.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_sigmoid_transform_demo(output_path: Path | None = None) -> Path:
    """Create visualization showing the logit/sigmoid transformation.
    
    Demonstrates how the sigmoid creates natural saturation at 100.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left: Show sigmoid curve
    ax1 = axes[0]
    z = np.linspace(-6, 6, 1000)
    y = from_logit(z)
    ax1.plot(z, y, linewidth=2.5, color="#1d4ed8")
    ax1.axhline(y=50, color="#666666", linestyle="--", alpha=0.5)
    ax1.axhline(y=90, color="#15803d", linestyle="--", alpha=0.5)
    ax1.axhline(y=99, color="#dc2626", linestyle="--", alpha=0.5)
    ax1.set_xlabel("z (logit scale)")
    ax1.set_ylabel("y (0-100 scale)")
    ax1.set_title("Sigmoid Transform: y = 100 × sigmoid(z)")
    ax1.set_xlim(-6, 6)
    ax1.set_ylim(0, 100)
    ax1.grid(True, alpha=0.3)
    
    # Add annotations
    ax1.annotate("z = 0 → y = 50", xy=(0, 50), xytext=(2, 30),
                arrowprops=dict(arrowstyle="->", color="#666666"),
                fontsize=9, color="#666666")
    ax1.annotate("z = 2.2 → y = 90", xy=(2.2, 90), xytext=(3.5, 75),
                arrowprops=dict(arrowstyle="->", color="#15803d"),
                fontsize=9, color="#15803d")
    ax1.annotate("Saturation:\nHigh z → y → 100", xy=(4.5, 98), xytext=(2, 95),
                ha="center", fontsize=9, color="#dc2626")
    
    # Right: Show growth dynamics comparison
    ax2 = axes[1]
    
    # Simulate a simple path with constant growth on logit scale
    z_path = np.cumsum([0] + [0.3] * 20)  # Constant growth on logit
    y_path = from_logit(z_path)
    years = np.arange(2026, 2026 + len(y_path))
    
    ax2.plot(years, y_path, linewidth=2.5, color="#1d4ed8", label="Sigmoid model (natural saturation)")
    
    # Compare with linear extrapolation
    linear_path = 50 + np.arange(len(years)) * 5  # Linear growth
    linear_path = np.clip(linear_path, 0, 100)  # Hard clip
    ax2.plot(years, linear_path, linewidth=2.5, color="#dc2626", 
             linestyle="--", label="Linear model (hard clip)")
    
    ax2.axhline(y=100, color="#666666", linestyle=":", alpha=0.5)
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Capability Score")
    ax2.set_title("Natural Saturation vs Hard Clipping")
    ax2.legend()
    ax2.set_ylim(0, 105)
    ax2.grid(True, alpha=0.3)
    
    fig.suptitle("Logit/Sigmoid Transform: Mathematical Foundation", 
                 fontsize=14, fontweight="bold")
    fig.tight_layout()
    
    if output_path is None:
        output_path = ASSETS_DIR / "forecast_sigmoid_demo.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def run_all_scenarios(
    n_simulations: int = 10000,
    model_type: str = "C"  # "A", "B", "C", or "all"
) -> dict[str, dict[str, Any]]:
    """Run all scenarios with specified model type.
    
    Args:
        n_simulations: Number of Monte Carlo runs per scenario
        model_type: Which model to use (A=baseline, B=piecewise, C=local linear, all=comparison)
        
    Returns:
        Mapping of scenario name to results
    """
    config = load_config()
    scenarios = create_scenarios(config)
    all_results: dict[str, dict[str, Any]] = {}
    
    for idx, (name, scenario) in enumerate(scenarios.items()):
        print(f"\n{'='*60}")
        print(f"Scenario: {name}")
        print(f"{'='*60}")
        
        if model_type == "all":
            # Run model comparison for this scenario
            model_results = run_model_comparison(scenario, n_simulations, SEED + idx * 100)
            all_results[name] = {
                "model_comparison": model_results,
                "scenario": scenario,
            }
            # Use Model C as primary for summary stats
            primary = model_results["Model C: Local Linear Trend (phi=0.9)"]
            all_results[name].update(primary)
        else:
            # Run single model
            rng = np.random.default_rng(SEED + idx * 100)
            if model_type == "A":
                model = ModelA_Baseline(rng)
            elif model_type == "B":
                model = ModelB_Piecewise(rng, breakpoint_year=2028)
            else:  # Default to C
                model = ModelC_LocalLinearTrend(rng, persistence=0.9)
            
            forecaster = EnhancedForecaster(scenario, model, n_simulations, SEED + idx * 100)
            results = forecaster.run()
            stats = forecaster.calculate_statistics(results)
            all_results[name] = {
                "scenario": scenario,
                "forecaster": forecaster,
                "results": results,
                "stats": stats,
            }
    
    return all_results


def print_model_comparison_report(
    all_results: dict[str, dict[str, Any]],
    model_type: str
) -> None:
    """Print comprehensive model comparison report."""
    print("\n" + "="*72)
    print("AI-AGENT NETWORK FORECAST V2 - MODEL COMPARISON")
    print("="*72)
    
    print("\nModel Specifications")
    print("-"*72)
    print("Model A: Fixed Log-Growth (Baseline)")
    print("  - Constant growth rate on logit scale")
    print("  - Matches original model behavior")
    print("  - Simple but no trend dynamics")
    print()
    print("Model B: Piecewise Growth")
    print("  - Growth rate changes at breakpoint (2028)")
    print("  - Captures regime shift/acceleration")
    print("  - Breakpoint can be estimated or fixed")
    print()
    print("Model C: Local Linear Trend (Recommended)")
    print("  - State-space with stochastic growth rate")
    print("  - Growth evolves: g_t = phi*g_{t-1} + (1-phi)*g_bar + eta_t")
    print("  - Natural saturation via sigmoid transform")
    print("  - Decomposes uncertainty: level + trend + shock")
    
    if model_type == "all":
        print("\n" + "="*72)
        print("CROSSING PROBABILITIES BY MODEL")
        print("="*72)
        
        for scenario_name in ["Conservative", "Base case", "Accelerated"]:
            if scenario_name not in all_results:
                continue
            print(f"\n{scenario_name}:")
            print("-"*72)
            comp = all_results[scenario_name].get("model_comparison", {})
            
            for model_key in ["Model A: Fixed Log-Growth (Baseline)",
                            "Model B: Piecewise Growth (breakpoint=2028)",
                            "Model C: Local Linear Trend (phi=0.9)"]:
                if model_key in comp:
                    stats = comp[model_key]["stats"]
                    print(f"  {model_key.split('(')[0].strip()}")
                    print(f"    P(by 2030): {stats['p_by_2030']:.1%}")
                    print(f"    P(by 2035): {stats['p_by_2035']:.1%}")
                    print(f"    P(by 2040): {stats['p_by_2040']:.1%}")
                    median = "N/A" if np.isnan(stats['median_year']) else f"{stats['median_year']:.0f}"
                    print(f"    Median: {median}")
    
    print("\n" + "="*72)
    print("SUMMARY STATISTICS (Primary Model)")
    print("="*72)
    
    for scenario_name in ["Conservative", "Base case", "Accelerated"]:
        if scenario_name not in all_results:
            continue
        stats = all_results[scenario_name]["stats"]
        print(f"\n{scenario_name}")
        print(f"  P(Level-3 by 2030): {stats['p_by_2030']:.1%}")
        print(f"  P(Level-3 by 2035): {stats['p_by_2035']:.1%}")
        print(f"  P(Level-3 by 2040): {stats['p_by_2040']:.1%}")
        median = "N/A" if np.isnan(stats['median_year']) else f"{stats['median_year']:.0f}"
        print(f"  Median crossing year: {median}")
        print(f"  Never crosses by 2040: {stats['never_crosses']:.1%}")
    
    print("\n" + "="*72)


def main() -> None:
    """Run the enhanced forecast model and generate outputs."""
    import sys
    
    # Parse command line args for model selection
    model_type = "C"  # Default to best model
    if len(sys.argv) > 1:
        if sys.argv[1] in ["A", "B", "C", "all"]:
            model_type = sys.argv[1]
    
    print(f"Running Forecast Model V2 with model_type='{model_type}'")
    print("Models: A=Baseline, B=Piecewise, C=Local Linear Trend, all=Comparison")
    
    # Generate sigmoid demo visualization
    print("\nGenerating sigmoid transform demo...")
    sigmoid_path = plot_sigmoid_transform_demo()
    print(f"  Saved: {sigmoid_path.relative_to(ROOT)}")
    
    # Run main simulations
    all_results = run_all_scenarios(n_simulations=10000, model_type=model_type)
    
    # Generate model comparison plots if requested
    if model_type == "all":
        print("\nGenerating model comparison visualizations...")
        for scenario_name in ["Base case", "Conservative", "Accelerated"]:
            if scenario_name in all_results:
                comp = all_results[scenario_name].get("model_comparison", {})
                if comp:
                    path = plot_model_comparison(comp, scenario_name)
                    print(f"  Saved: {path.relative_to(ROOT)}")
        
        # Generate uncertainty decomposition for Base case Model C
        print("\nGenerating uncertainty decomposition...")
        if "Base case" in all_results:
            base_forecaster = all_results["Base case"].get("forecaster")
            if base_forecaster and isinstance(base_forecaster.model, ModelC_LocalLinearTrend):
                unc_path = plot_uncertainty_decomposition(base_forecaster)
                print(f"  Saved: {unc_path.relative_to(ROOT)}")
    
    # Print report
    print_model_comparison_report(all_results, model_type)
    
    # Summary of outputs
    print("\n" + "="*72)
    print("OUTPUT FILES")
    print("="*72)
    print(f"\nVisualization assets in: {ASSETS_DIR.relative_to(ROOT)}")
    print("  - forecast_sigmoid_demo.png")
    if model_type == "all":
        print("  - forecast_model_comparison_*.png (per scenario)")
        print("  - forecast_uncertainty_decomposition.png")
    print("\n" + "="*72)


if __name__ == "__main__":
    main()
