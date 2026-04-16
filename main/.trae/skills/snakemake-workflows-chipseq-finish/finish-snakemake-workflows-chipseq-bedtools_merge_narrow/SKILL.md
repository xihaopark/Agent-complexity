---
name: finish-snakemake-workflows-chipseq-bedtools_merge_narrow
description: Use this skill when orchestrating the retained "bedtools_merge_narrow" step of the snakemake workflows chipseq finish finish workflow. It keeps the bedtools merge narrow stage tied to upstream `bedtools_merge_broad` and the downstream handoff to `macs2_merged_expand`. It tracks completion via `results/finish/bedtools_merge_narrow.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: bedtools_merge_narrow
  step_name: bedtools merge narrow
---

# Scope
Use this skill only for the `bedtools_merge_narrow` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `bedtools_merge_broad`
- Step file: `finish/chipseq-finish/steps/bedtools_merge_narrow.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bedtools_merge_narrow.done`
- Representative outputs: `results/finish/bedtools_merge_narrow.done`
- Execution targets: `bedtools_merge_narrow`
- Downstream handoff: `macs2_merged_expand`

## Guardrails
- Treat `results/finish/bedtools_merge_narrow.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bedtools_merge_narrow.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `macs2_merged_expand` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bedtools_merge_narrow.done` exists and `macs2_merged_expand` can proceed without re-running bedtools merge narrow.
