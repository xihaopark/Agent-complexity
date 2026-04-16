---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-calculate_coding_potential
description: Use this skill when orchestrating the retained "calculate_coding_potential" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the calculate coding potential stage tied to upstream `calculate_protein_domains` and the downstream handoff to `annotate_isoform_switch`. It tracks completion via `results/finish/calculate_coding_potential.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: calculate_coding_potential
  step_name: calculate coding potential
---

# Scope
Use this skill only for the `calculate_coding_potential` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `calculate_protein_domains`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/calculate_coding_potential.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/calculate_coding_potential.done`
- Representative outputs: `results/finish/calculate_coding_potential.done`
- Execution targets: `calculate_coding_potential`
- Downstream handoff: `annotate_isoform_switch`

## Guardrails
- Treat `results/finish/calculate_coding_potential.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/calculate_coding_potential.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annotate_isoform_switch` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/calculate_coding_potential.done` exists and `annotate_isoform_switch` can proceed without re-running calculate coding potential.
