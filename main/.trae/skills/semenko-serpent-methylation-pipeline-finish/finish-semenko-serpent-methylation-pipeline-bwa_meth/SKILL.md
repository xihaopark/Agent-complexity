---
name: finish-semenko-serpent-methylation-pipeline-bwa_meth
description: Use this skill when orchestrating the retained "bwa_meth" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the bwa meth stage tied to upstream `fastp` and the downstream handoff to `mark_nonconverted`. It tracks completion via `results/finish/bwa_meth.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: bwa_meth
  step_name: bwa meth
---

# Scope
Use this skill only for the `bwa_meth` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `fastp`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/bwa_meth.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_meth.done`
- Representative outputs: `results/finish/bwa_meth.done`
- Execution targets: `bwa_meth`
- Downstream handoff: `mark_nonconverted`

## Guardrails
- Treat `results/finish/bwa_meth.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_meth.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `mark_nonconverted` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_meth.done` exists and `mark_nonconverted` can proceed without re-running bwa meth.
