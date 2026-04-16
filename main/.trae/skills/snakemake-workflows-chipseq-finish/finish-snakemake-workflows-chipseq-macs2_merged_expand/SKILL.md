---
name: finish-snakemake-workflows-chipseq-macs2_merged_expand
description: Use this skill when orchestrating the retained "macs2_merged_expand" step of the snakemake workflows chipseq finish finish workflow. It keeps the macs2 merged expand stage tied to upstream `bedtools_merge_narrow` and the downstream handoff to `create_consensus_bed`. It tracks completion via `results/finish/macs2_merged_expand.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: macs2_merged_expand
  step_name: macs2 merged expand
---

# Scope
Use this skill only for the `macs2_merged_expand` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `bedtools_merge_narrow`
- Step file: `finish/chipseq-finish/steps/macs2_merged_expand.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/macs2_merged_expand.done`
- Representative outputs: `results/finish/macs2_merged_expand.done`
- Execution targets: `macs2_merged_expand`
- Downstream handoff: `create_consensus_bed`

## Guardrails
- Treat `results/finish/macs2_merged_expand.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/macs2_merged_expand.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_consensus_bed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/macs2_merged_expand.done` exists and `create_consensus_bed` can proceed without re-running macs2 merged expand.
