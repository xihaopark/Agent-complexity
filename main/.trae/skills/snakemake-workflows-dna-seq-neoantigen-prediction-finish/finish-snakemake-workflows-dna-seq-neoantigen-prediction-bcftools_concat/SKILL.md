---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-bcftools_concat
description: Use this skill when orchestrating the retained "bcftools_concat" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the bcftools concat stage tied to upstream `sort_calls` and the downstream handoff to `annotate_variants`. It tracks completion via `results/finish/bcftools_concat.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: bcftools_concat
  step_name: bcftools concat
---

# Scope
Use this skill only for the `bcftools_concat` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `sort_calls`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/bcftools_concat.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bcftools_concat.done`
- Representative outputs: `results/finish/bcftools_concat.done`
- Execution targets: `bcftools_concat`
- Downstream handoff: `annotate_variants`

## Guardrails
- Treat `results/finish/bcftools_concat.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bcftools_concat.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annotate_variants` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bcftools_concat.done` exists and `annotate_variants` can proceed without re-running bcftools concat.
