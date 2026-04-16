---
name: finish-semenko-serpent-methylation-pipeline-md5sum
description: Use this skill when orchestrating the retained "md5sum" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the md5sum stage tied to upstream `wgbs_tools_index` and the downstream handoff to `seqtk_subsample`. It tracks completion via `results/finish/md5sum.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: md5sum
  step_name: md5sum
---

# Scope
Use this skill only for the `md5sum` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `wgbs_tools_index`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/md5sum.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/md5sum.done`
- Representative outputs: `results/finish/md5sum.done`
- Execution targets: `md5sum`
- Downstream handoff: `seqtk_subsample`

## Guardrails
- Treat `results/finish/md5sum.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/md5sum.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `seqtk_subsample` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/md5sum.done` exists and `seqtk_subsample` can proceed without re-running md5sum.
