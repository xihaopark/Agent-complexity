---
name: finish-maxplanck-ie-snakepipes-plotfingerprint
description: Use this skill when orchestrating the retained "plotFingerprint" step of the maxplanck ie snakepipes finish finish workflow. It keeps the plotFingerprint stage tied to upstream `Genrich_peaks` and the downstream handoff to `plotFingerprint_allelic`. It tracks completion via `results/finish/plotFingerprint.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: plotFingerprint
  step_name: plotFingerprint
---

# Scope
Use this skill only for the `plotFingerprint` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `Genrich_peaks`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/plotFingerprint.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plotFingerprint.done`
- Representative outputs: `results/finish/plotFingerprint.done`
- Execution targets: `plotFingerprint`
- Downstream handoff: `plotFingerprint_allelic`

## Guardrails
- Treat `results/finish/plotFingerprint.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plotFingerprint.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plotFingerprint_allelic` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plotFingerprint.done` exists and `plotFingerprint_allelic` can proceed without re-running plotFingerprint.
