---
name: finish-snakemake-workflows-read-alignment-pangenome-assign_primers
description: Use this skill when orchestrating the retained "assign_primers" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the assign primers stage tied to upstream `apply_bqsr` and the downstream handoff to `filter_primerless_reads`. It tracks completion via `results/finish/assign_primers.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: assign_primers
  step_name: assign primers
---

# Scope
Use this skill only for the `assign_primers` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `apply_bqsr`
- Step file: `finish/read-alignment-pangenome-finish/steps/assign_primers.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/assign_primers.done`
- Representative outputs: `results/finish/assign_primers.done`
- Execution targets: `assign_primers`
- Downstream handoff: `filter_primerless_reads`

## Guardrails
- Treat `results/finish/assign_primers.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/assign_primers.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_primerless_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/assign_primers.done` exists and `filter_primerless_reads` can proceed without re-running assign primers.
