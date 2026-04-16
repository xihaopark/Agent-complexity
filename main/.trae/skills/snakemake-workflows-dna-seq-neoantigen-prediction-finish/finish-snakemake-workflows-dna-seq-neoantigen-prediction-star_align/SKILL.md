---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-star_align
description: Use this skill when orchestrating the retained "STAR_align" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the STAR align stage tied to upstream `kallisto_quant` and the downstream handoff to `arriba`. It tracks completion via `results/finish/STAR_align.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: STAR_align
  step_name: STAR align
---

# Scope
Use this skill only for the `STAR_align` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `kallisto_quant`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/STAR_align.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/STAR_align.done`
- Representative outputs: `results/finish/STAR_align.done`
- Execution targets: `STAR_align`
- Downstream handoff: `arriba`

## Guardrails
- Treat `results/finish/STAR_align.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/STAR_align.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `arriba` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/STAR_align.done` exists and `arriba` can proceed without re-running STAR align.
