---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-init_isoform_switch
description: Use this skill when orchestrating the retained "init_isoform_switch" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the init isoform switch stage tied to upstream `vega_volcano_plot` and the downstream handoff to `calculate_protein_domains`. It tracks completion via `results/finish/init_isoform_switch.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: init_isoform_switch
  step_name: init isoform switch
---

# Scope
Use this skill only for the `init_isoform_switch` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `vega_volcano_plot`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/init_isoform_switch.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/init_isoform_switch.done`
- Representative outputs: `results/finish/init_isoform_switch.done`
- Execution targets: `init_isoform_switch`
- Downstream handoff: `calculate_protein_domains`

## Guardrails
- Treat `results/finish/init_isoform_switch.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/init_isoform_switch.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `calculate_protein_domains` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/init_isoform_switch.done` exists and `calculate_protein_domains` can proceed without re-running init isoform switch.
