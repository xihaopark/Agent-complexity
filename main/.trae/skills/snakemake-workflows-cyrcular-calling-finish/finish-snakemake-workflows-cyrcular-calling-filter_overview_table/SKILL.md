---
name: finish-snakemake-workflows-cyrcular-calling-filter_overview_table
description: Use this skill when orchestrating the retained "filter_overview_table" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the filter overview table stage tied to upstream `extract_vcf_header_lines_for_bcftools_annotate` and the downstream handoff to `filter_varlociraptor`. It tracks completion via `results/finish/filter_overview_table.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: filter_overview_table
  step_name: filter overview table
---

# Scope
Use this skill only for the `filter_overview_table` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `extract_vcf_header_lines_for_bcftools_annotate`
- Step file: `finish/cyrcular-calling-finish/steps/filter_overview_table.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_overview_table.done`
- Representative outputs: `results/finish/filter_overview_table.done`
- Execution targets: `filter_overview_table`
- Downstream handoff: `filter_varlociraptor`

## Guardrails
- Treat `results/finish/filter_overview_table.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_overview_table.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_varlociraptor` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_overview_table.done` exists and `filter_varlociraptor` can proceed without re-running filter overview table.
