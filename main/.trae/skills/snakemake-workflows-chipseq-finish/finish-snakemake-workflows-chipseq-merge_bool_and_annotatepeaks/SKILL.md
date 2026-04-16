---
name: finish-snakemake-workflows-chipseq-merge_bool_and_annotatepeaks
description: Use this skill when orchestrating the retained "merge_bool_and_annotatepeaks" step of the snakemake workflows chipseq finish finish workflow. It keeps the merge bool and annotatepeaks stage tied to upstream `trim_homer_consensus_annotatepeaks` and the downstream handoff to `feature_counts`. It tracks completion via `results/finish/merge_bool_and_annotatepeaks.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: merge_bool_and_annotatepeaks
  step_name: merge bool and annotatepeaks
---

# Scope
Use this skill only for the `merge_bool_and_annotatepeaks` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `trim_homer_consensus_annotatepeaks`
- Step file: `finish/chipseq-finish/steps/merge_bool_and_annotatepeaks.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_bool_and_annotatepeaks.done`
- Representative outputs: `results/finish/merge_bool_and_annotatepeaks.done`
- Execution targets: `merge_bool_and_annotatepeaks`
- Downstream handoff: `feature_counts`

## Guardrails
- Treat `results/finish/merge_bool_and_annotatepeaks.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_bool_and_annotatepeaks.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `feature_counts` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_bool_and_annotatepeaks.done` exists and `feature_counts` can proceed without re-running merge bool and annotatepeaks.
