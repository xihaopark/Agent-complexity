---
name: finish-riyadua-cervical-cancer-snakemake-workflow-preprocess
description: Use this skill when orchestrating the retained "preprocess" step of the riyadua cervical cancer snakemake workflow finish finish workflow. It keeps the preprocess stage and the downstream handoff to `differential_expression`. It tracks completion via `results/finish/preprocess.done`.
metadata:
  workflow_id: riyadua-cervical-cancer-snakemake-workflow-finish
  workflow_name: riyadua cervical cancer snakemake workflow finish
  step_id: preprocess
  step_name: preprocess
---

# Scope
Use this skill only for the `preprocess` step in `riyadua-cervical-cancer-snakemake-workflow-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/riyadua-cervical-cancer-snakemake-workflow-finish/steps/preprocess.smk`
- Config file: `finish/riyadua-cervical-cancer-snakemake-workflow-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/preprocess.done`
- Representative outputs: `results/finish/preprocess.done`
- Execution targets: `preprocess`
- Downstream handoff: `differential_expression`

## Guardrails
- Treat `results/finish/preprocess.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/preprocess.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `differential_expression` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/preprocess.done` exists and `differential_expression` can proceed without re-running preprocess.
