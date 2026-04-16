---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-ihw_fdr_control
description: Use this skill when orchestrating the retained "ihw_fdr_control" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the ihw fdr control stage tied to upstream `sleuth_diffexp` and the downstream handoff to `plot_bootstrap`. It tracks completion via `results/finish/ihw_fdr_control.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: ihw_fdr_control
  step_name: ihw fdr control
---

# Scope
Use this skill only for the `ihw_fdr_control` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `sleuth_diffexp`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/ihw_fdr_control.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ihw_fdr_control.done`
- Representative outputs: `results/finish/ihw_fdr_control.done`
- Execution targets: `ihw_fdr_control`
- Downstream handoff: `plot_bootstrap`

## Guardrails
- Treat `results/finish/ihw_fdr_control.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ihw_fdr_control.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_bootstrap` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ihw_fdr_control.done` exists and `plot_bootstrap` can proceed without re-running ihw fdr control.
