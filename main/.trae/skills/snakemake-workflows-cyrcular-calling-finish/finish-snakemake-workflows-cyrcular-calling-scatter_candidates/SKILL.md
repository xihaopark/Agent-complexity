---
name: finish-snakemake-workflows-cyrcular-calling-scatter_candidates
description: Use this skill when orchestrating the retained "scatter_candidates" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the scatter candidates stage tied to upstream `varlociraptor_preprocess` and the downstream handoff to `sort_bnd_bcfs`. It tracks completion via `results/finish/scatter_candidates.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: scatter_candidates
  step_name: scatter candidates
---

# Scope
Use this skill only for the `scatter_candidates` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `varlociraptor_preprocess`
- Step file: `finish/cyrcular-calling-finish/steps/scatter_candidates.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/scatter_candidates.done`
- Representative outputs: `results/finish/scatter_candidates.done`
- Execution targets: `scatter_candidates`
- Downstream handoff: `sort_bnd_bcfs`

## Guardrails
- Treat `results/finish/scatter_candidates.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/scatter_candidates.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sort_bnd_bcfs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/scatter_candidates.done` exists and `sort_bnd_bcfs` can proceed without re-running scatter candidates.
