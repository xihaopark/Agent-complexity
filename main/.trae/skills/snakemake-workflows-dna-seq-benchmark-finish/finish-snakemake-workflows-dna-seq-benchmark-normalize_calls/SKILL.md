---
name: finish-snakemake-workflows-dna-seq-benchmark-normalize_calls
description: Use this skill when orchestrating the retained "normalize_calls" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the normalize calls stage tied to upstream `restrict_to_reference_contigs` and the downstream handoff to `stratify_truth`. It tracks completion via `results/finish/normalize_calls.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: normalize_calls
  step_name: normalize calls
---

# Scope
Use this skill only for the `normalize_calls` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `restrict_to_reference_contigs`
- Step file: `finish/dna-seq-benchmark-finish/steps/normalize_calls.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/normalize_calls.done`
- Representative outputs: `results/finish/normalize_calls.done`
- Execution targets: `normalize_calls`
- Downstream handoff: `stratify_truth`

## Guardrails
- Treat `results/finish/normalize_calls.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/normalize_calls.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `stratify_truth` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/normalize_calls.done` exists and `stratify_truth` can proceed without re-running normalize calls.
