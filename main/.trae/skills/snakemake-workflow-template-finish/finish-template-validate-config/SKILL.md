---
name: finish-template-validate-config
description: Use this skill when orchestrating the retained "validate_config" step of the Snakemake Workflow Template finish workflow. It validates the minimal template configuration and gates downstream reference preparation.
metadata:
  workflow_id: snakemake-workflow-template-finish
  workflow_name: Snakemake Workflow Template Finish Workflow
  step_id: validate_config
  step_name: Validate workflow configuration
---

# Scope
Use this skill only for the `validate_config` step in `snakemake-workflow-template-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/snakemake-workflow-template-finish/steps/validate_config.smk`
- Config file: `finish/snakemake-workflow-template-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/validate_config.done`
- Representative outputs: `results/finish/validate_config.done`
- Downstream handoff: `prepare_reference`

## Guardrails
- Treat `results/finish/validate_config.done` as the authoritative completion signal for this wrapped finish step.
- Do not require transient validation logs to mark the step complete.

## Done Criteria
Mark this step complete only when configuration validation succeeds and reference preparation can start without manual setup changes.
