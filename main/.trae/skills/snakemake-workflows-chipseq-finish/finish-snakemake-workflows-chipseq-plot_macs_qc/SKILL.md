---
name: finish-snakemake-workflows-chipseq-plot_macs_qc
description: Use this skill when orchestrating the retained "plot_macs_qc" step of the snakemake workflows chipseq finish finish workflow. It keeps the plot macs qc stage tied to upstream `homer_annotatepeaks` and the downstream handoff to `plot_homer_annotatepeaks`. It tracks completion via `results/finish/plot_macs_qc.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: plot_macs_qc
  step_name: plot macs qc
---

# Scope
Use this skill only for the `plot_macs_qc` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `homer_annotatepeaks`
- Step file: `finish/chipseq-finish/steps/plot_macs_qc.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_macs_qc.done`
- Representative outputs: `results/finish/plot_macs_qc.done`
- Execution targets: `plot_macs_qc`
- Downstream handoff: `plot_homer_annotatepeaks`

## Guardrails
- Treat `results/finish/plot_macs_qc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_macs_qc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_homer_annotatepeaks` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_macs_qc.done` exists and `plot_homer_annotatepeaks` can proceed without re-running plot macs qc.
