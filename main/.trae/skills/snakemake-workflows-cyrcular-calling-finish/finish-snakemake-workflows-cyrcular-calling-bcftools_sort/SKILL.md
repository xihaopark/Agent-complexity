---
name: finish-snakemake-workflows-cyrcular-calling-bcftools_sort
description: Use this skill when orchestrating the retained "bcftools_sort" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the bcftools sort stage tied to upstream `bcftools_concat` and the downstream handoff to `varlociraptor_call`. It tracks completion via `results/finish/bcftools_sort.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: bcftools_sort
  step_name: bcftools sort
---

# Scope
Use this skill only for the `bcftools_sort` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `bcftools_concat`
- Step file: `finish/cyrcular-calling-finish/steps/bcftools_sort.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bcftools_sort.done`
- Representative outputs: `results/finish/bcftools_sort.done`
- Execution targets: `bcftools_sort`
- Downstream handoff: `varlociraptor_call`

## Guardrails
- Treat `results/finish/bcftools_sort.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bcftools_sort.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `varlociraptor_call` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bcftools_sort.done` exists and `varlociraptor_call` can proceed without re-running bcftools sort.
