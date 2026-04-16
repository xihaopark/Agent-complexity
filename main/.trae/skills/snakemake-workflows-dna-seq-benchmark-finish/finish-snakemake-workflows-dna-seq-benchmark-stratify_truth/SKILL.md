---
name: finish-snakemake-workflows-dna-seq-benchmark-stratify_truth
description: Use this skill when orchestrating the retained "stratify_truth" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the stratify truth stage tied to upstream `normalize_calls` and the downstream handoff to `stratify_results`. It tracks completion via `results/finish/stratify_truth.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: stratify_truth
  step_name: stratify truth
---

# Scope
Use this skill only for the `stratify_truth` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `normalize_calls`
- Step file: `finish/dna-seq-benchmark-finish/steps/stratify_truth.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/stratify_truth.done`
- Representative outputs: `results/finish/stratify_truth.done`
- Execution targets: `stratify_truth`
- Downstream handoff: `stratify_results`

## Guardrails
- Treat `results/finish/stratify_truth.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/stratify_truth.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `stratify_results` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/stratify_truth.done` exists and `stratify_results` can proceed without re-running stratify truth.
