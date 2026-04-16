---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-prepare_pca
description: Use this skill when orchestrating the retained "prepare_pca" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the prepare pca stage tied to upstream `plot_bootstrap` and the downstream handoff to `plot_pca`. It tracks completion via `results/finish/prepare_pca.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: prepare_pca
  step_name: prepare pca
---

# Scope
Use this skill only for the `prepare_pca` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `plot_bootstrap`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/prepare_pca.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepare_pca.done`
- Representative outputs: `results/finish/prepare_pca.done`
- Execution targets: `prepare_pca`
- Downstream handoff: `plot_pca`

## Guardrails
- Treat `results/finish/prepare_pca.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prepare_pca.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_pca` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prepare_pca.done` exists and `plot_pca` can proceed without re-running prepare pca.
