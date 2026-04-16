---
name: finish-snakemake-workflows-cyrcular-calling-filter_varlociraptor
description: Use this skill when orchestrating the retained "filter_varlociraptor" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the filter varlociraptor stage tied to upstream `filter_overview_table` and the downstream handoff to `circle_coverage_plot`. It tracks completion via `results/finish/filter_varlociraptor.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: filter_varlociraptor
  step_name: filter varlociraptor
---

# Scope
Use this skill only for the `filter_varlociraptor` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `filter_overview_table`
- Step file: `finish/cyrcular-calling-finish/steps/filter_varlociraptor.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_varlociraptor.done`
- Representative outputs: `results/finish/filter_varlociraptor.done`
- Execution targets: `filter_varlociraptor`
- Downstream handoff: `circle_coverage_plot`

## Guardrails
- Treat `results/finish/filter_varlociraptor.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_varlociraptor.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `circle_coverage_plot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_varlociraptor.done` exists and `circle_coverage_plot` can proceed without re-running filter varlociraptor.
