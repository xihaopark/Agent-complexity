---
name: finish-semenko-serpent-methylation-pipeline-seqtk_subsample
description: Use this skill when orchestrating the retained "seqtk_subsample" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the seqtk subsample stage tied to upstream `md5sum` and the downstream handoff to `fastp`. It tracks completion via `results/finish/seqtk_subsample.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: seqtk_subsample
  step_name: seqtk subsample
---

# Scope
Use this skill only for the `seqtk_subsample` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `md5sum`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/seqtk_subsample.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/seqtk_subsample.done`
- Representative outputs: `results/finish/seqtk_subsample.done`
- Execution targets: `seqtk_subsample`
- Downstream handoff: `fastp`

## Guardrails
- Treat `results/finish/seqtk_subsample.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/seqtk_subsample.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastp` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/seqtk_subsample.done` exists and `fastp` can proceed without re-running seqtk subsample.
