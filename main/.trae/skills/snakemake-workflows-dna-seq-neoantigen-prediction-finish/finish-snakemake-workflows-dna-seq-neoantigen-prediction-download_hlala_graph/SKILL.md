---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-download_hlala_graph
description: Use this skill when orchestrating the retained "download_HLALA_graph" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the download HLALA graph stage tied to upstream `bwa_index` and the downstream handoff to `index_HLALA`. It tracks completion via `results/finish/download_HLALA_graph.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: download_HLALA_graph
  step_name: download HLALA graph
---

# Scope
Use this skill only for the `download_HLALA_graph` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `bwa_index`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/download_HLALA_graph.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/download_HLALA_graph.done`
- Representative outputs: `results/finish/download_HLALA_graph.done`
- Execution targets: `download_HLALA_graph`
- Downstream handoff: `index_HLALA`

## Guardrails
- Treat `results/finish/download_HLALA_graph.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/download_HLALA_graph.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `index_HLALA` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/download_HLALA_graph.done` exists and `index_HLALA` can proceed without re-running download HLALA graph.
