---
name: finish-maxplanck-ie-snakepipes-bamcoverage_short_cleaned
description: Use this skill when orchestrating the retained "bamcoverage_short_cleaned" step of the maxplanck ie snakepipes finish finish workflow. It keeps the bamcoverage short cleaned stage tied to upstream `bamPE_fragment_size` and the downstream handoff to `multiQC`. It tracks completion via `results/finish/bamcoverage_short_cleaned.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: bamcoverage_short_cleaned
  step_name: bamcoverage short cleaned
---

# Scope
Use this skill only for the `bamcoverage_short_cleaned` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `bamPE_fragment_size`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/bamcoverage_short_cleaned.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bamcoverage_short_cleaned.done`
- Representative outputs: `results/finish/bamcoverage_short_cleaned.done`
- Execution targets: `bamcoverage_short_cleaned`
- Downstream handoff: `multiQC`

## Guardrails
- Treat `results/finish/bamcoverage_short_cleaned.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bamcoverage_short_cleaned.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiQC` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bamcoverage_short_cleaned.done` exists and `multiQC` can proceed without re-running bamcoverage short cleaned.
