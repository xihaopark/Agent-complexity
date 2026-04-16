---
name: finish-snakemake-workflows-read-alignment-pangenome-merge_consensus_reads
description: Use this skill when orchestrating the retained "merge_consensus_reads" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the merge consensus reads stage tied to upstream `map_consensus_reads` and the downstream handoff to `sort_consensus_reads`. It tracks completion via `results/finish/merge_consensus_reads.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: merge_consensus_reads
  step_name: merge consensus reads
---

# Scope
Use this skill only for the `merge_consensus_reads` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `map_consensus_reads`
- Step file: `finish/read-alignment-pangenome-finish/steps/merge_consensus_reads.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_consensus_reads.done`
- Representative outputs: `results/finish/merge_consensus_reads.done`
- Execution targets: `merge_consensus_reads`
- Downstream handoff: `sort_consensus_reads`

## Guardrails
- Treat `results/finish/merge_consensus_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_consensus_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sort_consensus_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_consensus_reads.done` exists and `sort_consensus_reads` can proceed without re-running merge consensus reads.
