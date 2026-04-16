---
name: finish-snakemake-workflows-read-alignment-pangenome-create_reference_paths
description: Use this skill when orchestrating the retained "create_reference_paths" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the create reference paths stage tied to upstream `count_sample_kmers` and the downstream handoff to `map_reads_vg`. It tracks completion via `results/finish/create_reference_paths.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: create_reference_paths
  step_name: create reference paths
---

# Scope
Use this skill only for the `create_reference_paths` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `count_sample_kmers`
- Step file: `finish/read-alignment-pangenome-finish/steps/create_reference_paths.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_reference_paths.done`
- Representative outputs: `results/finish/create_reference_paths.done`
- Execution targets: `create_reference_paths`
- Downstream handoff: `map_reads_vg`

## Guardrails
- Treat `results/finish/create_reference_paths.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_reference_paths.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `map_reads_vg` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_reference_paths.done` exists and `map_reads_vg` can proceed without re-running create reference paths.
