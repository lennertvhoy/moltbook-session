# Model Audit Package

This directory contains a comprehensive audit of the AI-agent network forecasting model.

## Files

| File | Purpose |
|------|---------|
| `MODEL_AUDIT_COMPLETE.md` | Full audit document with all findings |
| `audit_data.json` | Machine-readable ablation and sensitivity results |
| `generate_audit_data.py` | Script to reproduce audit data |
| `generate_audit_plots.py` | Script to generate audit visualizations |
| `README.md` | This file |

## Quick Summary

### Key Finding
The new state-space model (Model C) produces nearly identical crossing probabilities (9.0%) to the simple fixed-growth model (Model A, 8.2%). The sophisticated mean-reverting growth structure adds minimal value because φ=0.9 keeps growth rates close to their mean.

### Primary Driver of Conservatism
The **logit/sigmoid transformation** is responsible for almost all the difference from naive extrapolation. It creates strong saturation at high scores (80+), making late-stage growth extremely slow.

### Most Sensitive Parameters
1. **Floors** (60→55 increases crossing from 8% to 17%)
2. **Initial values** (especially low N=20, G=25)
3. **Growth rates** (especially slow G=0.12)

### Least Sensitive Parameters
1. **φ (persistence)** - 0.7 to 0.99 changes crossing by <1%
2. **Threshold** - 70 to 75 has minimal effect

### Most Binding Floors
1. **G (Governance)** - fails 76% of the time
2. **N (Network)** - fails 65% of the time
3. **M (Memory)** - fails 36% of the time
4. **R (Reliability)** - fails 30% of the time

## Generated Assets

The audit generated additional visualizations in `assets/`:

| File | Description |
|------|-------------|
| `audit_growth_comparison.png` | Old vs new model growth dynamics |
| `audit_sensitivity_tornado.png` | Parameter sensitivity ranking |
| `audit_logit_saturation.png` | Mathematical saturation effects |
| `audit_floor_binding.png` | Which floors fail most often |

## How to Reproduce

```bash
# Generate audit data
uv run python docs/model_audit/generate_audit_data.py

# Generate audit plots
uv run python docs/model_audit/generate_audit_plots.py
```

## Questions?

See `MODEL_AUDIT_COMPLETE.md` Section 12 for "Questions ChatGPT Should Challenge".
