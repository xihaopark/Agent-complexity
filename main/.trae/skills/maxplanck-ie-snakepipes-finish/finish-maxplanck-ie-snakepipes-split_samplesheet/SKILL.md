---
name: finish-maxplanck-ie-snakepipes-split_samplesheet
description: Use this skill when orchestrating the retained "split_sampleSheet" step of the maxplanck ie snakepipes finish finish workflow. It keeps the split sampleSheet stage tied to upstream `get_nearest_gene` and the downstream handoff to `filter_gtf`. It tracks completion via `results/finish/split_sampleSheet.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: split_sampleSheet
  step_name: split sampleSheet
---

# Scope
Use this skill only for the `split_sampleSheet` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `get_nearest_gene`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/split_sampleSheet.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/split_sampleSheet.done`
- Representative outputs: `results/finish/split_sampleSheet.done`
- Execution targets: `split_sampleSheet`
- Downstream handoff: `filter_gtf`

## Guardrails
- Treat `results/finish/split_sampleSheet.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/split_sampleSheet.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_gtf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/split_sampleSheet.done` exists and `filter_gtf` can proceed without re-running split sampleSheet.
