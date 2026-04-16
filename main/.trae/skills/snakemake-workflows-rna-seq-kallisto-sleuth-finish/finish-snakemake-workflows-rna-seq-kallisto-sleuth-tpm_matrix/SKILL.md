---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-tpm_matrix
description: Use this skill when orchestrating the retained "tpm_matrix" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the tpm matrix stage tied to upstream `logcount_matrix` and the downstream handoff to `plot_diffexp_heatmap`. It tracks completion via `results/finish/tpm_matrix.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: tpm_matrix
  step_name: tpm matrix
---

# Scope
Use this skill only for the `tpm_matrix` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `logcount_matrix`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/tpm_matrix.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/tpm_matrix.done`
- Representative outputs: `results/finish/tpm_matrix.done`
- Execution targets: `tpm_matrix`
- Downstream handoff: `plot_diffexp_heatmap`

## Guardrails
- Treat `results/finish/tpm_matrix.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/tpm_matrix.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_diffexp_heatmap` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/tpm_matrix.done` exists and `plot_diffexp_heatmap` can proceed without re-running tpm matrix.
