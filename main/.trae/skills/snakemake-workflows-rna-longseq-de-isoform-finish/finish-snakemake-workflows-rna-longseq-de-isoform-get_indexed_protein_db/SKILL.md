---
name: finish-snakemake-workflows-rna-longseq-de-isoform-get_indexed_protein_db
description: Use this skill when orchestrating the retained "get_indexed_protein_db" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the get indexed protein db stage tied to upstream `iso_analysis_report` and the downstream handoff to `generate_gene_query`. It tracks completion via `results/finish/get_indexed_protein_db.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: get_indexed_protein_db
  step_name: get indexed protein db
---

# Scope
Use this skill only for the `get_indexed_protein_db` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `iso_analysis_report`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/get_indexed_protein_db.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_indexed_protein_db.done`
- Representative outputs: `results/finish/get_indexed_protein_db.done`
- Execution targets: `get_indexed_protein_db`
- Downstream handoff: `generate_gene_query`

## Guardrails
- Treat `results/finish/get_indexed_protein_db.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_indexed_protein_db.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `generate_gene_query` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_indexed_protein_db.done` exists and `generate_gene_query` can proceed without re-running get indexed protein db.
