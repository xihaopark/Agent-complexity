---
name: finish-snakemake-workflows-read-alignment-pangenome-map_reads_bwa
description: Use this skill when orchestrating the retained "map_reads_bwa" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the map reads bwa stage tied to upstream `merge_trimmed_fastqs` and the downstream handoff to `count_sample_kmers`. It tracks completion via `results/finish/map_reads_bwa.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: map_reads_bwa
  step_name: map reads bwa
---

# Scope
Use this skill only for the `map_reads_bwa` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `merge_trimmed_fastqs`
- Step file: `finish/read-alignment-pangenome-finish/steps/map_reads_bwa.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/map_reads_bwa.done`
- Representative outputs: `results/finish/map_reads_bwa.done`
- Execution targets: `map_reads_bwa`
- Downstream handoff: `count_sample_kmers`

## Guardrails
- Treat `results/finish/map_reads_bwa.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/map_reads_bwa.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `count_sample_kmers` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/map_reads_bwa.done` exists and `count_sample_kmers` can proceed without re-running map reads bwa.
