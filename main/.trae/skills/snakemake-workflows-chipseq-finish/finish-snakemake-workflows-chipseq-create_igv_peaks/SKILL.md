---
name: finish-snakemake-workflows-chipseq-create_igv_peaks
description: Use this skill when orchestrating the retained "create_igv_peaks" step of the snakemake workflows chipseq finish finish workflow. It keeps the create igv peaks stage tied to upstream `sm_rep_frip_score` and the downstream handoff to `homer_annotatepeaks`. It tracks completion via `results/finish/create_igv_peaks.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: create_igv_peaks
  step_name: create igv peaks
---

# Scope
Use this skill only for the `create_igv_peaks` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `sm_rep_frip_score`
- Step file: `finish/chipseq-finish/steps/create_igv_peaks.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_igv_peaks.done`
- Representative outputs: `results/finish/create_igv_peaks.done`
- Execution targets: `create_igv_peaks`
- Downstream handoff: `homer_annotatepeaks`

## Guardrails
- Treat `results/finish/create_igv_peaks.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_igv_peaks.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `homer_annotatepeaks` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_igv_peaks.done` exists and `homer_annotatepeaks` can proceed without re-running create igv peaks.
