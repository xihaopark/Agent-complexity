---
name: finish-joncahn-epigeneticbutton-prep_browser_on_region
description: Use this skill when orchestrating the retained "prep_browser_on_region" step of the joncahn epigeneticbutton finish finish workflow. It keeps the prep browser on region stage tied to upstream `prep_chromosomes_for_browser` and the downstream handoff to `make_single_loci_browser_plot`. It tracks completion via `results/finish/prep_browser_on_region.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: prep_browser_on_region
  step_name: prep browser on region
---

# Scope
Use this skill only for the `prep_browser_on_region` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `prep_chromosomes_for_browser`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/prep_browser_on_region.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prep_browser_on_region.done`
- Representative outputs: `results/finish/prep_browser_on_region.done`
- Execution targets: `prep_browser_on_region`
- Downstream handoff: `make_single_loci_browser_plot`

## Guardrails
- Treat `results/finish/prep_browser_on_region.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prep_browser_on_region.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_single_loci_browser_plot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prep_browser_on_region.done` exists and `make_single_loci_browser_plot` can proceed without re-running prep browser on region.
