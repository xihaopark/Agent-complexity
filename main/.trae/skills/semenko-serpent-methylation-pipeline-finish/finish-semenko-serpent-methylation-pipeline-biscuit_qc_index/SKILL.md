---
name: finish-semenko-serpent-methylation-pipeline-biscuit_qc_index
description: Use this skill when orchestrating the retained "biscuit_qc_index" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the biscuit qc index stage tied to upstream `biscuit_index` and the downstream handoff to `bwa_meth_index`. It tracks completion via `results/finish/biscuit_qc_index.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: biscuit_qc_index
  step_name: biscuit qc index
---

# Scope
Use this skill only for the `biscuit_qc_index` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `biscuit_index`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/biscuit_qc_index.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/biscuit_qc_index.done`
- Representative outputs: `results/finish/biscuit_qc_index.done`
- Execution targets: `biscuit_qc_index`
- Downstream handoff: `bwa_meth_index`

## Guardrails
- Treat `results/finish/biscuit_qc_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/biscuit_qc_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bwa_meth_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/biscuit_qc_index.done` exists and `bwa_meth_index` can proceed without re-running biscuit qc index.
