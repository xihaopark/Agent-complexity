---
name: finish-snakemake-workflows-cyrcular-calling-extract_vcf_header_lines_for_bcftools_annotate
description: Use this skill when orchestrating the retained "extract_vcf_header_lines_for_bcftools_annotate" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the extract vcf header lines for bcftools annotate stage tied to upstream `get_bcf_header` and the downstream handoff to `filter_overview_table`. It tracks completion via `results/finish/extract_vcf_header_lines_for_bcftools_annotate.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: extract_vcf_header_lines_for_bcftools_annotate
  step_name: extract vcf header lines for bcftools annotate
---

# Scope
Use this skill only for the `extract_vcf_header_lines_for_bcftools_annotate` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `get_bcf_header`
- Step file: `finish/cyrcular-calling-finish/steps/extract_vcf_header_lines_for_bcftools_annotate.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/extract_vcf_header_lines_for_bcftools_annotate.done`
- Representative outputs: `results/finish/extract_vcf_header_lines_for_bcftools_annotate.done`
- Execution targets: `extract_vcf_header_lines_for_bcftools_annotate`
- Downstream handoff: `filter_overview_table`

## Guardrails
- Treat `results/finish/extract_vcf_header_lines_for_bcftools_annotate.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/extract_vcf_header_lines_for_bcftools_annotate.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_overview_table` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/extract_vcf_header_lines_for_bcftools_annotate.done` exists and `filter_overview_table` can proceed without re-running extract vcf header lines for bcftools annotate.
