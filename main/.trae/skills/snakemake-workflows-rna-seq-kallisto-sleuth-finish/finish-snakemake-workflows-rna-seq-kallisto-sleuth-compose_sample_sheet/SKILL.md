---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-compose_sample_sheet
description: Use this skill when orchestrating the retained "compose_sample_sheet" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the compose sample sheet stage tied to upstream `kallisto_samtools_index` and the downstream handoff to `sleuth_init`. It tracks completion via `results/finish/compose_sample_sheet.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: compose_sample_sheet
  step_name: compose sample sheet
---

# Scope
Use this skill only for the `compose_sample_sheet` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `kallisto_samtools_index`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/compose_sample_sheet.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/compose_sample_sheet.done`
- Representative outputs: `results/finish/compose_sample_sheet.done`
- Execution targets: `compose_sample_sheet`
- Downstream handoff: `sleuth_init`

## Guardrails
- Treat `results/finish/compose_sample_sheet.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/compose_sample_sheet.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sleuth_init` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/compose_sample_sheet.done` exists and `sleuth_init` can proceed without re-running compose sample sheet.
