---
name: finish-snakemake-workflows-chipseq-phantompeakqualtools
description: Use this skill when orchestrating the retained "phantompeakqualtools" step of the snakemake workflows chipseq finish finish workflow. It keeps the phantompeakqualtools stage tied to upstream `plot_heatmap` and the downstream handoff to `phantompeak_correlation`. It tracks completion via `results/finish/phantompeakqualtools.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: phantompeakqualtools
  step_name: phantompeakqualtools
---

# Scope
Use this skill only for the `phantompeakqualtools` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `plot_heatmap`
- Step file: `finish/chipseq-finish/steps/phantompeakqualtools.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/phantompeakqualtools.done`
- Representative outputs: `results/finish/phantompeakqualtools.done`
- Execution targets: `phantompeakqualtools`
- Downstream handoff: `phantompeak_correlation`

## Guardrails
- Treat `results/finish/phantompeakqualtools.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/phantompeakqualtools.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `phantompeak_correlation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/phantompeakqualtools.done` exists and `phantompeak_correlation` can proceed without re-running phantompeakqualtools.
