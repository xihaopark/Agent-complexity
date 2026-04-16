---
name: finish-snakemake-workflows-read-alignment-pangenome-count_sample_kmers
description: Use this skill when orchestrating the retained "count_sample_kmers" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the count sample kmers stage tied to upstream `map_reads_bwa` and the downstream handoff to `create_reference_paths`. It tracks completion via `results/finish/count_sample_kmers.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: count_sample_kmers
  step_name: count sample kmers
---

# Scope
Use this skill only for the `count_sample_kmers` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `map_reads_bwa`
- Step file: `finish/read-alignment-pangenome-finish/steps/count_sample_kmers.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/count_sample_kmers.done`
- Representative outputs: `results/finish/count_sample_kmers.done`
- Execution targets: `count_sample_kmers`
- Downstream handoff: `create_reference_paths`

## Guardrails
- Treat `results/finish/count_sample_kmers.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/count_sample_kmers.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_reference_paths` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/count_sample_kmers.done` exists and `create_reference_paths` can proceed without re-running count sample kmers.
