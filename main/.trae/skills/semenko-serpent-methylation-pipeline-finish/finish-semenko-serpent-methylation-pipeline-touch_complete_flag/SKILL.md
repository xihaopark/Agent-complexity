---
name: finish-semenko-serpent-methylation-pipeline-touch_complete_flag
description: Use this skill when orchestrating the retained "touch_complete_flag" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the touch complete flag stage tied to upstream `wgbs_tools_pat_beta` and the downstream handoff to `multiqc`. It tracks completion via `results/finish/touch_complete_flag.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: touch_complete_flag
  step_name: touch complete flag
---

# Scope
Use this skill only for the `touch_complete_flag` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `wgbs_tools_pat_beta`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/touch_complete_flag.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/touch_complete_flag.done`
- Representative outputs: `results/finish/touch_complete_flag.done`
- Execution targets: `touch_complete_flag`
- Downstream handoff: `multiqc`

## Guardrails
- Treat `results/finish/touch_complete_flag.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/touch_complete_flag.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiqc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/touch_complete_flag.done` exists and `multiqc` can proceed without re-running touch complete flag.
