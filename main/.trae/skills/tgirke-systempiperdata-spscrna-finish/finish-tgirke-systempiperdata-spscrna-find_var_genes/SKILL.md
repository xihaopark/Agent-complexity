---
name: finish-tgirke-systempiperdata-spscrna-find_var_genes
description: Use this skill when orchestrating the retained "find_var_genes" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the find var genes stage tied to upstream `normalize` and the downstream handoff to `scaling`. It tracks completion via `results/finish/find_var_genes.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: find_var_genes
  step_name: find var genes
---

# Scope
Use this skill only for the `find_var_genes` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `normalize`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/find_var_genes.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/find_var_genes.done`
- Representative outputs: `results/finish/find_var_genes.done`
- Execution targets: `find_var_genes`
- Downstream handoff: `scaling`

## Guardrails
- Treat `results/finish/find_var_genes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/find_var_genes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `scaling` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/find_var_genes.done` exists and `scaling` can proceed without re-running find var genes.
