---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-annotate_isoform_switch
description: Use this skill when orchestrating the retained "annotate_isoform_switch" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the annotate isoform switch stage tied to upstream `calculate_coding_potential` and the downstream handoff to `spia`. It tracks completion via `results/finish/annotate_isoform_switch.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: annotate_isoform_switch
  step_name: annotate isoform switch
---

# Scope
Use this skill only for the `annotate_isoform_switch` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `calculate_coding_potential`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/annotate_isoform_switch.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotate_isoform_switch.done`
- Representative outputs: `results/finish/annotate_isoform_switch.done`
- Execution targets: `annotate_isoform_switch`
- Downstream handoff: `spia`

## Guardrails
- Treat `results/finish/annotate_isoform_switch.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annotate_isoform_switch.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `spia` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annotate_isoform_switch.done` exists and `spia` can proceed without re-running annotate isoform switch.
