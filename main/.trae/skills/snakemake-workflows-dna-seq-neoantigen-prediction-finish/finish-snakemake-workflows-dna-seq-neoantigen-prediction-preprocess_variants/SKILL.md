---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-preprocess_variants
description: Use this skill when orchestrating the retained "preprocess_variants" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the preprocess variants stage tied to upstream `concat_variants` and the downstream handoff to `norm_vcf`. It tracks completion via `results/finish/preprocess_variants.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: preprocess_variants
  step_name: preprocess variants
---

# Scope
Use this skill only for the `preprocess_variants` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `concat_variants`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/preprocess_variants.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/preprocess_variants.done`
- Representative outputs: `results/finish/preprocess_variants.done`
- Execution targets: `preprocess_variants`
- Downstream handoff: `norm_vcf`

## Guardrails
- Treat `results/finish/preprocess_variants.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/preprocess_variants.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `norm_vcf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/preprocess_variants.done` exists and `norm_vcf` can proceed without re-running preprocess variants.
