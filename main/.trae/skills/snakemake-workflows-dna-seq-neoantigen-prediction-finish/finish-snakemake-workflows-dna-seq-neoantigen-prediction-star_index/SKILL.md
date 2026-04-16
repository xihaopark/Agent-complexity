---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-star_index
description: Use this skill when orchestrating the retained "STAR_index" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the STAR index stage tied to upstream `get_annotation` and the downstream handoff to `split_annotation`. It tracks completion via `results/finish/STAR_index.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: STAR_index
  step_name: STAR index
---

# Scope
Use this skill only for the `STAR_index` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `get_annotation`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/STAR_index.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/STAR_index.done`
- Representative outputs: `results/finish/STAR_index.done`
- Execution targets: `STAR_index`
- Downstream handoff: `split_annotation`

## Guardrails
- Treat `results/finish/STAR_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/STAR_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `split_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/STAR_index.done` exists and `split_annotation` can proceed without re-running STAR index.
