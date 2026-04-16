---
name: finish-semenko-serpent-methylation-pipeline-biscuit_index
description: Use this skill when orchestrating the retained "biscuit_index" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the biscuit index stage tied to upstream `mask_reference_fasta` and the downstream handoff to `biscuit_qc_index`. It tracks completion via `results/finish/biscuit_index.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: biscuit_index
  step_name: biscuit index
---

# Scope
Use this skill only for the `biscuit_index` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `mask_reference_fasta`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/biscuit_index.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/biscuit_index.done`
- Representative outputs: `results/finish/biscuit_index.done`
- Execution targets: `biscuit_index`
- Downstream handoff: `biscuit_qc_index`

## Guardrails
- Treat `results/finish/biscuit_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/biscuit_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `biscuit_qc_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/biscuit_index.done` exists and `biscuit_qc_index` can proceed without re-running biscuit index.
