---
name: finish-snakemake-workflows-read-alignment-pangenome-sort_consensus_reads
description: Use this skill when orchestrating the retained "sort_consensus_reads" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the sort consensus reads stage tied to upstream `merge_consensus_reads` and the downstream handoff to `recalibrate_base_qualities`. It tracks completion via `results/finish/sort_consensus_reads.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: sort_consensus_reads
  step_name: sort consensus reads
---

# Scope
Use this skill only for the `sort_consensus_reads` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `merge_consensus_reads`
- Step file: `finish/read-alignment-pangenome-finish/steps/sort_consensus_reads.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sort_consensus_reads.done`
- Representative outputs: `results/finish/sort_consensus_reads.done`
- Execution targets: `sort_consensus_reads`
- Downstream handoff: `recalibrate_base_qualities`

## Guardrails
- Treat `results/finish/sort_consensus_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sort_consensus_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `recalibrate_base_qualities` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sort_consensus_reads.done` exists and `recalibrate_base_qualities` can proceed without re-running sort consensus reads.
