---
name: finish-maxplanck-ie-snakepipes-genrich_peaks
description: Use this skill when orchestrating the retained "Genrich_peaks" step of the maxplanck ie snakepipes finish finish workflow. It keeps the Genrich peaks stage tied to upstream `namesort_bams` and the downstream handoff to `plotFingerprint`. It tracks completion via `results/finish/Genrich_peaks.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: Genrich_peaks
  step_name: Genrich peaks
---

# Scope
Use this skill only for the `Genrich_peaks` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `namesort_bams`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/Genrich_peaks.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/Genrich_peaks.done`
- Representative outputs: `results/finish/Genrich_peaks.done`
- Execution targets: `Genrich_peaks`
- Downstream handoff: `plotFingerprint`

## Guardrails
- Treat `results/finish/Genrich_peaks.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/Genrich_peaks.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plotFingerprint` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/Genrich_peaks.done` exists and `plotFingerprint` can proceed without re-running Genrich peaks.
