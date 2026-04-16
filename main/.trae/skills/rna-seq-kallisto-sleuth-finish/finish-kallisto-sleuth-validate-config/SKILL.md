---
name: finish-kallisto-sleuth-validate-config
description: Use this skill when orchestrating the retained "validate_config" step of the RNA-seq Kallisto Sleuth finish workflow. It anchors the workflow entry point, validates configuration prerequisites, and gates the rest of the step sequence.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: RNA-seq Kallisto Sleuth Finish Workflow
  step_id: validate_config
  step_name: Validate workflow configuration
---

# Scope
Use this skill only for the `validate_config` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/validate_config.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/validate_config.done`
- Representative outputs: `results/finish/validate_config.done`
- Downstream handoff: `normalize_inputs`

## Guardrails
- Treat `results/finish/validate_config.done` as the authoritative completion signal for this wrapped finish step.
- Do not require nonexistent business outputs such as `logs/validate_config.log` to mark the step complete.

## Done Criteria
Mark this step complete only when configuration validation succeeds and the workflow can proceed to normalized input preparation without manual fixes.
