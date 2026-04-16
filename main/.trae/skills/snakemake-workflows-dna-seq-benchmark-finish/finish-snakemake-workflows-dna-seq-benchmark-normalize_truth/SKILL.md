---
name: finish-snakemake-workflows-dna-seq-benchmark-normalize_truth
description: Use this skill when orchestrating the retained "normalize_truth" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the normalize truth stage tied to upstream `merge_truthsets` and the downstream handoff to `get_confidence_bed`. It tracks completion via `results/finish/normalize_truth.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: normalize_truth
  step_name: normalize truth
---

# Scope
Use this skill only for the `normalize_truth` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `merge_truthsets`
- Step file: `finish/dna-seq-benchmark-finish/steps/normalize_truth.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/normalize_truth.done`
- Representative outputs: `results/finish/normalize_truth.done`
- Execution targets: `normalize_truth`
- Downstream handoff: `get_confidence_bed`

## Guardrails
- Treat `results/finish/normalize_truth.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/normalize_truth.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_confidence_bed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/normalize_truth.done` exists and `get_confidence_bed` can proceed without re-running normalize truth.
