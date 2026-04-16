---
name: finish-mckellardw-slide-snake-ilmn_3c_umitools_dedup_fwdbam
description: Use this skill when orchestrating the retained "ilmn_3c_umitools_dedup_fwdBAM" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3c umitools dedup fwdBAM stage tied to upstream `ilmn_3c_strand_split_bam` and the downstream handoff to `ilmn_3c_umitools_dedup_revBAM`. It tracks completion via `results/finish/ilmn_3c_umitools_dedup_fwdBAM.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3c_umitools_dedup_fwdBAM
  step_name: ilmn 3c umitools dedup fwdBAM
---

# Scope
Use this skill only for the `ilmn_3c_umitools_dedup_fwdBAM` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_3c_strand_split_bam`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3c_umitools_dedup_fwdBAM.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3c_umitools_dedup_fwdBAM.done`
- Representative outputs: `results/finish/ilmn_3c_umitools_dedup_fwdBAM.done`
- Execution targets: `ilmn_3c_umitools_dedup_fwdBAM`
- Downstream handoff: `ilmn_3c_umitools_dedup_revBAM`

## Guardrails
- Treat `results/finish/ilmn_3c_umitools_dedup_fwdBAM.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3c_umitools_dedup_fwdBAM.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_3c_umitools_dedup_revBAM` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3c_umitools_dedup_fwdBAM.done` exists and `ilmn_3c_umitools_dedup_revBAM` can proceed without re-running ilmn 3c umitools dedup fwdBAM.
