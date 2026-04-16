---
name: finish-epigen-fetch-ngs-fastq_to_bam
description: Use this skill when orchestrating the retained "fastq_to_bam" step of the epigen fetch_ngs finish finish workflow. It keeps the fastq to bam stage tied to upstream `iseq_download` and the downstream handoff to `fetch_file`. It tracks completion via `results/finish/fastq_to_bam.done`.
metadata:
  workflow_id: epigen-fetch_ngs-finish
  workflow_name: epigen fetch_ngs finish
  step_id: fastq_to_bam
  step_name: fastq to bam
---

# Scope
Use this skill only for the `fastq_to_bam` step in `epigen-fetch_ngs-finish`.

## Orchestration
- Upstream requirements: `iseq_download`
- Step file: `finish/epigen-fetch_ngs-finish/steps/fastq_to_bam.smk`
- Config file: `finish/epigen-fetch_ngs-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastq_to_bam.done`
- Representative outputs: `results/finish/fastq_to_bam.done`
- Execution targets: `fastq_to_bam`
- Downstream handoff: `fetch_file`

## Guardrails
- Treat `results/finish/fastq_to_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastq_to_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fetch_file` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastq_to_bam.done` exists and `fetch_file` can proceed without re-running fastq to bam.
