---
name: finish-snakemake-workflows-chipseq-samtools_sort_pe
description: Use this skill when orchestrating the retained "samtools_sort_pe" step of the snakemake workflows chipseq finish finish workflow. It keeps the samtools sort pe stage tied to upstream `orphan_remove` and the downstream handoff to `merge_se_pe`. It tracks completion via `results/finish/samtools_sort_pe.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: samtools_sort_pe
  step_name: samtools sort pe
---

# Scope
Use this skill only for the `samtools_sort_pe` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `orphan_remove`
- Step file: `finish/chipseq-finish/steps/samtools_sort_pe.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_sort_pe.done`
- Representative outputs: `results/finish/samtools_sort_pe.done`
- Execution targets: `samtools_sort_pe`
- Downstream handoff: `merge_se_pe`

## Guardrails
- Treat `results/finish/samtools_sort_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_sort_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_se_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_sort_pe.done` exists and `merge_se_pe` can proceed without re-running samtools sort pe.
