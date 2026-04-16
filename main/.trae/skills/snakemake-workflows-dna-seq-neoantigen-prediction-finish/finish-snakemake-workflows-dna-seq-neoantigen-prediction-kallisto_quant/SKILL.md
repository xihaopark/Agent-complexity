---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-kallisto_quant
description: Use this skill when orchestrating the retained "kallisto_quant" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the kallisto quant stage tied to upstream `add_RNA_info` and the downstream handoff to `STAR_align`. It tracks completion via `results/finish/kallisto_quant.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: kallisto_quant
  step_name: kallisto quant
---

# Scope
Use this skill only for the `kallisto_quant` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `add_RNA_info`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/kallisto_quant.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/kallisto_quant.done`
- Representative outputs: `results/finish/kallisto_quant.done`
- Execution targets: `kallisto_quant`
- Downstream handoff: `STAR_align`

## Guardrails
- Treat `results/finish/kallisto_quant.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/kallisto_quant.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `STAR_align` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/kallisto_quant.done` exists and `STAR_align` can proceed without re-running kallisto quant.
