---
name: finish-snakemake-workflows-read-alignment-pangenome-merge_trimmed_fastqs
description: Use this skill when orchestrating the retained "merge_trimmed_fastqs" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the merge trimmed fastqs stage tied to upstream `fastp_pe` and the downstream handoff to `map_reads_bwa`. It tracks completion via `results/finish/merge_trimmed_fastqs.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: merge_trimmed_fastqs
  step_name: merge trimmed fastqs
---

# Scope
Use this skill only for the `merge_trimmed_fastqs` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `fastp_pe`
- Step file: `finish/read-alignment-pangenome-finish/steps/merge_trimmed_fastqs.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_trimmed_fastqs.done`
- Representative outputs: `results/finish/merge_trimmed_fastqs.done`
- Execution targets: `merge_trimmed_fastqs`
- Downstream handoff: `map_reads_bwa`

## Guardrails
- Treat `results/finish/merge_trimmed_fastqs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_trimmed_fastqs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `map_reads_bwa` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_trimmed_fastqs.done` exists and `map_reads_bwa` can proceed without re-running merge trimmed fastqs.
