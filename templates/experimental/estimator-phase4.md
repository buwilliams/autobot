# Phase 4 – Calculation Engine & Project-Level Roll-up

- **Calculation logic:**
  - σ_story = (p90 – p50) / 2
  - Σ50 = sum of all p50
  - Σσ = sqrt(sum((p90 – p50)²))
  - MostLikely = Σ50 + 2 × Σσ
  - TotalCost = MostLikely × rate × (1 + ΣadditionalFactors) × calibration
- **API:** GET /projects/:projectId/estimate (returns detailed breakdown)
- **UI:** Project estimate panel with live numbers and confidence intervals
