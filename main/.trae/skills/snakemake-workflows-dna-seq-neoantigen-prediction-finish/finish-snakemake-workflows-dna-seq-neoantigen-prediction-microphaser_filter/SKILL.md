---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-microphaser_filter
description: Use this skill when orchestrating the retained "microphaser_filter" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the microphaser filter stage tied to upstream `build_germline_proteome` and the downstream handoff to `concat_tsvs`. It tracks completion via `results/finish/microphaser_filter.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: microphaser_filter
  step_name: microphaser filter
---

# Scope
Use this skill only for the `microphaser_filter` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `build_germline_proteome`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/microphaser_filter.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/microphaser_filter.done`
- Representative outputs: `results/finish/microphaser_filter.done`
- Execution targets: `microphaser_filter`
- Downstream handoff: `concat_tsvs`

## Guardrails
- Treat `results/finish/microphaser_filter.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/microphaser_filter.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `concat_tsvs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/microphaser_filter.done` exists and `concat_tsvs` can proceed without re-running microphaser filter.
