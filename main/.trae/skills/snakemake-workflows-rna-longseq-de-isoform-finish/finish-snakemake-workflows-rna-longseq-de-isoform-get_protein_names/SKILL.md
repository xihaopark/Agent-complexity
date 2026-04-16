---
name: finish-snakemake-workflows-rna-longseq-de-isoform-get_protein_names
description: Use this skill when orchestrating the retained "get_protein_names" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the get protein names stage tied to upstream `lambda_gene_annotation` and the downstream handoff to `all`. It tracks completion via `results/finish/get_protein_names.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: get_protein_names
  step_name: get protein names
---

# Scope
Use this skill only for the `get_protein_names` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `lambda_gene_annotation`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/get_protein_names.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_protein_names.done`
- Representative outputs: `results/finish/get_protein_names.done`
- Execution targets: `get_protein_names`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/get_protein_names.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_protein_names.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_protein_names.done` exists and `all` can proceed without re-running get protein names.
