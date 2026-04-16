---
name: finish-star-deseq2-rseqc-qc
description: Use this skill when orchestrating the retained "rseqc_qc" step of the RNA-seq STAR DESeq2 finish workflow. It keeps the RSeQC quality-control stage aligned with the alignment dependency, expected QC outputs, and the MultiQC aggregation handoff.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: RNA-seq STAR DESeq2 Finish Workflow
  step_id: rseqc_qc
  step_name: Run RSeQC quality control
---

# Scope
Use this skill only for the `rseqc_qc` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `alignment`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/rseqc_qc.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/qc/rseqc/*.infer_experiment.txt`, `results/qc/rseqc/*.stats.txt`, `results/qc/rseqc/*.junctionanno.junction.bed`
- Representative outputs: `results/qc/rseqc/*.infer_experiment.txt`, `results/qc/rseqc/*.stats.txt`, `results/qc/rseqc/*.junctionanno.junction.bed`
- Execution targets: `results/qc/rseqc/*.infer_experiment.txt`, `results/qc/rseqc/*.stats.txt`
- Downstream handoff: `multiqc_report`

## Guardrails
- This workflow slice does not emit a finish stamp; validate completion against stable RSeQC result files rather than log directories.
- Keep this stage limited to per-sample QC artifacts that MultiQC can aggregate.

## Done Criteria
Mark this step complete only when the expected RSeQC reports exist for every aligned sample and the `multiqc_report` step can aggregate them without rerunning alignment.
