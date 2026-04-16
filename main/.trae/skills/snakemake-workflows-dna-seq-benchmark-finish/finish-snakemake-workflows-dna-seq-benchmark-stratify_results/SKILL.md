---
name: finish-snakemake-workflows-dna-seq-benchmark-stratify_results
description: Use this skill when orchestrating the retained "stratify_results" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the stratify results stage tied to upstream `stratify_truth` and the downstream handoff to `index_stratified_truth`. It tracks completion via `results/finish/stratify_results.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: stratify_results
  step_name: stratify results
---

# Scope
Use this skill only for the `stratify_results` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `stratify_truth`
- Step file: `finish/dna-seq-benchmark-finish/steps/stratify_results.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/stratify_results.done`
- Representative outputs: `results/finish/stratify_results.done`
- Execution targets: `stratify_results`
- Downstream handoff: `index_stratified_truth`

## Guardrails
- Treat `results/finish/stratify_results.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/stratify_results.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `index_stratified_truth` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/stratify_results.done` exists and `index_stratified_truth` can proceed without re-running stratify results.
