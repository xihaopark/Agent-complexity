---
name: finish-mckellardw-slide-snake-ilmn_3c_umitools_dedup_revbam
description: Use this skill when orchestrating the retained "ilmn_3c_umitools_dedup_revBAM" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3c umitools dedup revBAM stage tied to upstream `ilmn_3c_umitools_dedup_fwdBAM` and the downstream handoff to `ilmn_3c_merge_dedup_bam`. It tracks completion via `results/finish/ilmn_3c_umitools_dedup_revBAM.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3c_umitools_dedup_revBAM
  step_name: ilmn 3c umitools dedup revBAM
---

# Scope
Use this skill only for the `ilmn_3c_umitools_dedup_revBAM` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_3c_umitools_dedup_fwdBAM`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3c_umitools_dedup_revBAM.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3c_umitools_dedup_revBAM.done`
- Representative outputs: `results/finish/ilmn_3c_umitools_dedup_revBAM.done`
- Execution targets: `ilmn_3c_umitools_dedup_revBAM`
- Downstream handoff: `ilmn_3c_merge_dedup_bam`

## Guardrails
- Treat `results/finish/ilmn_3c_umitools_dedup_revBAM.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3c_umitools_dedup_revBAM.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_3c_merge_dedup_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3c_umitools_dedup_revBAM.done` exists and `ilmn_3c_merge_dedup_bam` can proceed without re-running ilmn 3c umitools dedup revBAM.
