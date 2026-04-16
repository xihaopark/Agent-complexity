---
name: finish-snakemake-workflows-cyrcular-calling-cyrcular_annotate_graph
description: Use this skill when orchestrating the retained "cyrcular_annotate_graph" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the cyrcular annotate graph stage tied to upstream `cyrcular_generate_tables` and the downstream handoff to `reheader_filtered_bcf`. It tracks completion via `results/finish/cyrcular_annotate_graph.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: cyrcular_annotate_graph
  step_name: cyrcular annotate graph
---

# Scope
Use this skill only for the `cyrcular_annotate_graph` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `cyrcular_generate_tables`
- Step file: `finish/cyrcular-calling-finish/steps/cyrcular_annotate_graph.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cyrcular_annotate_graph.done`
- Representative outputs: `results/finish/cyrcular_annotate_graph.done`
- Execution targets: `cyrcular_annotate_graph`
- Downstream handoff: `reheader_filtered_bcf`

## Guardrails
- Treat `results/finish/cyrcular_annotate_graph.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cyrcular_annotate_graph.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `reheader_filtered_bcf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cyrcular_annotate_graph.done` exists and `reheader_filtered_bcf` can proceed without re-running cyrcular annotate graph.
