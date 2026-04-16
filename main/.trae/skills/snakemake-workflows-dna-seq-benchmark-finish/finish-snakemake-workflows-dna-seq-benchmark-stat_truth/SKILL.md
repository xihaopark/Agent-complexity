---
name: finish-snakemake-workflows-dna-seq-benchmark-stat_truth
description: Use this skill when orchestrating the retained "stat_truth" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the stat truth stage tied to upstream `index_stratified_truth` and the downstream handoff to `generate_sdf`. It tracks completion via `results/finish/stat_truth.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: stat_truth
  step_name: stat truth
---

# Scope
Use this skill only for the `stat_truth` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `index_stratified_truth`
- Step file: `finish/dna-seq-benchmark-finish/steps/stat_truth.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/stat_truth.done`
- Representative outputs: `results/finish/stat_truth.done`
- Execution targets: `stat_truth`
- Downstream handoff: `generate_sdf`

## Guardrails
- Treat `results/finish/stat_truth.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/stat_truth.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `generate_sdf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/stat_truth.done` exists and `generate_sdf` can proceed without re-running stat truth.
