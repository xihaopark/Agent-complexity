---
name: finish-snakemake-workflows-chipseq-frip_score
description: Use this skill when orchestrating the retained "frip_score" step of the snakemake workflows chipseq finish finish workflow. It keeps the frip score stage tied to upstream `bedtools_intersect` and the downstream handoff to `sm_rep_frip_score`. It tracks completion via `results/finish/frip_score.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: frip_score
  step_name: frip score
---

# Scope
Use this skill only for the `frip_score` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `bedtools_intersect`
- Step file: `finish/chipseq-finish/steps/frip_score.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/frip_score.done`
- Representative outputs: `results/finish/frip_score.done`
- Execution targets: `frip_score`
- Downstream handoff: `sm_rep_frip_score`

## Guardrails
- Treat `results/finish/frip_score.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/frip_score.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sm_rep_frip_score` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/frip_score.done` exists and `sm_rep_frip_score` can proceed without re-running frip score.
