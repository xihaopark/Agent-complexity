---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-concat_variants
description: Use this skill when orchestrating the retained "concat_variants" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the concat variants stage tied to upstream `reheader_germline` and the downstream handoff to `preprocess_variants`. It tracks completion via `results/finish/concat_variants.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: concat_variants
  step_name: concat variants
---

# Scope
Use this skill only for the `concat_variants` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `reheader_germline`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/concat_variants.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/concat_variants.done`
- Representative outputs: `results/finish/concat_variants.done`
- Execution targets: `concat_variants`
- Downstream handoff: `preprocess_variants`

## Guardrails
- Treat `results/finish/concat_variants.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/concat_variants.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `preprocess_variants` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/concat_variants.done` exists and `preprocess_variants` can proceed without re-running concat variants.
