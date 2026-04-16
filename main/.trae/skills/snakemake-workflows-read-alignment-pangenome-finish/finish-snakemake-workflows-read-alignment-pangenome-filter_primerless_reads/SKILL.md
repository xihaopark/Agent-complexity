---
name: finish-snakemake-workflows-read-alignment-pangenome-filter_primerless_reads
description: Use this skill when orchestrating the retained "filter_primerless_reads" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the filter primerless reads stage tied to upstream `assign_primers` and the downstream handoff to `trim_primers`. It tracks completion via `results/finish/filter_primerless_reads.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: filter_primerless_reads
  step_name: filter primerless reads
---

# Scope
Use this skill only for the `filter_primerless_reads` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `assign_primers`
- Step file: `finish/read-alignment-pangenome-finish/steps/filter_primerless_reads.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_primerless_reads.done`
- Representative outputs: `results/finish/filter_primerless_reads.done`
- Execution targets: `filter_primerless_reads`
- Downstream handoff: `trim_primers`

## Guardrails
- Treat `results/finish/filter_primerless_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_primerless_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `trim_primers` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_primerless_reads.done` exists and `trim_primers` can proceed without re-running filter primerless reads.
