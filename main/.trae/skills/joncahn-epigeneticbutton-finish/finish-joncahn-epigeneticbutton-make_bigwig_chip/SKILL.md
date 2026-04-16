---
name: finish-joncahn-epigeneticbutton-make_bigwig_chip
description: Use this skill when orchestrating the retained "make_bigwig_chip" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make bigwig chip stage tied to upstream `make_coverage_chip` and the downstream handoff to `make_fingerprint_plot`. It tracks completion via `results/finish/make_bigwig_chip.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_bigwig_chip
  step_name: make bigwig chip
---

# Scope
Use this skill only for the `make_bigwig_chip` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_coverage_chip`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_bigwig_chip.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_bigwig_chip.done`
- Representative outputs: `results/finish/make_bigwig_chip.done`
- Execution targets: `make_bigwig_chip`
- Downstream handoff: `make_fingerprint_plot`

## Guardrails
- Treat `results/finish/make_bigwig_chip.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_bigwig_chip.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_fingerprint_plot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_bigwig_chip.done` exists and `make_fingerprint_plot` can proceed without re-running make bigwig chip.
