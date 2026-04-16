---
name: finish-snakemake-workflows-chipseq-merge_se_pe
description: Use this skill when orchestrating the retained "merge_se_pe" step of the snakemake workflows chipseq finish finish workflow. It keeps the merge se pe stage tied to upstream `samtools_sort_pe` and the downstream handoff to `samtools_flagstat`. It tracks completion via `results/finish/merge_se_pe.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: merge_se_pe
  step_name: merge se pe
---

# Scope
Use this skill only for the `merge_se_pe` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `samtools_sort_pe`
- Step file: `finish/chipseq-finish/steps/merge_se_pe.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_se_pe.done`
- Representative outputs: `results/finish/merge_se_pe.done`
- Execution targets: `merge_se_pe`
- Downstream handoff: `samtools_flagstat`

## Guardrails
- Treat `results/finish/merge_se_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_se_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_flagstat` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_se_pe.done` exists and `samtools_flagstat` can proceed without re-running merge se pe.
