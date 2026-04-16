---
name: finish-varlociraptor-inspect-inputs
description: Use this skill when orchestrating the retained "inspect_inputs" step of the DNA-seq Varlociraptor finish workflow. It checks tumor-normal input readiness after configuration validation and prepares the workflow for reference bundling.
metadata:
  workflow_id: dna-seq-varlociraptor-finish
  workflow_name: DNA-seq Varlociraptor Finish Workflow
  step_id: inspect_inputs
  step_name: Inspect tumor normal inputs
---

# Scope
Use this skill only for the `inspect_inputs` step in `dna-seq-varlociraptor-finish`.

## Orchestration
- Upstream requirements: `validate_config`
- Step file: `finish/dna-seq-varlociraptor-finish/steps/inspect_inputs.smk`
- Config file: `finish/dna-seq-varlociraptor-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/inspect_inputs.done`
- Representative outputs: `results/input_inventory/*`
- Downstream handoff: `prepare_references`

## Guardrails
- Treat `results/finish/inspect_inputs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this step limited to input inventory and readiness checks; reference preparation remains separate.

## Done Criteria
Mark this step complete only when the input inventory is present and the workflow has a clear tumor-normal data picture for reference preparation.
