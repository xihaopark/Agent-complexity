---
name: finish-dwheelerau-snakemake-rnaseq-counts-clean
description: Use this skill when orchestrating the retained "clean" step of the dwheelerau snakemake rnaseq counts finish finish workflow. It keeps the clean stage tied to upstream `make_latex_tables` and the downstream handoff to `all`. It tracks completion via `results/finish/clean.done`.
metadata:
  workflow_id: dwheelerau-snakemake-rnaseq-counts-finish
  workflow_name: dwheelerau snakemake rnaseq counts finish
  step_id: clean
  step_name: clean
---

# Scope
Use this skill only for the `clean` step in `dwheelerau-snakemake-rnaseq-counts-finish`.

## Orchestration
- Upstream requirements: `make_latex_tables`
- Step file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/steps/clean.smk`
- Config file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/clean.done`
- Representative outputs: `results/finish/clean.done`
- Execution targets: `clean`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/clean.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/clean.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/clean.done` exists and `all` can proceed without re-running clean.
