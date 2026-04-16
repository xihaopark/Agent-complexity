---
name: finish-snakemake-workflows-read-alignment-pangenome-map_consensus_reads
description: Use this skill when orchestrating the retained "map_consensus_reads" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the map consensus reads stage tied to upstream `calc_consensus_reads` and the downstream handoff to `merge_consensus_reads`. It tracks completion via `results/finish/map_consensus_reads.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: map_consensus_reads
  step_name: map consensus reads
---

# Scope
Use this skill only for the `map_consensus_reads` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `calc_consensus_reads`
- Step file: `finish/read-alignment-pangenome-finish/steps/map_consensus_reads.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/map_consensus_reads.done`
- Representative outputs: `results/finish/map_consensus_reads.done`
- Execution targets: `map_consensus_reads`
- Downstream handoff: `merge_consensus_reads`

## Guardrails
- Treat `results/finish/map_consensus_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/map_consensus_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_consensus_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/map_consensus_reads.done` exists and `merge_consensus_reads` can proceed without re-running map consensus reads.
