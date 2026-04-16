---
name: finish-semenko-serpent-methylation-pipeline-goleft_indexcov
description: Use this skill when orchestrating the retained "goleft_indexcov" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the goleft indexcov stage tied to upstream `fastqc_bam` and the downstream handoff to `wgbs_tools_pat_beta`. It tracks completion via `results/finish/goleft_indexcov.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: goleft_indexcov
  step_name: goleft indexcov
---

# Scope
Use this skill only for the `goleft_indexcov` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `fastqc_bam`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/goleft_indexcov.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/goleft_indexcov.done`
- Representative outputs: `results/finish/goleft_indexcov.done`
- Execution targets: `goleft_indexcov`
- Downstream handoff: `wgbs_tools_pat_beta`

## Guardrails
- Treat `results/finish/goleft_indexcov.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/goleft_indexcov.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `wgbs_tools_pat_beta` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/goleft_indexcov.done` exists and `wgbs_tools_pat_beta` can proceed without re-running goleft indexcov.
