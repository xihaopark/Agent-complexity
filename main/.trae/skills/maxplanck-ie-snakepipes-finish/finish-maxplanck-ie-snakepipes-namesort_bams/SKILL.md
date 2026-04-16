---
name: finish-maxplanck-ie-snakepipes-namesort_bams
description: Use this skill when orchestrating the retained "namesort_bams" step of the maxplanck ie snakepipes finish finish workflow. It keeps the namesort bams stage tied to upstream `HMMRATAC_peaks` and the downstream handoff to `Genrich_peaks`. It tracks completion via `results/finish/namesort_bams.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: namesort_bams
  step_name: namesort bams
---

# Scope
Use this skill only for the `namesort_bams` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `HMMRATAC_peaks`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/namesort_bams.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/namesort_bams.done`
- Representative outputs: `results/finish/namesort_bams.done`
- Execution targets: `namesort_bams`
- Downstream handoff: `Genrich_peaks`

## Guardrails
- Treat `results/finish/namesort_bams.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/namesort_bams.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `Genrich_peaks` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/namesort_bams.done` exists and `Genrich_peaks` can proceed without re-running namesort bams.
