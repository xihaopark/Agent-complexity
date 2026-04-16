---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-hla_la
description: Use this skill when orchestrating the retained "HLA_LA" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the HLA LA stage tied to upstream `concat_tsvs` and the downstream handoff to `parse_HLA_LA`. It tracks completion via `results/finish/HLA_LA.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: HLA_LA
  step_name: HLA LA
---

# Scope
Use this skill only for the `HLA_LA` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `concat_tsvs`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/HLA_LA.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/HLA_LA.done`
- Representative outputs: `results/finish/HLA_LA.done`
- Execution targets: `HLA_LA`
- Downstream handoff: `parse_HLA_LA`

## Guardrails
- Treat `results/finish/HLA_LA.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/HLA_LA.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `parse_HLA_LA` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/HLA_LA.done` exists and `parse_HLA_LA` can proceed without re-running HLA LA.
