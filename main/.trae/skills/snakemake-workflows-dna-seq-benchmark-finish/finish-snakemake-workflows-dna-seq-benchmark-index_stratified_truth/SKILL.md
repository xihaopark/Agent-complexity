---
name: finish-snakemake-workflows-dna-seq-benchmark-index_stratified_truth
description: Use this skill when orchestrating the retained "index_stratified_truth" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the index stratified truth stage tied to upstream `stratify_results` and the downstream handoff to `stat_truth`. It tracks completion via `results/finish/index_stratified_truth.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: index_stratified_truth
  step_name: index stratified truth
---

# Scope
Use this skill only for the `index_stratified_truth` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `stratify_results`
- Step file: `finish/dna-seq-benchmark-finish/steps/index_stratified_truth.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/index_stratified_truth.done`
- Representative outputs: `results/finish/index_stratified_truth.done`
- Execution targets: `index_stratified_truth`
- Downstream handoff: `stat_truth`

## Guardrails
- Treat `results/finish/index_stratified_truth.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/index_stratified_truth.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `stat_truth` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/index_stratified_truth.done` exists and `stat_truth` can proceed without re-running index stratified truth.
