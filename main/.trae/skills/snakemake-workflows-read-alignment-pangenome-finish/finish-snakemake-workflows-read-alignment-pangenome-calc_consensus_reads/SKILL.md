---
name: finish-snakemake-workflows-read-alignment-pangenome-calc_consensus_reads
description: Use this skill when orchestrating the retained "calc_consensus_reads" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the calc consensus reads stage tied to upstream `mark_duplicates` and the downstream handoff to `map_consensus_reads`. It tracks completion via `results/finish/calc_consensus_reads.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: calc_consensus_reads
  step_name: calc consensus reads
---

# Scope
Use this skill only for the `calc_consensus_reads` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `mark_duplicates`
- Step file: `finish/read-alignment-pangenome-finish/steps/calc_consensus_reads.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/calc_consensus_reads.done`
- Representative outputs: `results/finish/calc_consensus_reads.done`
- Execution targets: `calc_consensus_reads`
- Downstream handoff: `map_consensus_reads`

## Guardrails
- Treat `results/finish/calc_consensus_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/calc_consensus_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `map_consensus_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/calc_consensus_reads.done` exists and `map_consensus_reads` can proceed without re-running calc consensus reads.
