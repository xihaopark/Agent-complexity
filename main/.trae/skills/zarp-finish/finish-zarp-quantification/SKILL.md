---
name: finish-zarp-quantification
description: Use this skill when orchestrating the retained "quantification" step of the Zarp finish workflow. It defines how aligned reads become quantification outputs and prepares the final finish target aggregation.
metadata:
  workflow_id: zarp-finish
  workflow_name: Zarp Finish Workflow
  step_id: quantification
  step_name: Quantify aligned reads
---

# Scope
Use this skill only for the `quantification` step in `zarp-finish`.

## Orchestration
- Upstream requirements: `alignment`
- Step file: `finish/zarp-finish/steps/quantification.smk`
- Config file: `finish/zarp-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/quantification.done`
- Representative outputs: `output/quantification/*`
- Execution targets: `quantification_ready`
- Downstream handoff: `finish_target`

## Guardrails
- Treat `results/finish/quantification.done` as the authoritative completion signal for this wrapped finish step.
- Keep quantification isolated from final packaging so the terminal finish step can remain lightweight.

## Done Criteria
Mark this step complete only when quantification outputs exist and the finish-target step can assemble the final artifacts without rerunning alignment.
