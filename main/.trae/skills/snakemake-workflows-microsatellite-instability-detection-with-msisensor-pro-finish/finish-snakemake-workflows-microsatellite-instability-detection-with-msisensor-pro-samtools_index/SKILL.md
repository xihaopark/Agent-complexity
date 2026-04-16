---
name: finish-snakemake-workflows-microsatellite-instability-detection-with-msisensor-pro-samtools_index
description: Use this skill when orchestrating the retained "samtools_index" step of the snakemake workflows microsatellite instability detection with msisensor pro finish finish workflow. It keeps the samtools index stage and the downstream handoff to `download_genome`. It tracks completion via `results/finish/samtools_index.done`.
metadata:
  workflow_id: microsatellite-instability-detection-with-msisensor-pro-finish
  workflow_name: snakemake workflows microsatellite instability detection with msisensor pro finish
  step_id: samtools_index
  step_name: samtools index
---

# Scope
Use this skill only for the `samtools_index` step in `microsatellite-instability-detection-with-msisensor-pro-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/steps/samtools_index.smk`
- Config file: `finish/microsatellite-instability-detection-with-msisensor-pro-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_index.done`
- Representative outputs: `results/finish/samtools_index.done`
- Execution targets: `samtools_index`
- Downstream handoff: `download_genome`

## Guardrails
- Treat `results/finish/samtools_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `download_genome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_index.done` exists and `download_genome` can proceed without re-running samtools index.
