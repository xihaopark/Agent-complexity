---
name: finish-semenko-serpent-methylation-pipeline-fastp
description: Use this skill when orchestrating the retained "fastp" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the fastp stage tied to upstream `seqtk_subsample` and the downstream handoff to `bwa_meth`. It tracks completion via `results/finish/fastp.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: fastp
  step_name: fastp
---

# Scope
Use this skill only for the `fastp` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `seqtk_subsample`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/fastp.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastp.done`
- Representative outputs: `results/finish/fastp.done`
- Execution targets: `fastp`
- Downstream handoff: `bwa_meth`

## Guardrails
- Treat `results/finish/fastp.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastp.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bwa_meth` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastp.done` exists and `bwa_meth` can proceed without re-running fastp.
