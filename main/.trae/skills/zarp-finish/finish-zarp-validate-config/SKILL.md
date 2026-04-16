---
name: finish-zarp-validate-config
description: Use this skill when orchestrating the retained "validate_config" step of the Zarp finish workflow. It validates the entry configuration and gates the rest of the finish workflow sequence.
metadata:
  workflow_id: zarp-finish
  workflow_name: Zarp Finish Workflow
  step_id: validate_config
  step_name: Validate workflow configuration
---

# Scope
Use this skill only for the `validate_config` step in `zarp-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/zarp-finish/steps/validate_config.smk`
- Config file: `finish/zarp-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/validate_config.done`
- Representative outputs: `results/finish/validate_config.done`
- Downstream handoff: `stage_inputs`

## Guardrails
- Treat `results/finish/validate_config.done` as the authoritative completion signal for this wrapped finish step.
- Do not rely on transient validation logs to infer completion.

## Done Criteria
Mark this step complete only when configuration validation succeeds and input staging can start without unresolved setup issues.
