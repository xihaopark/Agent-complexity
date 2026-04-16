---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-get_annotation
description: Use this skill when orchestrating the retained "get_annotation" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the get annotation stage tied to upstream `kallisto_index` and the downstream handoff to `STAR_index`. It tracks completion via `results/finish/get_annotation.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: get_annotation
  step_name: get annotation
---

# Scope
Use this skill only for the `get_annotation` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `kallisto_index`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/get_annotation.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_annotation.done`
- Representative outputs: `results/finish/get_annotation.done`
- Execution targets: `get_annotation`
- Downstream handoff: `STAR_index`

## Guardrails
- Treat `results/finish/get_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `STAR_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_annotation.done` exists and `STAR_index` can proceed without re-running get annotation.
