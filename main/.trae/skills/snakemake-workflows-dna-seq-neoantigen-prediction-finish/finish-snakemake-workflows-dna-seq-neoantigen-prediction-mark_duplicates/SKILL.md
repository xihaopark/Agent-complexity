---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-mark_duplicates
description: Use this skill when orchestrating the retained "mark_duplicates" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the mark duplicates stage tied to upstream `map_reads` and the downstream handoff to `recalibrate_base_qualities`. It tracks completion via `results/finish/mark_duplicates.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: mark_duplicates
  step_name: mark duplicates
---

# Scope
Use this skill only for the `mark_duplicates` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `map_reads`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/mark_duplicates.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/mark_duplicates.done`
- Representative outputs: `results/finish/mark_duplicates.done`
- Execution targets: `mark_duplicates`
- Downstream handoff: `recalibrate_base_qualities`

## Guardrails
- Treat `results/finish/mark_duplicates.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/mark_duplicates.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `recalibrate_base_qualities` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/mark_duplicates.done` exists and `recalibrate_base_qualities` can proceed without re-running mark duplicates.
