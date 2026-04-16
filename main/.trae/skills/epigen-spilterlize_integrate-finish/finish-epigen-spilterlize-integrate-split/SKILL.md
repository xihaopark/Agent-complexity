---
name: finish-epigen-spilterlize-integrate-split
description: Use this skill when orchestrating the retained "split" step of the epigen spilterlize_integrate finish finish workflow. It keeps the split stage and the downstream handoff to `filter_features`. It tracks completion via `results/finish/split.done`.
metadata:
  workflow_id: epigen-spilterlize_integrate-finish
  workflow_name: epigen spilterlize_integrate finish
  step_id: split
  step_name: split
---

# Scope
Use this skill only for the `split` step in `epigen-spilterlize_integrate-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/epigen-spilterlize_integrate-finish/steps/split.smk`
- Config file: `finish/epigen-spilterlize_integrate-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/split.done`
- Representative outputs: `results/finish/split.done`
- Execution targets: `split`
- Downstream handoff: `filter_features`

## Guardrails
- Treat `results/finish/split.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/split.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_features` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/split.done` exists and `filter_features` can proceed without re-running split.
