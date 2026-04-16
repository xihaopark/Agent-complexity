---
name: finish-snakemake-workflows-read-alignment-pangenome-mark_duplicates
description: Use this skill when orchestrating the retained "mark_duplicates" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the mark duplicates stage tied to upstream `annotate_umis` and the downstream handoff to `calc_consensus_reads`. It tracks completion via `results/finish/mark_duplicates.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: mark_duplicates
  step_name: mark duplicates
---

# Scope
Use this skill only for the `mark_duplicates` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `annotate_umis`
- Step file: `finish/read-alignment-pangenome-finish/steps/mark_duplicates.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/mark_duplicates.done`
- Representative outputs: `results/finish/mark_duplicates.done`
- Execution targets: `mark_duplicates`
- Downstream handoff: `calc_consensus_reads`

## Guardrails
- Treat `results/finish/mark_duplicates.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/mark_duplicates.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `calc_consensus_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/mark_duplicates.done` exists and `calc_consensus_reads` can proceed without re-running mark duplicates.
