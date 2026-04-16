---
name: finish-epigen-unsupervised-analysis-densmap_embed
description: Use this skill when orchestrating the retained "densmap_embed" step of the epigen unsupervised_analysis finish finish workflow. It keeps the densmap embed stage tied to upstream `config_export` and the downstream handoff to `distance_matrix`. It tracks completion via `results/finish/densmap_embed.done`.
metadata:
  workflow_id: epigen-unsupervised_analysis-finish
  workflow_name: epigen unsupervised_analysis finish
  step_id: densmap_embed
  step_name: densmap embed
---

# Scope
Use this skill only for the `densmap_embed` step in `epigen-unsupervised_analysis-finish`.

## Orchestration
- Upstream requirements: `config_export`
- Step file: `finish/epigen-unsupervised_analysis-finish/steps/densmap_embed.smk`
- Config file: `finish/epigen-unsupervised_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/densmap_embed.done`
- Representative outputs: `results/finish/densmap_embed.done`
- Execution targets: `densmap_embed`
- Downstream handoff: `distance_matrix`

## Guardrails
- Treat `results/finish/densmap_embed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/densmap_embed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `distance_matrix` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/densmap_embed.done` exists and `distance_matrix` can proceed without re-running densmap embed.
