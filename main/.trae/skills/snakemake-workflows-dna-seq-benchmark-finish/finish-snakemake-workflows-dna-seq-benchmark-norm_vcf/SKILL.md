---
name: finish-snakemake-workflows-dna-seq-benchmark-norm_vcf
description: Use this skill when orchestrating the retained "norm_vcf" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the norm vcf stage tied to upstream `eval` and the downstream handoff to `index_vcf`. It tracks completion via `results/finish/norm_vcf.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: norm_vcf
  step_name: norm vcf
---

# Scope
Use this skill only for the `norm_vcf` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `eval`
- Step file: `finish/dna-seq-benchmark-finish/steps/norm_vcf.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/norm_vcf.done`
- Representative outputs: `results/finish/norm_vcf.done`
- Execution targets: `norm_vcf`
- Downstream handoff: `index_vcf`

## Guardrails
- Treat `results/finish/norm_vcf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/norm_vcf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `index_vcf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/norm_vcf.done` exists and `index_vcf` can proceed without re-running norm vcf.
