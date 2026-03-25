# Model Audit Documentation (INTERNAL)

**Status:** Internal documentation — not part of public release canon

This directory contains detailed audit materials for the forecasting model. These documents are:

- **For:** Internal verification, methodology review, and developer reference
- **Not for:** General public reading or citation as canonical project output

## Contents

| File | Purpose | Audience |
|------|---------|----------|
| `MODEL_AUDIT_COMPLETE.md` | Full technical audit of v1→v2 model changes | Technical reviewers |
| `MODEL_V2_DESIGN.md` | Design document for potential future enhancements | Model developers |
| `MODEL_V2_FORMAL_SPECIFICATION.md` | Mathematical formalization of V2 design | Technical reviewers |
| `ablation_validation_report.md` | Ablation study results | Methodology reviewers |
| `FLOOR_JUSTIFICATION_FRAMEWORK.md` | Rationale for floor parameters | Technical reviewers |
| `audit_*.png` | Diagnostic visualizations from audit process | Internal QA |
| `audit_data.json` | Machine-readable audit results | Internal tools |

## Public-Facing Model Description

For the canonical, public-facing explanation of the forecast model, see:
- [`../../content/06-forecast.md`](../../content/06-forecast.md) — Main content explanation
- [`../../analyses/forecast_model.py`](../../analyses/forecast_model.py) — Reference implementation
- [`../../data/forecast_scenarios.json`](../../data/forecast_scenarios.json) — Scenario parameters

## Scope Note

The audit documents in this directory may discuss:
- Alternative model designs not implemented
- Sensitivity analyses and ablation studies
- Known limitations and open questions
- Historical model versions

These discussions are valuable for transparency but are **not** part of the project's public claims or findings. When citing this project, refer to the content in `content/` rather than these audit files.

---

*This directory is part of the repository's internal quality assurance system.*
