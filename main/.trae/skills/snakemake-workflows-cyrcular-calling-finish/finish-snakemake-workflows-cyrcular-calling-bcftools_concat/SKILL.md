---
name: finish-snakemake-workflows-cyrcular-calling-bcftools_concat
description: Use this skill when orchestrating the retained "bcftools_concat" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the bcftools concat stage tied to upstream `bcf_index` and the downstream handoff to `bcftools_sort`. It tracks completion via `results/finish/bcftools_concat.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: bcftools_concat
  step_name: bcftools concat
---

# Scope
Use this skill only for the `bcftools_concat` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `bcf_index`
- Step file: `finish/cyrcular-calling-finish/steps/bcftools_concat.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bcftools_concat.done`
- Representative outputs: `results/finish/bcftools_concat.done`
- Execution targets: `bcftools_concat`
- Downstream handoff: `bcftools_sort`

## Guardrails
- Treat `results/finish/bcftools_concat.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bcftools_concat.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bcftools_sort` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bcftools_concat.done` exists and `bcftools_sort` can proceed without re-running bcftools concat.
