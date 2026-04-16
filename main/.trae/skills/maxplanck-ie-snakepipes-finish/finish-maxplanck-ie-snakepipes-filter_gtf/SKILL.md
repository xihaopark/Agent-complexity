---
name: finish-maxplanck-ie-snakepipes-filter_gtf
description: Use this skill when orchestrating the retained "filter_gtf" step of the maxplanck ie snakepipes finish finish workflow. It keeps the filter gtf stage tied to upstream `split_sampleSheet` and the downstream handoff to `gtf_to_files`. It tracks completion via `results/finish/filter_gtf.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: filter_gtf
  step_name: filter gtf
---

# Scope
Use this skill only for the `filter_gtf` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `split_sampleSheet`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/filter_gtf.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_gtf.done`
- Representative outputs: `results/finish/filter_gtf.done`
- Execution targets: `filter_gtf`
- Downstream handoff: `gtf_to_files`

## Guardrails
- Treat `results/finish/filter_gtf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_gtf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gtf_to_files` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_gtf.done` exists and `gtf_to_files` can proceed without re-running filter gtf.
