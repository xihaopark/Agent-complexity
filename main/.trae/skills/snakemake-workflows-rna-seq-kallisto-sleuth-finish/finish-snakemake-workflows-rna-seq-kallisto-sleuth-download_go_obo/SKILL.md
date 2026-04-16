---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-download_go_obo
description: Use this skill when orchestrating the retained "download_go_obo" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the download go obo stage tied to upstream `ens_gene_to_go` and the downstream handoff to `goatools_go_enrichment`. It tracks completion via `results/finish/download_go_obo.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: download_go_obo
  step_name: download go obo
---

# Scope
Use this skill only for the `download_go_obo` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `ens_gene_to_go`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/download_go_obo.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/download_go_obo.done`
- Representative outputs: `results/finish/download_go_obo.done`
- Execution targets: `download_go_obo`
- Downstream handoff: `goatools_go_enrichment`

## Guardrails
- Treat `results/finish/download_go_obo.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/download_go_obo.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `goatools_go_enrichment` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/download_go_obo.done` exists and `goatools_go_enrichment` can proceed without re-running download go obo.
