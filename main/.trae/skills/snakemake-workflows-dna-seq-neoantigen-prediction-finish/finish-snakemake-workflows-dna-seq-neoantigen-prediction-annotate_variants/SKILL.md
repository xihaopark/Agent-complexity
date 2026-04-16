---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-annotate_variants
description: Use this skill when orchestrating the retained "annotate_variants" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the annotate variants stage tied to upstream `bcftools_concat` and the downstream handoff to `annotate_strelka_variants`. It tracks completion via `results/finish/annotate_variants.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: annotate_variants
  step_name: annotate variants
---

# Scope
Use this skill only for the `annotate_variants` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `bcftools_concat`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/annotate_variants.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotate_variants.done`
- Representative outputs: `results/finish/annotate_variants.done`
- Execution targets: `annotate_variants`
- Downstream handoff: `annotate_strelka_variants`

## Guardrails
- Treat `results/finish/annotate_variants.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annotate_variants.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annotate_strelka_variants` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annotate_variants.done` exists and `annotate_strelka_variants` can proceed without re-running annotate variants.
