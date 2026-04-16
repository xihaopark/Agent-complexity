---
name: finish-snakemake-workflows-read-alignment-pangenome-filter_unmapped_primers
description: Use this skill when orchestrating the retained "filter_unmapped_primers" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the filter unmapped primers stage tied to upstream `map_primers` and the downstream handoff to `primer_to_bed`. It tracks completion via `results/finish/filter_unmapped_primers.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: filter_unmapped_primers
  step_name: filter unmapped primers
---

# Scope
Use this skill only for the `filter_unmapped_primers` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `map_primers`
- Step file: `finish/read-alignment-pangenome-finish/steps/filter_unmapped_primers.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_unmapped_primers.done`
- Representative outputs: `results/finish/filter_unmapped_primers.done`
- Execution targets: `filter_unmapped_primers`
- Downstream handoff: `primer_to_bed`

## Guardrails
- Treat `results/finish/filter_unmapped_primers.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_unmapped_primers.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `primer_to_bed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_unmapped_primers.done` exists and `primer_to_bed` can proceed without re-running filter unmapped primers.
