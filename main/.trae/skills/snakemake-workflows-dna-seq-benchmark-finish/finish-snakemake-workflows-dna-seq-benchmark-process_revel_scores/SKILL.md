---
name: finish-snakemake-workflows-dna-seq-benchmark-process_revel_scores
description: Use this skill when orchestrating the retained "process_revel_scores" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the process revel scores stage tied to upstream `download_revel` and the downstream handoff to `tabix_revel_scores`. It tracks completion via `results/finish/process_revel_scores.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: process_revel_scores
  step_name: process revel scores
---

# Scope
Use this skill only for the `process_revel_scores` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `download_revel`
- Step file: `finish/dna-seq-benchmark-finish/steps/process_revel_scores.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/process_revel_scores.done`
- Representative outputs: `results/finish/process_revel_scores.done`
- Execution targets: `process_revel_scores`
- Downstream handoff: `tabix_revel_scores`

## Guardrails
- Treat `results/finish/process_revel_scores.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/process_revel_scores.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `tabix_revel_scores` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/process_revel_scores.done` exists and `tabix_revel_scores` can proceed without re-running process revel scores.
