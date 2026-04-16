---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-get_vep_cache
description: Use this skill when orchestrating the retained "get_vep_cache" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the get vep cache stage tied to upstream `index_HLALA` and the downstream handoff to `get_vep_plugins`. It tracks completion via `results/finish/get_vep_cache.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: get_vep_cache
  step_name: get vep cache
---

# Scope
Use this skill only for the `get_vep_cache` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `index_HLALA`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/get_vep_cache.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_vep_cache.done`
- Representative outputs: `results/finish/get_vep_cache.done`
- Execution targets: `get_vep_cache`
- Downstream handoff: `get_vep_plugins`

## Guardrails
- Treat `results/finish/get_vep_cache.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_vep_cache.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_vep_plugins` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_vep_cache.done` exists and `get_vep_plugins` can proceed without re-running get vep cache.
