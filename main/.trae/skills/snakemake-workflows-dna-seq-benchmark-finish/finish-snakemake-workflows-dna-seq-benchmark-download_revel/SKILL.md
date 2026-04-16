---
name: finish-snakemake-workflows-dna-seq-benchmark-download_revel
description: Use this skill when orchestrating the retained "download_revel" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the download revel stage tied to upstream `get_vep_plugins` and the downstream handoff to `process_revel_scores`. It tracks completion via `results/finish/download_revel.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: download_revel
  step_name: download revel
---

# Scope
Use this skill only for the `download_revel` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `get_vep_plugins`
- Step file: `finish/dna-seq-benchmark-finish/steps/download_revel.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/download_revel.done`
- Representative outputs: `results/finish/download_revel.done`
- Execution targets: `download_revel`
- Downstream handoff: `process_revel_scores`

## Guardrails
- Treat `results/finish/download_revel.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/download_revel.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `process_revel_scores` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/download_revel.done` exists and `process_revel_scores` can proceed without re-running download revel.
