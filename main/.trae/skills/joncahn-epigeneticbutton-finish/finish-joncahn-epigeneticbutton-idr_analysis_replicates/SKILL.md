---
name: finish-joncahn-epigeneticbutton-idr_analysis_replicates
description: Use this skill when orchestrating the retained "idr_analysis_replicates" step of the joncahn epigeneticbutton finish finish workflow. It keeps the idr analysis replicates stage tied to upstream `calling_peaks_macs2_se` and the downstream handoff to `merging_chip_replicates`. It tracks completion via `results/finish/idr_analysis_replicates.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: idr_analysis_replicates
  step_name: idr analysis replicates
---

# Scope
Use this skill only for the `idr_analysis_replicates` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `calling_peaks_macs2_se`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/idr_analysis_replicates.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/idr_analysis_replicates.done`
- Representative outputs: `results/finish/idr_analysis_replicates.done`
- Execution targets: `idr_analysis_replicates`
- Downstream handoff: `merging_chip_replicates`

## Guardrails
- Treat `results/finish/idr_analysis_replicates.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/idr_analysis_replicates.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merging_chip_replicates` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/idr_analysis_replicates.done` exists and `merging_chip_replicates` can proceed without re-running idr analysis replicates.
