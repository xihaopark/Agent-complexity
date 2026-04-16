---
name: finish-joncahn-epigeneticbutton-all_chip
description: Use this skill when orchestrating the retained "all_chip" step of the joncahn epigeneticbutton finish finish workflow. It keeps the all chip stage tied to upstream `perform_pairwise_diff_peaks` and the downstream handoff to `atac_shift_bam`. It tracks completion via `results/finish/all_chip.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: all_chip
  step_name: all chip
---

# Scope
Use this skill only for the `all_chip` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `perform_pairwise_diff_peaks`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/all_chip.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all_chip.done`
- Representative outputs: `results/finish/all_chip.done`
- Execution targets: `all_chip`
- Downstream handoff: `atac_shift_bam`

## Guardrails
- Treat `results/finish/all_chip.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all_chip.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `atac_shift_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/all_chip.done` exists and `atac_shift_bam` can proceed without re-running all chip.
