---
name: finish-semenko-serpent-methylation-pipeline-wgbs_tools_index
description: Use this skill when orchestrating the retained "wgbs_tools_index" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the wgbs tools index stage tied to upstream `bwa_meth_index` and the downstream handoff to `md5sum`. It tracks completion via `results/finish/wgbs_tools_index.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: wgbs_tools_index
  step_name: wgbs tools index
---

# Scope
Use this skill only for the `wgbs_tools_index` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `bwa_meth_index`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/wgbs_tools_index.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/wgbs_tools_index.done`
- Representative outputs: `results/finish/wgbs_tools_index.done`
- Execution targets: `wgbs_tools_index`
- Downstream handoff: `md5sum`

## Guardrails
- Treat `results/finish/wgbs_tools_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/wgbs_tools_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `md5sum` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/wgbs_tools_index.done` exists and `md5sum` can proceed without re-running wgbs tools index.
