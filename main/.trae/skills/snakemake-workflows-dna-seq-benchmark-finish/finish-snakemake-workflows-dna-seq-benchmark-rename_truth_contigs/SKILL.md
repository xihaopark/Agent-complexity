---
name: finish-snakemake-workflows-dna-seq-benchmark-rename_truth_contigs
description: Use this skill when orchestrating the retained "rename_truth_contigs" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the rename truth contigs stage tied to upstream `get_truth` and the downstream handoff to `merge_truthsets`. It tracks completion via `results/finish/rename_truth_contigs.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: rename_truth_contigs
  step_name: rename truth contigs
---

# Scope
Use this skill only for the `rename_truth_contigs` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `get_truth`
- Step file: `finish/dna-seq-benchmark-finish/steps/rename_truth_contigs.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rename_truth_contigs.done`
- Representative outputs: `results/finish/rename_truth_contigs.done`
- Execution targets: `rename_truth_contigs`
- Downstream handoff: `merge_truthsets`

## Guardrails
- Treat `results/finish/rename_truth_contigs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rename_truth_contigs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_truthsets` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rename_truth_contigs.done` exists and `merge_truthsets` can proceed without re-running rename truth contigs.
