---
name: finish-epigen-enrichment-analysis-gene_ora_gseapy
description: Use this skill when orchestrating the retained "gene_ORA_GSEApy" step of the epigen enrichment_analysis finish finish workflow. It keeps the gene ORA GSEApy stage tied to upstream `env_export` and the downstream handoff to `gene_motif_enrichment_analysis_RcisTarget`. It tracks completion via `results/finish/gene_ORA_GSEApy.done`.
metadata:
  workflow_id: epigen-enrichment_analysis-finish
  workflow_name: epigen enrichment_analysis finish
  step_id: gene_ORA_GSEApy
  step_name: gene ORA GSEApy
---

# Scope
Use this skill only for the `gene_ORA_GSEApy` step in `epigen-enrichment_analysis-finish`.

## Orchestration
- Upstream requirements: `env_export`
- Step file: `finish/epigen-enrichment_analysis-finish/steps/gene_ORA_GSEApy.smk`
- Config file: `finish/epigen-enrichment_analysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gene_ORA_GSEApy.done`
- Representative outputs: `results/finish/gene_ORA_GSEApy.done`
- Execution targets: `gene_ORA_GSEApy`
- Downstream handoff: `gene_motif_enrichment_analysis_RcisTarget`

## Guardrails
- Treat `results/finish/gene_ORA_GSEApy.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gene_ORA_GSEApy.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gene_motif_enrichment_analysis_RcisTarget` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gene_ORA_GSEApy.done` exists and `gene_motif_enrichment_analysis_RcisTarget` can proceed without re-running gene ORA GSEApy.
