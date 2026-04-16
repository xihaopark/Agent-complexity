---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-concat_proteome
description: Use this skill when orchestrating the retained "concat_proteome" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the concat proteome stage tied to upstream `microphaser_germline` and the downstream handoff to `build_germline_proteome`. It tracks completion via `results/finish/concat_proteome.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: concat_proteome
  step_name: concat proteome
---

# Scope
Use this skill only for the `concat_proteome` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `microphaser_germline`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/concat_proteome.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/concat_proteome.done`
- Representative outputs: `results/finish/concat_proteome.done`
- Execution targets: `concat_proteome`
- Downstream handoff: `build_germline_proteome`

## Guardrails
- Treat `results/finish/concat_proteome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/concat_proteome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `build_germline_proteome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/concat_proteome.done` exists and `build_germline_proteome` can proceed without re-running concat proteome.
