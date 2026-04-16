---
name: finish-snakemake-workflows-dna-seq-benchmark-get_truth
description: Use this skill when orchestrating the retained "get_truth" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the get truth stage tied to upstream `get_archive` and the downstream handoff to `rename_truth_contigs`. It tracks completion via `results/finish/get_truth.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: get_truth
  step_name: get truth
---

# Scope
Use this skill only for the `get_truth` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `get_archive`
- Step file: `finish/dna-seq-benchmark-finish/steps/get_truth.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_truth.done`
- Representative outputs: `results/finish/get_truth.done`
- Execution targets: `get_truth`
- Downstream handoff: `rename_truth_contigs`

## Guardrails
- Treat `results/finish/get_truth.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_truth.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rename_truth_contigs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_truth.done` exists and `rename_truth_contigs` can proceed without re-running get truth.
