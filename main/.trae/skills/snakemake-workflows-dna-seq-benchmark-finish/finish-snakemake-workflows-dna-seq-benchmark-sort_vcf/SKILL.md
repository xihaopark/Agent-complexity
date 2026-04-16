---
name: finish-snakemake-workflows-dna-seq-benchmark-sort_vcf
description: Use this skill when orchestrating the retained "sort_vcf" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the sort vcf stage tied to upstream `index_bcf` and the downstream handoff to `get_reads`. It tracks completion via `results/finish/sort_vcf.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: sort_vcf
  step_name: sort vcf
---

# Scope
Use this skill only for the `sort_vcf` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `index_bcf`
- Step file: `finish/dna-seq-benchmark-finish/steps/sort_vcf.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sort_vcf.done`
- Representative outputs: `results/finish/sort_vcf.done`
- Execution targets: `sort_vcf`
- Downstream handoff: `get_reads`

## Guardrails
- Treat `results/finish/sort_vcf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sort_vcf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sort_vcf.done` exists and `get_reads` can proceed without re-running sort vcf.
