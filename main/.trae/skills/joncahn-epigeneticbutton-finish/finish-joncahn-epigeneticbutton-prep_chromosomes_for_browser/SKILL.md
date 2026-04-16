---
name: finish-joncahn-epigeneticbutton-prep_chromosomes_for_browser
description: Use this skill when orchestrating the retained "prep_chromosomes_for_browser" step of the joncahn epigeneticbutton finish finish workflow. It keeps the prep chromosomes for browser stage tied to upstream `plotting_profile_on_targetfile` and the downstream handoff to `prep_browser_on_region`. It tracks completion via `results/finish/prep_chromosomes_for_browser.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: prep_chromosomes_for_browser
  step_name: prep chromosomes for browser
---

# Scope
Use this skill only for the `prep_chromosomes_for_browser` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `plotting_profile_on_targetfile`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/prep_chromosomes_for_browser.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prep_chromosomes_for_browser.done`
- Representative outputs: `results/finish/prep_chromosomes_for_browser.done`
- Execution targets: `prep_chromosomes_for_browser`
- Downstream handoff: `prep_browser_on_region`

## Guardrails
- Treat `results/finish/prep_chromosomes_for_browser.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prep_chromosomes_for_browser.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prep_browser_on_region` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prep_chromosomes_for_browser.done` exists and `prep_browser_on_region` can proceed without re-running prep chromosomes for browser.
