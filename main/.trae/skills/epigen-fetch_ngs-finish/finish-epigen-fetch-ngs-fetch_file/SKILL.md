---
name: finish-epigen-fetch-ngs-fetch_file
description: Use this skill when orchestrating the retained "fetch_file" step of the epigen fetch_ngs finish finish workflow. It keeps the fetch file stage tied to upstream `fastq_to_bam` and the downstream handoff to `merge_metadata`. It tracks completion via `results/finish/fetch_file.done`.
metadata:
  workflow_id: epigen-fetch_ngs-finish
  workflow_name: epigen fetch_ngs finish
  step_id: fetch_file
  step_name: fetch file
---

# Scope
Use this skill only for the `fetch_file` step in `epigen-fetch_ngs-finish`.

## Orchestration
- Upstream requirements: `fastq_to_bam`
- Step file: `finish/epigen-fetch_ngs-finish/steps/fetch_file.smk`
- Config file: `finish/epigen-fetch_ngs-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fetch_file.done`
- Representative outputs: `results/finish/fetch_file.done`
- Execution targets: `fetch_file`
- Downstream handoff: `merge_metadata`

## Guardrails
- Treat `results/finish/fetch_file.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fetch_file.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_metadata` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fetch_file.done` exists and `merge_metadata` can proceed without re-running fetch file.
