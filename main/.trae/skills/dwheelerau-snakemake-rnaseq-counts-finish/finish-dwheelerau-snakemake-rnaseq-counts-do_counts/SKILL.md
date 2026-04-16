---
name: finish-dwheelerau-snakemake-rnaseq-counts-do_counts
description: Use this skill when orchestrating the retained "do_counts" step of the dwheelerau snakemake rnaseq counts finish finish workflow. It keeps the do counts stage tied to upstream `sam_to_bam` and the downstream handoff to `log_count_result`. It tracks completion via `results/finish/do_counts.done`.
metadata:
  workflow_id: dwheelerau-snakemake-rnaseq-counts-finish
  workflow_name: dwheelerau snakemake rnaseq counts finish
  step_id: do_counts
  step_name: do counts
---

# Scope
Use this skill only for the `do_counts` step in `dwheelerau-snakemake-rnaseq-counts-finish`.

## Orchestration
- Upstream requirements: `sam_to_bam`
- Step file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/steps/do_counts.smk`
- Config file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/do_counts.done`
- Representative outputs: `results/finish/do_counts.done`
- Execution targets: `do_counts`
- Downstream handoff: `log_count_result`

## Guardrails
- Treat `results/finish/do_counts.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/do_counts.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `log_count_result` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/do_counts.done` exists and `log_count_result` can proceed without re-running do counts.
