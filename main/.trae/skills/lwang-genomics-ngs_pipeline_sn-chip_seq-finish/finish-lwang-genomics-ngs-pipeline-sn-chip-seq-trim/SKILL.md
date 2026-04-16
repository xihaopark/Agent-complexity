---
name: finish-lwang-genomics-ngs-pipeline-sn-chip-seq-trim
description: Use this skill when orchestrating the retained "trim" step of the lwang genomics ngs_pipeline_sn chip_seq finish finish workflow. It keeps the trim stage tied to upstream `fastqc_raw` and the downstream handoff to `align`. It tracks completion via `results/finish/trim.done`.
metadata:
  workflow_id: lwang-genomics-ngs_pipeline_sn-chip_seq-finish
  workflow_name: lwang genomics ngs_pipeline_sn chip_seq finish
  step_id: trim
  step_name: trim
---

# Scope
Use this skill only for the `trim` step in `lwang-genomics-ngs_pipeline_sn-chip_seq-finish`.

## Orchestration
- Upstream requirements: `fastqc_raw`
- Step file: `finish/lwang-genomics-ngs_pipeline_sn-chip_seq-finish/steps/trim.smk`
- Config file: `finish/lwang-genomics-ngs_pipeline_sn-chip_seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/trim.done`
- Representative outputs: `results/finish/trim.done`
- Execution targets: `trim`
- Downstream handoff: `align`

## Guardrails
- Treat `results/finish/trim.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/trim.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `align` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/trim.done` exists and `align` can proceed without re-running trim.
