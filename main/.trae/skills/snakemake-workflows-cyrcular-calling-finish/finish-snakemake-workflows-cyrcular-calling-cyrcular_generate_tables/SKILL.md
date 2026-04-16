---
name: finish-snakemake-workflows-cyrcular-calling-cyrcular_generate_tables
description: Use this skill when orchestrating the retained "cyrcular_generate_tables" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the cyrcular generate tables stage tied to upstream `circle_bnds` and the downstream handoff to `cyrcular_annotate_graph`. It tracks completion via `results/finish/cyrcular_generate_tables.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: cyrcular_generate_tables
  step_name: cyrcular generate tables
---

# Scope
Use this skill only for the `cyrcular_generate_tables` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `circle_bnds`
- Step file: `finish/cyrcular-calling-finish/steps/cyrcular_generate_tables.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cyrcular_generate_tables.done`
- Representative outputs: `results/finish/cyrcular_generate_tables.done`
- Execution targets: `cyrcular_generate_tables`
- Downstream handoff: `cyrcular_annotate_graph`

## Guardrails
- Treat `results/finish/cyrcular_generate_tables.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cyrcular_generate_tables.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cyrcular_annotate_graph` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cyrcular_generate_tables.done` exists and `cyrcular_annotate_graph` can proceed without re-running cyrcular generate tables.
