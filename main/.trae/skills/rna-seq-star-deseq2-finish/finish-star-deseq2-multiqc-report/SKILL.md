---
name: finish-star-deseq2-multiqc-report
description: Use this skill when orchestrating the retained "multiqc_report" step of the RNA-seq STAR DESeq2 finish workflow. It defines the QC aggregation stage, the RSeQC dependency, the final MultiQC artifact, and its role in the finish workflow narrative.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: RNA-seq STAR DESeq2 Finish Workflow
  step_id: multiqc_report
  step_name: Aggregate QC with MultiQC
---

# Scope
Use this skill only for the `multiqc_report` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `rseqc_qc`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/multiqc_report.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/qc/multiqc_report.html`
- Representative outputs: `results/qc/multiqc_report.html`
- Execution targets: `results/qc/multiqc_report.html`
- Downstream handoff: none

## Guardrails
- This workflow slice does not emit a finish stamp; treat the rendered MultiQC HTML as the durable completion artifact.
- Keep this step packaging-oriented and avoid revalidating upstream per-sample QC files as if they were primary outputs here.

## Done Criteria
Mark this step complete only when the MultiQC report is present and reflects the latest QC artifacts produced by `rseqc_qc`.
