---
name: finish-snakemake-workflows-chipseq-feature_counts
description: Use this skill when orchestrating the retained "feature_counts" step of the snakemake workflows chipseq finish finish workflow. It keeps the feature counts stage tied to upstream `merge_bool_and_annotatepeaks` and the downstream handoff to `featurecounts_modified_colnames`. It tracks completion via `results/finish/feature_counts.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: feature_counts
  step_name: feature counts
---

# Scope
Use this skill only for the `feature_counts` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `merge_bool_and_annotatepeaks`
- Step file: `finish/chipseq-finish/steps/feature_counts.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/feature_counts.done`
- Representative outputs: `results/finish/feature_counts.done`
- Execution targets: `feature_counts`
- Downstream handoff: `featurecounts_modified_colnames`

## Guardrails
- Treat `results/finish/feature_counts.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/feature_counts.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `featurecounts_modified_colnames` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/feature_counts.done` exists and `featurecounts_modified_colnames` can proceed without re-running feature counts.
