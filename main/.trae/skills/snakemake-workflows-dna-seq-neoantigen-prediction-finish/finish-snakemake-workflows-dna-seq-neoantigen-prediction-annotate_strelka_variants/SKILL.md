---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-annotate_strelka_variants
description: Use this skill when orchestrating the retained "annotate_strelka_variants" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the annotate strelka variants stage tied to upstream `annotate_variants` and the downstream handoff to `filter_by_annotation`. It tracks completion via `results/finish/annotate_strelka_variants.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: annotate_strelka_variants
  step_name: annotate strelka variants
---

# Scope
Use this skill only for the `annotate_strelka_variants` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `annotate_variants`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/annotate_strelka_variants.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotate_strelka_variants.done`
- Representative outputs: `results/finish/annotate_strelka_variants.done`
- Execution targets: `annotate_strelka_variants`
- Downstream handoff: `filter_by_annotation`

## Guardrails
- Treat `results/finish/annotate_strelka_variants.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annotate_strelka_variants.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_by_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annotate_strelka_variants.done` exists and `filter_by_annotation` can proceed without re-running annotate strelka variants.
