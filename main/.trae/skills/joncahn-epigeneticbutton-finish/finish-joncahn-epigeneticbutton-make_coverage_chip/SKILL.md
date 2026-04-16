---
name: finish-joncahn-epigeneticbutton-make_coverage_chip
description: Use this skill when orchestrating the retained "make_coverage_chip" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make coverage chip stage tied to upstream `pe_or_se_chip_dispatch` and the downstream handoff to `make_bigwig_chip`. It tracks completion via `results/finish/make_coverage_chip.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_coverage_chip
  step_name: make coverage chip
---

# Scope
Use this skill only for the `make_coverage_chip` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `pe_or_se_chip_dispatch`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_coverage_chip.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_coverage_chip.done`
- Representative outputs: `results/finish/make_coverage_chip.done`
- Execution targets: `make_coverage_chip`
- Downstream handoff: `make_bigwig_chip`

## Guardrails
- Treat `results/finish/make_coverage_chip.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_coverage_chip.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_bigwig_chip` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_coverage_chip.done` exists and `make_bigwig_chip` can proceed without re-running make coverage chip.
