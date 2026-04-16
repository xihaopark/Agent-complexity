---
name: finish-maxplanck-ie-snakepipes-hmmratac_peaks
description: Use this skill when orchestrating the retained "HMMRATAC_peaks" step of the maxplanck ie snakepipes finish finish workflow. It keeps the HMMRATAC peaks stage tied to upstream `tempChromSizes` and the downstream handoff to `namesort_bams`. It tracks completion via `results/finish/HMMRATAC_peaks.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: HMMRATAC_peaks
  step_name: HMMRATAC peaks
---

# Scope
Use this skill only for the `HMMRATAC_peaks` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `tempChromSizes`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/HMMRATAC_peaks.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/HMMRATAC_peaks.done`
- Representative outputs: `results/finish/HMMRATAC_peaks.done`
- Execution targets: `HMMRATAC_peaks`
- Downstream handoff: `namesort_bams`

## Guardrails
- Treat `results/finish/HMMRATAC_peaks.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/HMMRATAC_peaks.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `namesort_bams` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/HMMRATAC_peaks.done` exists and `namesort_bams` can proceed without re-running HMMRATAC peaks.
