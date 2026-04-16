---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-recalibrate_base_qualities
description: Use this skill when orchestrating the retained "recalibrate_base_qualities" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the recalibrate base qualities stage tied to upstream `mark_duplicates` and the downstream handoff to `apply_bqsr`. It tracks completion via `results/finish/recalibrate_base_qualities.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: recalibrate_base_qualities
  step_name: recalibrate base qualities
---

# Scope
Use this skill only for the `recalibrate_base_qualities` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `mark_duplicates`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/recalibrate_base_qualities.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/recalibrate_base_qualities.done`
- Representative outputs: `results/finish/recalibrate_base_qualities.done`
- Execution targets: `recalibrate_base_qualities`
- Downstream handoff: `apply_bqsr`

## Guardrails
- Treat `results/finish/recalibrate_base_qualities.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/recalibrate_base_qualities.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `apply_bqsr` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/recalibrate_base_qualities.done` exists and `apply_bqsr` can proceed without re-running recalibrate base qualities.
