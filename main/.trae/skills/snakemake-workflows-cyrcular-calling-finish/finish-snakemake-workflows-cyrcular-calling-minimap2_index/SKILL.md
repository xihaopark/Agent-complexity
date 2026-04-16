---
name: finish-snakemake-workflows-cyrcular-calling-minimap2_index
description: Use this skill when orchestrating the retained "minimap2_index" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the minimap2 index stage tied to upstream `genome_faidx` and the downstream handoff to `download_regulatory_annotation`. It tracks completion via `results/finish/minimap2_index.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: minimap2_index
  step_name: minimap2 index
---

# Scope
Use this skill only for the `minimap2_index` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `genome_faidx`
- Step file: `finish/cyrcular-calling-finish/steps/minimap2_index.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/minimap2_index.done`
- Representative outputs: `results/finish/minimap2_index.done`
- Execution targets: `minimap2_index`
- Downstream handoff: `download_regulatory_annotation`

## Guardrails
- Treat `results/finish/minimap2_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/minimap2_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `download_regulatory_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/minimap2_index.done` exists and `download_regulatory_annotation` can proceed without re-running minimap2 index.
