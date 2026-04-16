---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-fgsea
description: Use this skill when orchestrating the retained "fgsea" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the fgsea stage tied to upstream `spia` and the downstream handoff to `fgsea_plot_gene_sets`. It tracks completion via `results/finish/fgsea.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: fgsea
  step_name: fgsea
---

# Scope
Use this skill only for the `fgsea` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `spia`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/fgsea.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fgsea.done`
- Representative outputs: `results/finish/fgsea.done`
- Execution targets: `fgsea`
- Downstream handoff: `fgsea_plot_gene_sets`

## Guardrails
- Treat `results/finish/fgsea.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fgsea.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fgsea_plot_gene_sets` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fgsea.done` exists and `fgsea_plot_gene_sets` can proceed without re-running fgsea.
