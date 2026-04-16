---
name: finish-star-deseq2-trimming
description: Use this skill when orchestrating the retained "trimming" step of the RNA-seq STAR DESeq2 finish workflow. It captures the step goal, dependency chain, completion artifacts, and downstream handoff so the agent can run or validate this step in order.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: RNA-seq STAR DESeq2 Finish Workflow
  step_id: trimming
  step_name: Trimming reads
---

# Scope
Use this skill only for the `trimming` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/rna-seq-star-deseq2-finish/steps/trimming.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/trimmed/*/*.fastq.gz`
- Representative outputs: `results/trimmed/*/*.fastq.gz`, `results/trimmed/*/*.html`, `results/trimmed/*/*.json`
- Execution targets: `results/trimmed/*/*.fastq.gz`
- Downstream handoff: `alignment`

## Guardrails
- This workflow slice does not emit a finish stamp; validate completion against the trimmed FASTQ outputs themselves.
- Keep this step scoped to trimmed read outputs and fastp QC sidecars, not downstream alignment products.

## Done Criteria
Mark this step complete only when trimmed FASTQ outputs exist for every planned sample and the `alignment` step can start without recreating upstream inputs.
