---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-bwa_index
description: Use this skill when orchestrating the retained "bwa_index" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the bwa index stage tied to upstream `remove_iupac_codes` and the downstream handoff to `download_HLALA_graph`. It tracks completion via `results/finish/bwa_index.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: bwa_index
  step_name: bwa index
---

# Scope
Use this skill only for the `bwa_index` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `remove_iupac_codes`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/bwa_index.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_index.done`
- Representative outputs: `results/finish/bwa_index.done`
- Execution targets: `bwa_index`
- Downstream handoff: `download_HLALA_graph`

## Guardrails
- Treat `results/finish/bwa_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `download_HLALA_graph` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_index.done` exists and `download_HLALA_graph` can proceed without re-running bwa index.
