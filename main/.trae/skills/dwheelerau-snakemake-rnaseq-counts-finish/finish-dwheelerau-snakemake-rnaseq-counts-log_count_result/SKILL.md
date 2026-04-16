---
name: finish-dwheelerau-snakemake-rnaseq-counts-log_count_result
description: Use this skill when orchestrating the retained "log_count_result" step of the dwheelerau snakemake rnaseq counts finish finish workflow. It keeps the log count result stage tied to upstream `do_counts` and the downstream handoff to `make_latex_tables`. It tracks completion via `results/finish/log_count_result.done`.
metadata:
  workflow_id: dwheelerau-snakemake-rnaseq-counts-finish
  workflow_name: dwheelerau snakemake rnaseq counts finish
  step_id: log_count_result
  step_name: log count result
---

# Scope
Use this skill only for the `log_count_result` step in `dwheelerau-snakemake-rnaseq-counts-finish`.

## Orchestration
- Upstream requirements: `do_counts`
- Step file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/steps/log_count_result.smk`
- Config file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/log_count_result.done`
- Representative outputs: `results/finish/log_count_result.done`
- Execution targets: `log_count_result`
- Downstream handoff: `make_latex_tables`

## Guardrails
- Treat `results/finish/log_count_result.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/log_count_result.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_latex_tables` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/log_count_result.done` exists and `make_latex_tables` can proceed without re-running log count result.
