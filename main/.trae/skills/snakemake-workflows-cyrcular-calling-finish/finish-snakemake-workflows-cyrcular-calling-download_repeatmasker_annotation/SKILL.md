---
name: finish-snakemake-workflows-cyrcular-calling-download_repeatmasker_annotation
description: Use this skill when orchestrating the retained "download_repeatmasker_annotation" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the download repeatmasker annotation stage tied to upstream `download_regulatory_annotation` and the downstream handoff to `download_gene_annotation`. It tracks completion via `results/finish/download_repeatmasker_annotation.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: download_repeatmasker_annotation
  step_name: download repeatmasker annotation
---

# Scope
Use this skill only for the `download_repeatmasker_annotation` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `download_regulatory_annotation`
- Step file: `finish/cyrcular-calling-finish/steps/download_repeatmasker_annotation.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/download_repeatmasker_annotation.done`
- Representative outputs: `results/finish/download_repeatmasker_annotation.done`
- Execution targets: `download_repeatmasker_annotation`
- Downstream handoff: `download_gene_annotation`

## Guardrails
- Treat `results/finish/download_repeatmasker_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/download_repeatmasker_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `download_gene_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/download_repeatmasker_annotation.done` exists and `download_gene_annotation` can proceed without re-running download repeatmasker annotation.
