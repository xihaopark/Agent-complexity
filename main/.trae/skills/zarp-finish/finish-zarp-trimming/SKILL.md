---
name: finish-zarp-trimming
description: Use this skill when orchestrating the retained "trimming" step of the Zarp finish workflow. It frames read trimming as the handoff from staged inputs into downstream alignment.
metadata:
  workflow_id: zarp-finish
  workflow_name: Zarp Finish Workflow
  step_id: trimming
  step_name: Trim staged reads
---

# Scope
Use this skill only for the `trimming` step in `zarp-finish`.

## Orchestration
- Upstream requirements: `stage_inputs`
- Step file: `finish/zarp-finish/steps/trimming.smk`
- Config file: `finish/zarp-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/trimming.done`
- Representative outputs: `output/trimmed/*`
- Execution targets: `trimming_ready`
- Downstream handoff: `alignment`

## Guardrails
- Treat `results/finish/trimming.done` as the authoritative completion signal for this wrapped finish step.
- Keep the step bounded to trimmed-read production; downstream alignment owns mapping outputs.

## Done Criteria
Mark this step complete only when trimmed read outputs exist and the alignment stage can start from the staged workflow assets.
