---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-norm_vcf
description: Use this skill when orchestrating the retained "norm_vcf" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the norm vcf stage tied to upstream `preprocess_variants` and the downstream handoff to `freebayes`. It tracks completion via `results/finish/norm_vcf.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: norm_vcf
  step_name: norm vcf
---

# Scope
Use this skill only for the `norm_vcf` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `preprocess_variants`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/norm_vcf.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/norm_vcf.done`
- Representative outputs: `results/finish/norm_vcf.done`
- Execution targets: `norm_vcf`
- Downstream handoff: `freebayes`

## Guardrails
- Treat `results/finish/norm_vcf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/norm_vcf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `freebayes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/norm_vcf.done` exists and `freebayes` can proceed without re-running norm vcf.
