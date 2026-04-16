---
name: finish-maxplanck-ie-snakepipes-get_nearest_gene
description: Use this skill when orchestrating the retained "get_nearest_gene" step of the maxplanck ie snakepipes finish finish workflow. It keeps the get nearest gene stage tied to upstream `get_nearest_transcript` and the downstream handoff to `split_sampleSheet`. It tracks completion via `results/finish/get_nearest_gene.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: get_nearest_gene
  step_name: get nearest gene
---

# Scope
Use this skill only for the `get_nearest_gene` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `get_nearest_transcript`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/get_nearest_gene.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_nearest_gene.done`
- Representative outputs: `results/finish/get_nearest_gene.done`
- Execution targets: `get_nearest_gene`
- Downstream handoff: `split_sampleSheet`

## Guardrails
- Treat `results/finish/get_nearest_gene.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_nearest_gene.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `split_sampleSheet` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_nearest_gene.done` exists and `split_sampleSheet` can proceed without re-running get nearest gene.
