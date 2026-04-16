---
name: finish-epigen-dea-limma-one_vs_all_contrasts
description: Use this skill when orchestrating the retained "one_vs_all_contrasts" step of the epigen dea_limma finish finish workflow. It keeps the one vs all contrasts stage tied to upstream `dea` and the downstream handoff to `aggregate`. It tracks completion via `results/finish/one_vs_all_contrasts.done`.
metadata:
  workflow_id: epigen-dea_limma-finish
  workflow_name: epigen dea_limma finish
  step_id: one_vs_all_contrasts
  step_name: one vs all contrasts
---

# Scope
Use this skill only for the `one_vs_all_contrasts` step in `epigen-dea_limma-finish`.

## Orchestration
- Upstream requirements: `dea`
- Step file: `finish/epigen-dea_limma-finish/steps/one_vs_all_contrasts.smk`
- Config file: `finish/epigen-dea_limma-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/one_vs_all_contrasts.done`
- Representative outputs: `results/finish/one_vs_all_contrasts.done`
- Execution targets: `one_vs_all_contrasts`
- Downstream handoff: `aggregate`

## Guardrails
- Treat `results/finish/one_vs_all_contrasts.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/one_vs_all_contrasts.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `aggregate` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/one_vs_all_contrasts.done` exists and `aggregate` can proceed without re-running one vs all contrasts.
