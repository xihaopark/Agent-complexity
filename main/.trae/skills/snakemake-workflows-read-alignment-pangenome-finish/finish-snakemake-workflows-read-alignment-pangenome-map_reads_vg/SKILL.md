---
name: finish-snakemake-workflows-read-alignment-pangenome-map_reads_vg
description: Use this skill when orchestrating the retained "map_reads_vg" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the map reads vg stage tied to upstream `create_reference_paths` and the downstream handoff to `reheader_mapped_reads`. It tracks completion via `results/finish/map_reads_vg.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: map_reads_vg
  step_name: map reads vg
---

# Scope
Use this skill only for the `map_reads_vg` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `create_reference_paths`
- Step file: `finish/read-alignment-pangenome-finish/steps/map_reads_vg.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/map_reads_vg.done`
- Representative outputs: `results/finish/map_reads_vg.done`
- Execution targets: `map_reads_vg`
- Downstream handoff: `reheader_mapped_reads`

## Guardrails
- Treat `results/finish/map_reads_vg.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/map_reads_vg.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `reheader_mapped_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/map_reads_vg.done` exists and `reheader_mapped_reads` can proceed without re-running map reads vg.
