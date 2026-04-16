---
name: finish-kallisto-sleuth-normalize-inputs
description: Use this skill when orchestrating the retained "normalize_inputs" step of the RNA-seq Kallisto Sleuth finish workflow. It keeps metadata and workflow inputs normalized after configuration validation and before reference preparation.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: RNA-seq Kallisto Sleuth Finish Workflow
  step_id: normalize_inputs
  step_name: Normalize metadata and workflow inputs
---

# Scope
Use this skill only for the `normalize_inputs` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `validate_config`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/normalize_inputs.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/normalize_inputs.done`
- Representative outputs: `results/finish/normalize_inputs.done`
- Downstream handoff: `prepare_references`

## Guardrails
- Treat `results/finish/normalize_inputs.done` as the authoritative completion signal for this wrapped finish step.
- This step is a workflow-boundary normalization gate, not a full materialization stage with independent analytical outputs.

## Done Criteria
Mark this step complete only when normalized workflow inputs are materialized and the reference-preparation step can consume them directly.
