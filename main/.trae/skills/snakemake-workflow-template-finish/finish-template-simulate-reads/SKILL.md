---
name: finish-template-simulate-reads
description: Use this skill when orchestrating the retained "simulate_reads" step of the Snakemake Workflow Template finish workflow. It uses prepared references to generate example reads and hands them to FastQC.
metadata:
  workflow_id: snakemake-workflow-template-finish
  workflow_name: Snakemake Workflow Template Finish Workflow
  step_id: simulate_reads
  step_name: Simulate example reads
---

# Scope
Use this skill only for the `simulate_reads` step in `snakemake-workflow-template-finish`.

## Orchestration
- Upstream requirements: `prepare_reference`
- Step file: `finish/snakemake-workflow-template-finish/steps/simulate_reads.smk`
- Config file: `finish/snakemake-workflow-template-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/simulate_reads.done`
- Representative outputs: `results/simulated_reads/*`
- Downstream handoff: `fastqc`

## Guardrails
- Treat `results/finish/simulate_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this step scoped to synthetic read generation; QC aggregation belongs to later steps.

## Done Criteria
Mark this step complete only when simulated reads exist and the FastQC stage can run without regenerating reference assets.
