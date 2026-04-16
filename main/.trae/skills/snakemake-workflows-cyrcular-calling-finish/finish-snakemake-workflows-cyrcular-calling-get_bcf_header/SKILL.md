---
name: finish-snakemake-workflows-cyrcular-calling-get_bcf_header
description: Use this skill when orchestrating the retained "get_bcf_header" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the get bcf header stage tied to upstream `sort_bcf_header` and the downstream handoff to `extract_vcf_header_lines_for_bcftools_annotate`. It tracks completion via `results/finish/get_bcf_header.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: get_bcf_header
  step_name: get bcf header
---

# Scope
Use this skill only for the `get_bcf_header` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `sort_bcf_header`
- Step file: `finish/cyrcular-calling-finish/steps/get_bcf_header.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_bcf_header.done`
- Representative outputs: `results/finish/get_bcf_header.done`
- Execution targets: `get_bcf_header`
- Downstream handoff: `extract_vcf_header_lines_for_bcftools_annotate`

## Guardrails
- Treat `results/finish/get_bcf_header.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_bcf_header.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `extract_vcf_header_lines_for_bcftools_annotate` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_bcf_header.done` exists and `extract_vcf_header_lines_for_bcftools_annotate` can proceed without re-running get bcf header.
