---
name: finish-semenko-serpent-methylation-pipeline-wgbs_tools_pat_beta
description: Use this skill when orchestrating the retained "wgbs_tools_pat_beta" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the wgbs tools pat beta stage tied to upstream `goleft_indexcov` and the downstream handoff to `touch_complete_flag`. It tracks completion via `results/finish/wgbs_tools_pat_beta.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: wgbs_tools_pat_beta
  step_name: wgbs tools pat beta
---

# Scope
Use this skill only for the `wgbs_tools_pat_beta` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `goleft_indexcov`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/wgbs_tools_pat_beta.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/wgbs_tools_pat_beta.done`
- Representative outputs: `results/finish/wgbs_tools_pat_beta.done`
- Execution targets: `wgbs_tools_pat_beta`
- Downstream handoff: `touch_complete_flag`

## Guardrails
- Treat `results/finish/wgbs_tools_pat_beta.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/wgbs_tools_pat_beta.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `touch_complete_flag` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/wgbs_tools_pat_beta.done` exists and `touch_complete_flag` can proceed without re-running wgbs tools pat beta.
