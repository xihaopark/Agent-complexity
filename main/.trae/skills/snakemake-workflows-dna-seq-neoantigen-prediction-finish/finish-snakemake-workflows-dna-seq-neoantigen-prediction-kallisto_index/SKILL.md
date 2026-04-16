---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-kallisto_index
description: Use this skill when orchestrating the retained "kallisto_index" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the kallisto index stage tied to upstream `get_cdna` and the downstream handoff to `get_annotation`. It tracks completion via `results/finish/kallisto_index.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: kallisto_index
  step_name: kallisto index
---

# Scope
Use this skill only for the `kallisto_index` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `get_cdna`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/kallisto_index.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/kallisto_index.done`
- Representative outputs: `results/finish/kallisto_index.done`
- Execution targets: `kallisto_index`
- Downstream handoff: `get_annotation`

## Guardrails
- Treat `results/finish/kallisto_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/kallisto_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/kallisto_index.done` exists and `get_annotation` can proceed without re-running kallisto index.
