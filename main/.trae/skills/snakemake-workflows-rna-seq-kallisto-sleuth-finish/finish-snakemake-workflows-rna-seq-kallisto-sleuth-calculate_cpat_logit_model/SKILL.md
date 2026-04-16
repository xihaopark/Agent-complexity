---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-calculate_cpat_logit_model
description: Use this skill when orchestrating the retained "calculate_cpat_logit_model" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the calculate cpat logit model stage tied to upstream `calculate_cpat_hexamers` and the downstream handoff to `get_spia_db`. It tracks completion via `results/finish/calculate_cpat_logit_model.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: calculate_cpat_logit_model
  step_name: calculate cpat logit model
---

# Scope
Use this skill only for the `calculate_cpat_logit_model` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `calculate_cpat_hexamers`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/calculate_cpat_logit_model.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/calculate_cpat_logit_model.done`
- Representative outputs: `results/finish/calculate_cpat_logit_model.done`
- Execution targets: `calculate_cpat_logit_model`
- Downstream handoff: `get_spia_db`

## Guardrails
- Treat `results/finish/calculate_cpat_logit_model.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/calculate_cpat_logit_model.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_spia_db` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/calculate_cpat_logit_model.done` exists and `get_spia_db` can proceed without re-running calculate cpat logit model.
