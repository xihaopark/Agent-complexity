---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-calculate_cpat_hexamers
description: Use this skill when orchestrating the retained "calculate_cpat_hexamers" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the calculate cpat hexamers stage tied to upstream `convert_pfam` and the downstream handoff to `calculate_cpat_logit_model`. It tracks completion via `results/finish/calculate_cpat_hexamers.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: calculate_cpat_hexamers
  step_name: calculate cpat hexamers
---

# Scope
Use this skill only for the `calculate_cpat_hexamers` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `convert_pfam`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/calculate_cpat_hexamers.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/calculate_cpat_hexamers.done`
- Representative outputs: `results/finish/calculate_cpat_hexamers.done`
- Execution targets: `calculate_cpat_hexamers`
- Downstream handoff: `calculate_cpat_logit_model`

## Guardrails
- Treat `results/finish/calculate_cpat_hexamers.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/calculate_cpat_hexamers.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `calculate_cpat_logit_model` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/calculate_cpat_hexamers.done` exists and `calculate_cpat_logit_model` can proceed without re-running calculate cpat hexamers.
