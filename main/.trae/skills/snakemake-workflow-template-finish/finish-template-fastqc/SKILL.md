---
name: finish-template-fastqc
description: Use this skill when orchestrating the retained "fastqc" step of the Snakemake Workflow Template finish workflow. It analyzes simulated reads with FastQC and prepares the aggregated MultiQC report.
metadata:
  workflow_id: snakemake-workflow-template-finish
  workflow_name: Snakemake Workflow Template Finish Workflow
  step_id: fastqc
  step_name: Run FastQC on simulated reads
---

# Scope
Use this skill only for the `fastqc` step in `snakemake-workflow-template-finish`.

## Orchestration
- Upstream requirements: `simulate_reads`
- Step file: `finish/snakemake-workflow-template-finish/steps/fastqc.smk`
- Config file: `finish/snakemake-workflow-template-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastqc.done`
- Representative outputs: `results/fastqc/*`
- Downstream handoff: `multiqc_report`

## Guardrails
- Treat `results/finish/fastqc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage focused on per-sample QC artifacts; MultiQC remains a separate aggregation step.

## Done Criteria
Mark this step complete only when FastQC outputs are present for the simulated reads and MultiQC can aggregate them directly.
