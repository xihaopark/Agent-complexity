---
name: finish-mckellardw-slide-snake-ilmn_3u_plot_qc
description: Use this skill when orchestrating the retained "ilmn_3u_plot_qc" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3u plot qc stage tied to upstream `ilmn_3u_gzip_counts` and the downstream handoff to `ilmn_4a_kbpython_std`. It tracks completion via `results/finish/ilmn_3u_plot_qc.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3u_plot_qc
  step_name: ilmn 3u plot qc
---

# Scope
Use this skill only for the `ilmn_3u_plot_qc` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_3u_gzip_counts`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3u_plot_qc.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3u_plot_qc.done`
- Representative outputs: `results/finish/ilmn_3u_plot_qc.done`
- Execution targets: `ilmn_3u_plot_qc`
- Downstream handoff: `ilmn_4a_kbpython_std`

## Guardrails
- Treat `results/finish/ilmn_3u_plot_qc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3u_plot_qc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_4a_kbpython_std` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3u_plot_qc.done` exists and `ilmn_4a_kbpython_std` can proceed without re-running ilmn 3u plot qc.
