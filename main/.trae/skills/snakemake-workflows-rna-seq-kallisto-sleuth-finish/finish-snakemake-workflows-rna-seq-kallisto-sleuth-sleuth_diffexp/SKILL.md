---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-sleuth_diffexp
description: Use this skill when orchestrating the retained "sleuth_diffexp" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the sleuth diffexp stage tied to upstream `sleuth_init` and the downstream handoff to `ihw_fdr_control`. It tracks completion via `results/finish/sleuth_diffexp.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: sleuth_diffexp
  step_name: sleuth diffexp
---

# Scope
Use this skill only for the `sleuth_diffexp` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `sleuth_init`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/sleuth_diffexp.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sleuth_diffexp.done`
- Representative outputs: `results/finish/sleuth_diffexp.done`
- Execution targets: `sleuth_diffexp`
- Downstream handoff: `ihw_fdr_control`

## Guardrails
- Treat `results/finish/sleuth_diffexp.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sleuth_diffexp.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ihw_fdr_control` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sleuth_diffexp.done` exists and `ihw_fdr_control` can proceed without re-running sleuth diffexp.
