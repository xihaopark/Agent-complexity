---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-all
description: Use this skill when orchestrating the retained "all" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the all stage tied to upstream `meta_compare_pathways`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `meta_compare_pathways`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/all.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all.done`
- Representative outputs: `results/finish/all.done`
- Execution targets: `all`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/all.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/all.done` exists and matches the intended step boundary.
