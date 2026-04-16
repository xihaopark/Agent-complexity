---
name: finish-maxplanck-ie-snakepipes-bampe_fragment_size
description: Use this skill when orchestrating the retained "bamPE_fragment_size" step of the maxplanck ie snakepipes finish finish workflow. It keeps the bamPE fragment size stage tied to upstream `computeGCBias` and the downstream handoff to `bamcoverage_short_cleaned`. It tracks completion via `results/finish/bamPE_fragment_size.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: bamPE_fragment_size
  step_name: bamPE fragment size
---

# Scope
Use this skill only for the `bamPE_fragment_size` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `computeGCBias`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/bamPE_fragment_size.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bamPE_fragment_size.done`
- Representative outputs: `results/finish/bamPE_fragment_size.done`
- Execution targets: `bamPE_fragment_size`
- Downstream handoff: `bamcoverage_short_cleaned`

## Guardrails
- Treat `results/finish/bamPE_fragment_size.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bamPE_fragment_size.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bamcoverage_short_cleaned` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bamPE_fragment_size.done` exists and `bamcoverage_short_cleaned` can proceed without re-running bamPE fragment size.
