---
name: finish-snakemake-workflows-read-alignment-pangenome-apply_bqsr
description: Use this skill when orchestrating the retained "apply_bqsr" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the apply bqsr stage tied to upstream `recalibrate_base_qualities` and the downstream handoff to `assign_primers`. It tracks completion via `results/finish/apply_bqsr.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: apply_bqsr
  step_name: apply bqsr
---

# Scope
Use this skill only for the `apply_bqsr` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `recalibrate_base_qualities`
- Step file: `finish/read-alignment-pangenome-finish/steps/apply_bqsr.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/apply_bqsr.done`
- Representative outputs: `results/finish/apply_bqsr.done`
- Execution targets: `apply_bqsr`
- Downstream handoff: `assign_primers`

## Guardrails
- Treat `results/finish/apply_bqsr.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/apply_bqsr.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `assign_primers` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/apply_bqsr.done` exists and `assign_primers` can proceed without re-running apply bqsr.
