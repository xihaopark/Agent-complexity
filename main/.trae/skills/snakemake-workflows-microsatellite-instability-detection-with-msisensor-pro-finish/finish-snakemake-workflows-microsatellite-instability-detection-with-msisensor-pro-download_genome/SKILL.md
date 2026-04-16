---
name: finish-snakemake-workflows-microsatellite-instability-detection-with-msisensor-pro-download_genome
description: Use this skill when orchestrating the retained "download_genome" step of the snakemake workflows microsatellite instability detection with msisensor pro finish finish workflow. It keeps the download genome stage tied to upstream `samtools_index` and the downstream handoff to `msisensor_pro_scan`. It tracks completion via `results/finish/download_genome.done`.
metadata:
  workflow_id: microsatellite-instability-detection-with-msisensor-pro-finish
  workflow_name: snakemake workflows microsatellite instability detection with msisensor pro finish
  step_id: download_genome
  step_name: download genome
---

# Scope
Use this skill only for the `download_genome` step in `microsatellite-instability-detection-with-msisensor-pro-finish`.

## Orchestration
- Upstream requirements: `samtools_index`
- Step file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/steps/download_genome.smk`
- Config file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/download_genome.done`
- Representative outputs: `results/finish/download_genome.done`
- Execution targets: `download_genome`
- Downstream handoff: `msisensor_pro_scan`

## Guardrails
- Treat `results/finish/download_genome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/download_genome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `msisensor_pro_scan` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/download_genome.done` exists and `msisensor_pro_scan` can proceed without re-running download genome.
