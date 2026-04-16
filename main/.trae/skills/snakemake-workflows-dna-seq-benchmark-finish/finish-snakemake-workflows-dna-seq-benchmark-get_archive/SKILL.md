---
name: finish-snakemake-workflows-dna-seq-benchmark-get_archive
description: Use this skill when orchestrating the retained "get_archive" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the get archive stage tied to upstream `get_reads` and the downstream handoff to `get_truth`. It tracks completion via `results/finish/get_archive.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: get_archive
  step_name: get archive
---

# Scope
Use this skill only for the `get_archive` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `get_reads`
- Step file: `finish/dna-seq-benchmark-finish/steps/get_archive.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_archive.done`
- Representative outputs: `results/finish/get_archive.done`
- Execution targets: `get_archive`
- Downstream handoff: `get_truth`

## Guardrails
- Treat `results/finish/get_archive.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_archive.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_truth` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_archive.done` exists and `get_truth` can proceed without re-running get archive.
