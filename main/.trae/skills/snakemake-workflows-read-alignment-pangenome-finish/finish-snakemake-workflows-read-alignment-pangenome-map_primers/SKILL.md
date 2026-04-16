---
name: finish-snakemake-workflows-read-alignment-pangenome-map_primers
description: Use this skill when orchestrating the retained "map_primers" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the map primers stage tied to upstream `trim_primers` and the downstream handoff to `filter_unmapped_primers`. It tracks completion via `results/finish/map_primers.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: map_primers
  step_name: map primers
---

# Scope
Use this skill only for the `map_primers` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `trim_primers`
- Step file: `finish/read-alignment-pangenome-finish/steps/map_primers.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/map_primers.done`
- Representative outputs: `results/finish/map_primers.done`
- Execution targets: `map_primers`
- Downstream handoff: `filter_unmapped_primers`

## Guardrails
- Treat `results/finish/map_primers.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/map_primers.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_unmapped_primers` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/map_primers.done` exists and `filter_unmapped_primers` can proceed without re-running map primers.
