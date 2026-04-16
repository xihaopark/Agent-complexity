---
name: finish-semenko-serpent-methylation-pipeline-samtools_fixmate_sort_markdup
description: Use this skill when orchestrating the retained "samtools_fixmate_sort_markdup" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the samtools fixmate sort markdup stage tied to upstream `mark_nonconverted` and the downstream handoff to `samtools_index`. It tracks completion via `results/finish/samtools_fixmate_sort_markdup.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: samtools_fixmate_sort_markdup
  step_name: samtools fixmate sort markdup
---

# Scope
Use this skill only for the `samtools_fixmate_sort_markdup` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `mark_nonconverted`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/samtools_fixmate_sort_markdup.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_fixmate_sort_markdup.done`
- Representative outputs: `results/finish/samtools_fixmate_sort_markdup.done`
- Execution targets: `samtools_fixmate_sort_markdup`
- Downstream handoff: `samtools_index`

## Guardrails
- Treat `results/finish/samtools_fixmate_sort_markdup.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_fixmate_sort_markdup.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_fixmate_sort_markdup.done` exists and `samtools_index` can proceed without re-running samtools fixmate sort markdup.
