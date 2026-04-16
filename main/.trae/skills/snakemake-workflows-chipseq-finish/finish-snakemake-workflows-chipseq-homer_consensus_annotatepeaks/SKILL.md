---
name: finish-snakemake-workflows-chipseq-homer_consensus_annotatepeaks
description: Use this skill when orchestrating the retained "homer_consensus_annotatepeaks" step of the snakemake workflows chipseq finish finish workflow. It keeps the homer consensus annotatepeaks stage tied to upstream `create_consensus_igv` and the downstream handoff to `trim_homer_consensus_annotatepeaks`. It tracks completion via `results/finish/homer_consensus_annotatepeaks.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: homer_consensus_annotatepeaks
  step_name: homer consensus annotatepeaks
---

# Scope
Use this skill only for the `homer_consensus_annotatepeaks` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `create_consensus_igv`
- Step file: `finish/chipseq-finish/steps/homer_consensus_annotatepeaks.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/homer_consensus_annotatepeaks.done`
- Representative outputs: `results/finish/homer_consensus_annotatepeaks.done`
- Execution targets: `homer_consensus_annotatepeaks`
- Downstream handoff: `trim_homer_consensus_annotatepeaks`

## Guardrails
- Treat `results/finish/homer_consensus_annotatepeaks.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/homer_consensus_annotatepeaks.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `trim_homer_consensus_annotatepeaks` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/homer_consensus_annotatepeaks.done` exists and `trim_homer_consensus_annotatepeaks` can proceed without re-running homer consensus annotatepeaks.
