---
name: finish-snakemake-workflows-read-alignment-pangenome-sort_alignments
description: Use this skill when orchestrating the retained "sort_alignments" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the sort alignments stage tied to upstream `add_read_group` and the downstream handoff to `annotate_umis`. It tracks completion via `results/finish/sort_alignments.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: sort_alignments
  step_name: sort alignments
---

# Scope
Use this skill only for the `sort_alignments` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `add_read_group`
- Step file: `finish/read-alignment-pangenome-finish/steps/sort_alignments.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sort_alignments.done`
- Representative outputs: `results/finish/sort_alignments.done`
- Execution targets: `sort_alignments`
- Downstream handoff: `annotate_umis`

## Guardrails
- Treat `results/finish/sort_alignments.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sort_alignments.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annotate_umis` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sort_alignments.done` exists and `annotate_umis` can proceed without re-running sort alignments.
