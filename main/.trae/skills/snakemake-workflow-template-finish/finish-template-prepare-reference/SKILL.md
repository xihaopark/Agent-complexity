---
name: finish-template-prepare-reference
description: Use this skill when orchestrating the retained "prepare_reference" step of the Snakemake Workflow Template finish workflow. It turns validated configuration into reference assets and prepares the simulation stage.
metadata:
  workflow_id: snakemake-workflow-template-finish
  workflow_name: Snakemake Workflow Template Finish Workflow
  step_id: prepare_reference
  step_name: Prepare reference assets
---

# Scope
Use this skill only for the `prepare_reference` step in `snakemake-workflow-template-finish`.

## Orchestration
- Upstream requirements: `validate_config`
- Step file: `finish/snakemake-workflow-template-finish/steps/prepare_reference.smk`
- Config file: `finish/snakemake-workflow-template-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepare_reference.done`
- Representative outputs: `results/validate_genome/genome.fna`
- Execution targets: `results/validate_genome/genome.fna`
- Downstream handoff: `simulate_reads`

## Guardrails
- Treat `results/finish/prepare_reference.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to reference materialization; downstream read simulation owns synthetic read generation.

## Done Criteria
Mark this step complete only when the reference assets are present and simulated read generation can proceed without rebuilding them.
