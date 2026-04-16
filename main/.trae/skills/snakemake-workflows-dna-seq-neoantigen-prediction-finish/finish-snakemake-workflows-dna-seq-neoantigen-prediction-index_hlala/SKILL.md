---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-index_hlala
description: Use this skill when orchestrating the retained "index_HLALA" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the index HLALA stage tied to upstream `download_HLALA_graph` and the downstream handoff to `get_vep_cache`. It tracks completion via `results/finish/index_HLALA.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: index_HLALA
  step_name: index HLALA
---

# Scope
Use this skill only for the `index_HLALA` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `download_HLALA_graph`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/index_HLALA.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/index_HLALA.done`
- Representative outputs: `results/finish/index_HLALA.done`
- Execution targets: `index_HLALA`
- Downstream handoff: `get_vep_cache`

## Guardrails
- Treat `results/finish/index_HLALA.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/index_HLALA.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_vep_cache` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/index_HLALA.done` exists and `get_vep_cache` can proceed without re-running index HLALA.
