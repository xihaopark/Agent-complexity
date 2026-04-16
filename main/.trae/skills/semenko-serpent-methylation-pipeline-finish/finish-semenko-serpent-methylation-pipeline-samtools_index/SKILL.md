---
name: finish-semenko-serpent-methylation-pipeline-samtools_index
description: Use this skill when orchestrating the retained "samtools_index" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the samtools index stage tied to upstream `samtools_fixmate_sort_markdup` and the downstream handoff to `samtools_statistics`. It tracks completion via `results/finish/samtools_index.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: samtools_index
  step_name: samtools index
---

# Scope
Use this skill only for the `samtools_index` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `samtools_fixmate_sort_markdup`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/samtools_index.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_index.done`
- Representative outputs: `results/finish/samtools_index.done`
- Execution targets: `samtools_index`
- Downstream handoff: `samtools_statistics`

## Guardrails
- Treat `results/finish/samtools_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_statistics` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_index.done` exists and `samtools_statistics` can proceed without re-running samtools index.
