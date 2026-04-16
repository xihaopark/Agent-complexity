---
name: finish-snakemake-workflows-cyrcular-calling-merge_fastqs
description: Use this skill when orchestrating the retained "merge_fastqs" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the merge fastqs stage tied to upstream `minimap2_bam` and the downstream handoff to `samtools_index`. It tracks completion via `results/finish/merge_fastqs.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: merge_fastqs
  step_name: merge fastqs
---

# Scope
Use this skill only for the `merge_fastqs` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `minimap2_bam`
- Step file: `finish/cyrcular-calling-finish/steps/merge_fastqs.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_fastqs.done`
- Representative outputs: `results/finish/merge_fastqs.done`
- Execution targets: `merge_fastqs`
- Downstream handoff: `samtools_index`

## Guardrails
- Treat `results/finish/merge_fastqs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_fastqs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_fastqs.done` exists and `samtools_index` can proceed without re-running merge fastqs.
