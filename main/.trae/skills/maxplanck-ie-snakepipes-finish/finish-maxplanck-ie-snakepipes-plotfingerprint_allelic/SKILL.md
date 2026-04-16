---
name: finish-maxplanck-ie-snakepipes-plotfingerprint_allelic
description: Use this skill when orchestrating the retained "plotFingerprint_allelic" step of the maxplanck ie snakepipes finish finish workflow. It keeps the plotFingerprint allelic stage tied to upstream `plotFingerprint` and the downstream handoff to `MACS2_peak_qc`. It tracks completion via `results/finish/plotFingerprint_allelic.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: plotFingerprint_allelic
  step_name: plotFingerprint allelic
---

# Scope
Use this skill only for the `plotFingerprint_allelic` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `plotFingerprint`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/plotFingerprint_allelic.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plotFingerprint_allelic.done`
- Representative outputs: `results/finish/plotFingerprint_allelic.done`
- Execution targets: `plotFingerprint_allelic`
- Downstream handoff: `MACS2_peak_qc`

## Guardrails
- Treat `results/finish/plotFingerprint_allelic.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plotFingerprint_allelic.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `MACS2_peak_qc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plotFingerprint_allelic.done` exists and `MACS2_peak_qc` can proceed without re-running plotFingerprint allelic.
