---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-sort_calls
description: Use this skill when orchestrating the retained "sort_calls" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the sort calls stage tied to upstream `varlociraptor_call` and the downstream handoff to `bcftools_concat`. It tracks completion via `results/finish/sort_calls.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: sort_calls
  step_name: sort calls
---

# Scope
Use this skill only for the `sort_calls` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `varlociraptor_call`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/sort_calls.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sort_calls.done`
- Representative outputs: `results/finish/sort_calls.done`
- Execution targets: `sort_calls`
- Downstream handoff: `bcftools_concat`

## Guardrails
- Treat `results/finish/sort_calls.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sort_calls.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bcftools_concat` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sort_calls.done` exists and `bcftools_concat` can proceed without re-running sort calls.
