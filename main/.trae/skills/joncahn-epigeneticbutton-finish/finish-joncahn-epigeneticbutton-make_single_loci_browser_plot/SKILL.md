---
name: finish-joncahn-epigeneticbutton-make_single_loci_browser_plot
description: Use this skill when orchestrating the retained "make_single_loci_browser_plot" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make single loci browser plot stage tied to upstream `prep_browser_on_region` and the downstream handoff to `merge_region_browser_plots`. It tracks completion via `results/finish/make_single_loci_browser_plot.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_single_loci_browser_plot
  step_name: make single loci browser plot
---

# Scope
Use this skill only for the `make_single_loci_browser_plot` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `prep_browser_on_region`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_single_loci_browser_plot.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_single_loci_browser_plot.done`
- Representative outputs: `results/finish/make_single_loci_browser_plot.done`
- Execution targets: `make_single_loci_browser_plot`
- Downstream handoff: `merge_region_browser_plots`

## Guardrails
- Treat `results/finish/make_single_loci_browser_plot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_single_loci_browser_plot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_region_browser_plots` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_single_loci_browser_plot.done` exists and `merge_region_browser_plots` can proceed without re-running make single loci browser plot.
