---
name: finish-snakemake-workflows-cyrcular-calling-reheader_filtered_bcf
description: Use this skill when orchestrating the retained "reheader_filtered_bcf" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the reheader filtered bcf stage tied to upstream `cyrcular_annotate_graph` and the downstream handoff to `sort_bcf_header`. It tracks completion via `results/finish/reheader_filtered_bcf.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: reheader_filtered_bcf
  step_name: reheader filtered bcf
---

# Scope
Use this skill only for the `reheader_filtered_bcf` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `cyrcular_annotate_graph`
- Step file: `finish/cyrcular-calling-finish/steps/reheader_filtered_bcf.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/reheader_filtered_bcf.done`
- Representative outputs: `results/finish/reheader_filtered_bcf.done`
- Execution targets: `reheader_filtered_bcf`
- Downstream handoff: `sort_bcf_header`

## Guardrails
- Treat `results/finish/reheader_filtered_bcf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/reheader_filtered_bcf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sort_bcf_header` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/reheader_filtered_bcf.done` exists and `sort_bcf_header` can proceed without re-running reheader filtered bcf.
