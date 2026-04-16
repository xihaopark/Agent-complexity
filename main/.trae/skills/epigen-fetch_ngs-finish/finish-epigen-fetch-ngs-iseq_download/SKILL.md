---
name: finish-epigen-fetch-ngs-iseq_download
description: Use this skill when orchestrating the retained "iseq_download" step of the epigen fetch_ngs finish finish workflow. It keeps the iseq download stage tied to upstream `config_export` and the downstream handoff to `fastq_to_bam`. It tracks completion via `results/finish/iseq_download.done`.
metadata:
  workflow_id: epigen-fetch_ngs-finish
  workflow_name: epigen fetch_ngs finish
  step_id: iseq_download
  step_name: iseq download
---

# Scope
Use this skill only for the `iseq_download` step in `epigen-fetch_ngs-finish`.

## Orchestration
- Upstream requirements: `config_export`
- Step file: `finish/epigen-fetch_ngs-finish/steps/iseq_download.smk`
- Config file: `finish/epigen-fetch_ngs-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/iseq_download.done`
- Representative outputs: `results/finish/iseq_download.done`
- Execution targets: `iseq_download`
- Downstream handoff: `fastq_to_bam`

## Guardrails
- Treat `results/finish/iseq_download.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/iseq_download.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastq_to_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/iseq_download.done` exists and `fastq_to_bam` can proceed without re-running iseq download.
