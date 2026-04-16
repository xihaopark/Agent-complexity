---
name: finish-snakemake-workflows-chipseq-create_consensus_igv
description: Use this skill when orchestrating the retained "create_consensus_igv" step of the snakemake workflows chipseq finish finish workflow. It keeps the create consensus igv stage tied to upstream `plot_peak_intersect` and the downstream handoff to `homer_consensus_annotatepeaks`. It tracks completion via `results/finish/create_consensus_igv.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: create_consensus_igv
  step_name: create consensus igv
---

# Scope
Use this skill only for the `create_consensus_igv` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `plot_peak_intersect`
- Step file: `finish/chipseq-finish/steps/create_consensus_igv.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_consensus_igv.done`
- Representative outputs: `results/finish/create_consensus_igv.done`
- Execution targets: `create_consensus_igv`
- Downstream handoff: `homer_consensus_annotatepeaks`

## Guardrails
- Treat `results/finish/create_consensus_igv.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_consensus_igv.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `homer_consensus_annotatepeaks` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_consensus_igv.done` exists and `homer_consensus_annotatepeaks` can proceed without re-running create consensus igv.
