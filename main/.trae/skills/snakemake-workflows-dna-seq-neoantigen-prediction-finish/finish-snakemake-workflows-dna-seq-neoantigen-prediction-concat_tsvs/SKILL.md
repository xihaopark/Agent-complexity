---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-concat_tsvs
description: Use this skill when orchestrating the retained "concat_tsvs" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the concat tsvs stage tied to upstream `microphaser_filter` and the downstream handoff to `HLA_LA`. It tracks completion via `results/finish/concat_tsvs.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: concat_tsvs
  step_name: concat tsvs
---

# Scope
Use this skill only for the `concat_tsvs` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `microphaser_filter`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/concat_tsvs.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/concat_tsvs.done`
- Representative outputs: `results/finish/concat_tsvs.done`
- Execution targets: `concat_tsvs`
- Downstream handoff: `HLA_LA`

## Guardrails
- Treat `results/finish/concat_tsvs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/concat_tsvs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `HLA_LA` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/concat_tsvs.done` exists and `HLA_LA` can proceed without re-running concat tsvs.
