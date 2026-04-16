---
name: finish-gersteinlab-astro-feature_counting
description: Use this skill when orchestrating the retained "feature_counting" step of the gersteinlab astro finish finish workflow. It keeps the Feature Counting stage tied to upstream `genome_mapping`. It tracks completion via `results/finish/feature_counting.done`.
metadata:
  workflow_id: gersteinlab-astro-finish
  workflow_name: gersteinlab astro finish
  step_id: feature_counting
  step_name: Feature Counting
---

# Scope
Use this skill only for the `feature_counting` step in `gersteinlab-astro-finish`.

## Orchestration
- Upstream requirements: `genome_mapping`
- Step file: `finish/gersteinlab-astro-finish/steps/feature_counting.smk`
- Config file: `finish/gersteinlab-astro-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/feature_counting.done`
- Representative outputs: `results/finish/feature_counting.done`
- Execution targets: `feature_counting`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/feature_counting.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/feature_counting.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/feature_counting.done` exists and matches the intended step boundary.
