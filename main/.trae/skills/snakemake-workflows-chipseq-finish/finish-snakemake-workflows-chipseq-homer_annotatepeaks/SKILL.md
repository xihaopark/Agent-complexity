---
name: finish-snakemake-workflows-chipseq-homer_annotatepeaks
description: Use this skill when orchestrating the retained "homer_annotatepeaks" step of the snakemake workflows chipseq finish finish workflow. It keeps the homer annotatepeaks stage tied to upstream `create_igv_peaks` and the downstream handoff to `plot_macs_qc`. It tracks completion via `results/finish/homer_annotatepeaks.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: homer_annotatepeaks
  step_name: homer annotatepeaks
---

# Scope
Use this skill only for the `homer_annotatepeaks` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `create_igv_peaks`
- Step file: `finish/chipseq-finish/steps/homer_annotatepeaks.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/homer_annotatepeaks.done`
- Representative outputs: `results/finish/homer_annotatepeaks.done`
- Execution targets: `homer_annotatepeaks`
- Downstream handoff: `plot_macs_qc`

## Guardrails
- Treat `results/finish/homer_annotatepeaks.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/homer_annotatepeaks.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_macs_qc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/homer_annotatepeaks.done` exists and `plot_macs_qc` can proceed without re-running homer annotatepeaks.
