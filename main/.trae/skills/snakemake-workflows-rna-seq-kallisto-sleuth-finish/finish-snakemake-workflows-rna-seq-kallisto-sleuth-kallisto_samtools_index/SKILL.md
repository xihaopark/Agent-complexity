---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-kallisto_samtools_index
description: Use this skill when orchestrating the retained "kallisto_samtools_index" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the kallisto samtools index stage tied to upstream `kallisto_samtools_sort` and the downstream handoff to `compose_sample_sheet`. It tracks completion via `results/finish/kallisto_samtools_index.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: kallisto_samtools_index
  step_name: kallisto samtools index
---

# Scope
Use this skill only for the `kallisto_samtools_index` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `kallisto_samtools_sort`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/kallisto_samtools_index.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/kallisto_samtools_index.done`
- Representative outputs: `results/finish/kallisto_samtools_index.done`
- Execution targets: `kallisto_samtools_index`
- Downstream handoff: `compose_sample_sheet`

## Guardrails
- Treat `results/finish/kallisto_samtools_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/kallisto_samtools_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `compose_sample_sheet` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/kallisto_samtools_index.done` exists and `compose_sample_sheet` can proceed without re-running kallisto samtools index.
