---
name: finish-snakemake-workflows-read-alignment-pangenome-annotate_umis
description: Use this skill when orchestrating the retained "annotate_umis" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the annotate umis stage tied to upstream `sort_alignments` and the downstream handoff to `mark_duplicates`. It tracks completion via `results/finish/annotate_umis.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: annotate_umis
  step_name: annotate umis
---

# Scope
Use this skill only for the `annotate_umis` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `sort_alignments`
- Step file: `finish/read-alignment-pangenome-finish/steps/annotate_umis.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotate_umis.done`
- Representative outputs: `results/finish/annotate_umis.done`
- Execution targets: `annotate_umis`
- Downstream handoff: `mark_duplicates`

## Guardrails
- Treat `results/finish/annotate_umis.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annotate_umis.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `mark_duplicates` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annotate_umis.done` exists and `mark_duplicates` can proceed without re-running annotate umis.
