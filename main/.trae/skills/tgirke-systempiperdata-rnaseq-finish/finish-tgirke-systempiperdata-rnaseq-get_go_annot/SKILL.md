---
name: finish-tgirke-systempiperdata-rnaseq-get_go_annot
description: Use this skill when orchestrating the retained "get_go_annot" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the get go annot stage tied to upstream `venn_diagram` and the downstream handoff to `go_enrich`. It tracks completion via `results/finish/get_go_annot.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: get_go_annot
  step_name: get go annot
---

# Scope
Use this skill only for the `get_go_annot` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: `venn_diagram`
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/get_go_annot.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_go_annot.done`
- Representative outputs: `results/finish/get_go_annot.done`
- Execution targets: `get_go_annot`
- Downstream handoff: `go_enrich`

## Guardrails
- Treat `results/finish/get_go_annot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_go_annot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `go_enrich` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_go_annot.done` exists and `go_enrich` can proceed without re-running get go annot.
