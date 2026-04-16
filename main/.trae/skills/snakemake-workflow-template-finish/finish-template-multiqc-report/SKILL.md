---
name: finish-template-multiqc-report
description: Use this skill when orchestrating the retained "multiqc_report" step of the Snakemake Workflow Template finish workflow. It defines the terminal QC aggregation step and the final MultiQC artifact for the template workflow.
metadata:
  workflow_id: snakemake-workflow-template-finish
  workflow_name: Snakemake Workflow Template Finish Workflow
  step_id: multiqc_report
  step_name: Aggregate FastQC outputs with MultiQC
---

# Scope
Use this skill only for the `multiqc_report` step in `snakemake-workflow-template-finish`.

## Orchestration
- Upstream requirements: `fastqc`
- Step file: `finish/snakemake-workflow-template-finish/steps/multiqc_report.smk`
- Config file: `finish/snakemake-workflow-template-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/multiqc_report.done`
- Representative outputs: `results/multiqc/multiqc_report.html`
- Execution targets: `results/multiqc/multiqc_report.html`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/multiqc_report.done` as the authoritative completion signal for this wrapped finish step.
- Validate final QC aggregation against the rendered MultiQC report, not against intermediate FastQC directories.

## Done Criteria
Mark this step complete only when the MultiQC report exists and reflects the latest FastQC outputs for the template workflow.
