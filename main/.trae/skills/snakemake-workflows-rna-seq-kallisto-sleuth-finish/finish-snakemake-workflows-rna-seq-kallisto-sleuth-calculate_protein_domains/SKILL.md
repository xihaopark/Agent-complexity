---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-calculate_protein_domains
description: Use this skill when orchestrating the retained "calculate_protein_domains" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the calculate protein domains stage tied to upstream `init_isoform_switch` and the downstream handoff to `calculate_coding_potential`. It tracks completion via `results/finish/calculate_protein_domains.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: calculate_protein_domains
  step_name: calculate protein domains
---

# Scope
Use this skill only for the `calculate_protein_domains` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `init_isoform_switch`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/calculate_protein_domains.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/calculate_protein_domains.done`
- Representative outputs: `results/finish/calculate_protein_domains.done`
- Execution targets: `calculate_protein_domains`
- Downstream handoff: `calculate_coding_potential`

## Guardrails
- Treat `results/finish/calculate_protein_domains.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/calculate_protein_domains.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `calculate_coding_potential` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/calculate_protein_domains.done` exists and `calculate_coding_potential` can proceed without re-running calculate protein domains.
