---
name: finish-dwheelerau-snakemake-rnaseq-counts-make_latex_tables
description: Use this skill when orchestrating the retained "make_latex_tables" step of the dwheelerau snakemake rnaseq counts finish finish workflow. It keeps the make latex tables stage tied to upstream `log_count_result` and the downstream handoff to `clean`. It tracks completion via `results/finish/make_latex_tables.done`.
metadata:
  workflow_id: dwheelerau-snakemake-rnaseq-counts-finish
  workflow_name: dwheelerau snakemake rnaseq counts finish
  step_id: make_latex_tables
  step_name: make latex tables
---

# Scope
Use this skill only for the `make_latex_tables` step in `dwheelerau-snakemake-rnaseq-counts-finish`.

## Orchestration
- Upstream requirements: `log_count_result`
- Step file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/steps/make_latex_tables.smk`
- Config file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_latex_tables.done`
- Representative outputs: `results/finish/make_latex_tables.done`
- Execution targets: `make_latex_tables`
- Downstream handoff: `clean`

## Guardrails
- Treat `results/finish/make_latex_tables.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_latex_tables.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `clean` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_latex_tables.done` exists and `clean` can proceed without re-running make latex tables.
