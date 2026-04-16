---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-logcount_matrix
description: Use this skill when orchestrating the retained "logcount_matrix" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the logcount matrix stage tied to upstream `plot_diffexp_pval_hist` and the downstream handoff to `tpm_matrix`. It tracks completion via `results/finish/logcount_matrix.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: logcount_matrix
  step_name: logcount matrix
---

# Scope
Use this skill only for the `logcount_matrix` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `plot_diffexp_pval_hist`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/logcount_matrix.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/logcount_matrix.done`
- Representative outputs: `results/finish/logcount_matrix.done`
- Execution targets: `logcount_matrix`
- Downstream handoff: `tpm_matrix`

## Guardrails
- Treat `results/finish/logcount_matrix.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/logcount_matrix.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `tpm_matrix` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/logcount_matrix.done` exists and `tpm_matrix` can proceed without re-running logcount matrix.
