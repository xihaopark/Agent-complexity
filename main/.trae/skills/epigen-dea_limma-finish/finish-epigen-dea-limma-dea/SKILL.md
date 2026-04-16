---
name: finish-epigen-dea-limma-dea
description: Use this skill when orchestrating the retained "dea" step of the epigen dea_limma finish finish workflow. It keeps the dea stage and the downstream handoff to `one_vs_all_contrasts`. It tracks completion via `results/finish/dea.done`.
metadata:
  workflow_id: epigen-dea_limma-finish
  workflow_name: epigen dea_limma finish
  step_id: dea
  step_name: dea
---

# Scope
Use this skill only for the `dea` step in `epigen-dea_limma-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/epigen-dea_limma-finish/steps/dea.smk`
- Config file: `finish/epigen-dea_limma-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/dea.done`
- Representative outputs: `results/finish/dea.done`
- Execution targets: `dea`
- Downstream handoff: `one_vs_all_contrasts`

## Guardrails
- Treat `results/finish/dea.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/dea.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `one_vs_all_contrasts` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/dea.done` exists and `one_vs_all_contrasts` can proceed without re-running dea.
