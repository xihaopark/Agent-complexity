---
name: finish-riyadua-cervical-cancer-snakemake-workflow-differential_expression
description: Use this skill when orchestrating the retained "differential_expression" step of the riyadua cervical cancer snakemake workflow finish finish workflow. It keeps the differential expression stage tied to upstream `preprocess` and the downstream handoff to `all`. It tracks completion via `results/finish/differential_expression.done`.
metadata:
  workflow_id: riyadua-cervical-cancer-snakemake-workflow-finish
  workflow_name: riyadua cervical cancer snakemake workflow finish
  step_id: differential_expression
  step_name: differential expression
---

# Scope
Use this skill only for the `differential_expression` step in `riyadua-cervical-cancer-snakemake-workflow-finish`.

## Orchestration
- Upstream requirements: `preprocess`
- Step file: `finish/riyadua-cervical-cancer-snakemake-workflow-finish/steps/differential_expression.smk`
- Config file: `finish/riyadua-cervical-cancer-snakemake-workflow-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/differential_expression.done`
- Representative outputs: `results/finish/differential_expression.done`
- Execution targets: `differential_expression`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/differential_expression.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/differential_expression.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/differential_expression.done` exists and `all` can proceed without re-running differential expression.
