---
name: finish-snakemake-workflows-read-alignment-pangenome-trim_primers
description: Use this skill when orchestrating the retained "trim_primers" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the trim primers stage tied to upstream `filter_primerless_reads` and the downstream handoff to `map_primers`. It tracks completion via `results/finish/trim_primers.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: trim_primers
  step_name: trim primers
---

# Scope
Use this skill only for the `trim_primers` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `filter_primerless_reads`
- Step file: `finish/read-alignment-pangenome-finish/steps/trim_primers.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/trim_primers.done`
- Representative outputs: `results/finish/trim_primers.done`
- Execution targets: `trim_primers`
- Downstream handoff: `map_primers`

## Guardrails
- Treat `results/finish/trim_primers.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/trim_primers.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `map_primers` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/trim_primers.done` exists and `map_primers` can proceed without re-running trim primers.
