---
name: finish-semenko-serpent-methylation-pipeline-bwa_meth_index
description: Use this skill when orchestrating the retained "bwa_meth_index" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the bwa meth index stage tied to upstream `biscuit_qc_index` and the downstream handoff to `wgbs_tools_index`. It tracks completion via `results/finish/bwa_meth_index.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: bwa_meth_index
  step_name: bwa meth index
---

# Scope
Use this skill only for the `bwa_meth_index` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `biscuit_qc_index`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/bwa_meth_index.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_meth_index.done`
- Representative outputs: `results/finish/bwa_meth_index.done`
- Execution targets: `bwa_meth_index`
- Downstream handoff: `wgbs_tools_index`

## Guardrails
- Treat `results/finish/bwa_meth_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_meth_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `wgbs_tools_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_meth_index.done` exists and `wgbs_tools_index` can proceed without re-running bwa meth index.
