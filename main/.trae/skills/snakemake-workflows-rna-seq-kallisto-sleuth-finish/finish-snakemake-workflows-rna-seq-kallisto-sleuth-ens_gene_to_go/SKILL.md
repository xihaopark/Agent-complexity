---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-ens_gene_to_go
description: Use this skill when orchestrating the retained "ens_gene_to_go" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the ens gene to go stage tied to upstream `fgsea_plot_gene_sets` and the downstream handoff to `download_go_obo`. It tracks completion via `results/finish/ens_gene_to_go.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: ens_gene_to_go
  step_name: ens gene to go
---

# Scope
Use this skill only for the `ens_gene_to_go` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `fgsea_plot_gene_sets`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/ens_gene_to_go.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ens_gene_to_go.done`
- Representative outputs: `results/finish/ens_gene_to_go.done`
- Execution targets: `ens_gene_to_go`
- Downstream handoff: `download_go_obo`

## Guardrails
- Treat `results/finish/ens_gene_to_go.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ens_gene_to_go.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `download_go_obo` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ens_gene_to_go.done` exists and `download_go_obo` can proceed without re-running ens gene to go.
