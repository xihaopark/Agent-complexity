---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-filter_by_annotation
description: Use this skill when orchestrating the retained "filter_by_annotation" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the filter by annotation stage tied to upstream `annotate_strelka_variants` and the downstream handoff to `filter_odds`. It tracks completion via `results/finish/filter_by_annotation.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: filter_by_annotation
  step_name: filter by annotation
---

# Scope
Use this skill only for the `filter_by_annotation` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `annotate_strelka_variants`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/filter_by_annotation.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_by_annotation.done`
- Representative outputs: `results/finish/filter_by_annotation.done`
- Execution targets: `filter_by_annotation`
- Downstream handoff: `filter_odds`

## Guardrails
- Treat `results/finish/filter_by_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_by_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_odds` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_by_annotation.done` exists and `filter_odds` can proceed without re-running filter by annotation.
