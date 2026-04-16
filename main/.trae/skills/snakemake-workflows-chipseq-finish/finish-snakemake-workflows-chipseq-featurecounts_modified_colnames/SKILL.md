---
name: finish-snakemake-workflows-chipseq-featurecounts_modified_colnames
description: Use this skill when orchestrating the retained "featurecounts_modified_colnames" step of the snakemake workflows chipseq finish finish workflow. It keeps the featurecounts modified colnames stage tied to upstream `feature_counts` and the downstream handoff to `featurecounts_deseq2`. It tracks completion via `results/finish/featurecounts_modified_colnames.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: featurecounts_modified_colnames
  step_name: featurecounts modified colnames
---

# Scope
Use this skill only for the `featurecounts_modified_colnames` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `feature_counts`
- Step file: `finish/chipseq-finish/steps/featurecounts_modified_colnames.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/featurecounts_modified_colnames.done`
- Representative outputs: `results/finish/featurecounts_modified_colnames.done`
- Execution targets: `featurecounts_modified_colnames`
- Downstream handoff: `featurecounts_deseq2`

## Guardrails
- Treat `results/finish/featurecounts_modified_colnames.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/featurecounts_modified_colnames.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `featurecounts_deseq2` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/featurecounts_modified_colnames.done` exists and `featurecounts_deseq2` can proceed without re-running featurecounts modified colnames.
