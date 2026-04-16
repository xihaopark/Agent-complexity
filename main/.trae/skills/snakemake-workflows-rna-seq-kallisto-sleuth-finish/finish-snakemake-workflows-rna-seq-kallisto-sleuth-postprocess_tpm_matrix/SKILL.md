---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-postprocess_tpm_matrix
description: Use this skill when orchestrating the retained "postprocess_tpm_matrix" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the postprocess tpm matrix stage tied to upstream `postprocess_diffexp` and the downstream handoff to `plot_enrichment_scatter`. It tracks completion via `results/finish/postprocess_tpm_matrix.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: postprocess_tpm_matrix
  step_name: postprocess tpm matrix
---

# Scope
Use this skill only for the `postprocess_tpm_matrix` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `postprocess_diffexp`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/postprocess_tpm_matrix.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/postprocess_tpm_matrix.done`
- Representative outputs: `results/finish/postprocess_tpm_matrix.done`
- Execution targets: `postprocess_tpm_matrix`
- Downstream handoff: `plot_enrichment_scatter`

## Guardrails
- Treat `results/finish/postprocess_tpm_matrix.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/postprocess_tpm_matrix.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_enrichment_scatter` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/postprocess_tpm_matrix.done` exists and `plot_enrichment_scatter` can proceed without re-running postprocess tpm matrix.
