---
name: finish-varlociraptor-validate-config
description: Use this skill when orchestrating the retained "validate_config" step of the DNA-seq Varlociraptor finish workflow. It anchors the workflow entry point, validates configuration inputs, and gates downstream tumor-normal analysis steps.
metadata:
  workflow_id: dna-seq-varlociraptor-finish
  workflow_name: DNA-seq Varlociraptor Finish Workflow
  step_id: validate_config
  step_name: Validate workflow configuration
---

# Scope
Use this skill only for the `validate_config` step in `dna-seq-varlociraptor-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/dna-seq-varlociraptor-finish/steps/validate_config.smk`
- Config file: `finish/dna-seq-varlociraptor-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/validate_config.done`
- Representative outputs: `results/finish/validate_config.done`
- Downstream handoff: `inspect_inputs`

## Guardrails
- Treat `results/finish/validate_config.done` as the authoritative completion signal for this wrapped finish step.
- Do not use transient validation logs as the completion contract.

## Done Criteria
Mark this step complete only when configuration validation succeeds and the input-inspection stage can proceed without unresolved setup issues.
