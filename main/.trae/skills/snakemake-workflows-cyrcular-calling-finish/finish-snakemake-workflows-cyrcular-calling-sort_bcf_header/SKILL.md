---
name: finish-snakemake-workflows-cyrcular-calling-sort_bcf_header
description: Use this skill when orchestrating the retained "sort_bcf_header" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the sort bcf header stage tied to upstream `reheader_filtered_bcf` and the downstream handoff to `get_bcf_header`. It tracks completion via `results/finish/sort_bcf_header.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: sort_bcf_header
  step_name: sort bcf header
---

# Scope
Use this skill only for the `sort_bcf_header` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `reheader_filtered_bcf`
- Step file: `finish/cyrcular-calling-finish/steps/sort_bcf_header.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sort_bcf_header.done`
- Representative outputs: `results/finish/sort_bcf_header.done`
- Execution targets: `sort_bcf_header`
- Downstream handoff: `get_bcf_header`

## Guardrails
- Treat `results/finish/sort_bcf_header.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sort_bcf_header.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_bcf_header` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sort_bcf_header.done` exists and `get_bcf_header` can proceed without re-running sort bcf header.
