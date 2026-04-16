---
name: finish-snakemake-workflows-dna-seq-benchmark-merge_truthsets
description: Use this skill when orchestrating the retained "merge_truthsets" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the merge truthsets stage tied to upstream `rename_truth_contigs` and the downstream handoff to `normalize_truth`. It tracks completion via `results/finish/merge_truthsets.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: merge_truthsets
  step_name: merge truthsets
---

# Scope
Use this skill only for the `merge_truthsets` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `rename_truth_contigs`
- Step file: `finish/dna-seq-benchmark-finish/steps/merge_truthsets.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_truthsets.done`
- Representative outputs: `results/finish/merge_truthsets.done`
- Execution targets: `merge_truthsets`
- Downstream handoff: `normalize_truth`

## Guardrails
- Treat `results/finish/merge_truthsets.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_truthsets.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `normalize_truth` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_truthsets.done` exists and `normalize_truth` can proceed without re-running merge truthsets.
