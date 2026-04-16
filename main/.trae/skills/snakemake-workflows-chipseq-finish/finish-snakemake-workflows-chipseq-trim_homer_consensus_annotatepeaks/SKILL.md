---
name: finish-snakemake-workflows-chipseq-trim_homer_consensus_annotatepeaks
description: Use this skill when orchestrating the retained "trim_homer_consensus_annotatepeaks" step of the snakemake workflows chipseq finish finish workflow. It keeps the trim homer consensus annotatepeaks stage tied to upstream `homer_consensus_annotatepeaks` and the downstream handoff to `merge_bool_and_annotatepeaks`. It tracks completion via `results/finish/trim_homer_consensus_annotatepeaks.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: trim_homer_consensus_annotatepeaks
  step_name: trim homer consensus annotatepeaks
---

# Scope
Use this skill only for the `trim_homer_consensus_annotatepeaks` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `homer_consensus_annotatepeaks`
- Step file: `finish/chipseq-finish/steps/trim_homer_consensus_annotatepeaks.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/trim_homer_consensus_annotatepeaks.done`
- Representative outputs: `results/finish/trim_homer_consensus_annotatepeaks.done`
- Execution targets: `trim_homer_consensus_annotatepeaks`
- Downstream handoff: `merge_bool_and_annotatepeaks`

## Guardrails
- Treat `results/finish/trim_homer_consensus_annotatepeaks.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/trim_homer_consensus_annotatepeaks.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_bool_and_annotatepeaks` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/trim_homer_consensus_annotatepeaks.done` exists and `merge_bool_and_annotatepeaks` can proceed without re-running trim homer consensus annotatepeaks.
