---
name: finish-snakemake-workflows-rna-longseq-de-isoform-get_annotation
description: Use this skill when orchestrating the retained "get_annotation" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the get annotation stage tied to upstream `get_genome` and the downstream handoff to `standardize_gff`. It tracks completion via `results/finish/get_annotation.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: get_annotation
  step_name: get annotation
---

# Scope
Use this skill only for the `get_annotation` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `get_genome`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/get_annotation.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_annotation.done`
- Representative outputs: `results/finish/get_annotation.done`
- Execution targets: `get_annotation`
- Downstream handoff: `standardize_gff`

## Guardrails
- Treat `results/finish/get_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `standardize_gff` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_annotation.done` exists and `standardize_gff` can proceed without re-running get annotation.
