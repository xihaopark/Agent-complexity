---
name: finish-snakemake-workflows-chipseq-sm_rep_frip_score
description: Use this skill when orchestrating the retained "sm_rep_frip_score" step of the snakemake workflows chipseq finish finish workflow. It keeps the sm rep frip score stage tied to upstream `frip_score` and the downstream handoff to `create_igv_peaks`. It tracks completion via `results/finish/sm_rep_frip_score.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: sm_rep_frip_score
  step_name: sm rep frip score
---

# Scope
Use this skill only for the `sm_rep_frip_score` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `frip_score`
- Step file: `finish/chipseq-finish/steps/sm_rep_frip_score.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sm_rep_frip_score.done`
- Representative outputs: `results/finish/sm_rep_frip_score.done`
- Execution targets: `sm_rep_frip_score`
- Downstream handoff: `create_igv_peaks`

## Guardrails
- Treat `results/finish/sm_rep_frip_score.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sm_rep_frip_score.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_igv_peaks` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sm_rep_frip_score.done` exists and `create_igv_peaks` can proceed without re-running sm rep frip score.
