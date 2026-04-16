---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-convert_pfam
description: Use this skill when orchestrating the retained "convert_pfam" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the convert pfam stage tied to upstream `get_pfam` and the downstream handoff to `calculate_cpat_hexamers`. It tracks completion via `results/finish/convert_pfam.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: convert_pfam
  step_name: convert pfam
---

# Scope
Use this skill only for the `convert_pfam` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `get_pfam`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/convert_pfam.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/convert_pfam.done`
- Representative outputs: `results/finish/convert_pfam.done`
- Execution targets: `convert_pfam`
- Downstream handoff: `calculate_cpat_hexamers`

## Guardrails
- Treat `results/finish/convert_pfam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/convert_pfam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `calculate_cpat_hexamers` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/convert_pfam.done` exists and `calculate_cpat_hexamers` can proceed without re-running convert pfam.
