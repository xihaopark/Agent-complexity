---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-fgsea_plot_gene_sets
description: Use this skill when orchestrating the retained "fgsea_plot_gene_sets" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the fgsea plot gene sets stage tied to upstream `fgsea` and the downstream handoff to `ens_gene_to_go`. It tracks completion via `results/finish/fgsea_plot_gene_sets.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: fgsea_plot_gene_sets
  step_name: fgsea plot gene sets
---

# Scope
Use this skill only for the `fgsea_plot_gene_sets` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `fgsea`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/fgsea_plot_gene_sets.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fgsea_plot_gene_sets.done`
- Representative outputs: `results/finish/fgsea_plot_gene_sets.done`
- Execution targets: `fgsea_plot_gene_sets`
- Downstream handoff: `ens_gene_to_go`

## Guardrails
- Treat `results/finish/fgsea_plot_gene_sets.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fgsea_plot_gene_sets.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ens_gene_to_go` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fgsea_plot_gene_sets.done` exists and `ens_gene_to_go` can proceed without re-running fgsea plot gene sets.
