---
name: finish-snakemake-workflows-chipseq-plot_fingerprint
description: Use this skill when orchestrating the retained "plot_fingerprint" step of the snakemake workflows chipseq finish finish workflow. It keeps the plot fingerprint stage tied to upstream `phantompeak_multiqc` and the downstream handoff to `macs2_callpeak_broad`. It tracks completion via `results/finish/plot_fingerprint.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: plot_fingerprint
  step_name: plot fingerprint
---

# Scope
Use this skill only for the `plot_fingerprint` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `phantompeak_multiqc`
- Step file: `finish/chipseq-finish/steps/plot_fingerprint.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_fingerprint.done`
- Representative outputs: `results/finish/plot_fingerprint.done`
- Execution targets: `plot_fingerprint`
- Downstream handoff: `macs2_callpeak_broad`

## Guardrails
- Treat `results/finish/plot_fingerprint.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_fingerprint.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `macs2_callpeak_broad` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_fingerprint.done` exists and `macs2_callpeak_broad` can proceed without re-running plot fingerprint.
