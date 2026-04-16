---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-kallisto_samtools_sort
description: Use this skill when orchestrating the retained "kallisto_samtools_sort" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the kallisto samtools sort stage tied to upstream `kallisto_3prime_quant` and the downstream handoff to `kallisto_samtools_index`. It tracks completion via `results/finish/kallisto_samtools_sort.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: kallisto_samtools_sort
  step_name: kallisto samtools sort
---

# Scope
Use this skill only for the `kallisto_samtools_sort` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `kallisto_3prime_quant`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/kallisto_samtools_sort.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/kallisto_samtools_sort.done`
- Representative outputs: `results/finish/kallisto_samtools_sort.done`
- Execution targets: `kallisto_samtools_sort`
- Downstream handoff: `kallisto_samtools_index`

## Guardrails
- Treat `results/finish/kallisto_samtools_sort.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/kallisto_samtools_sort.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `kallisto_samtools_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/kallisto_samtools_sort.done` exists and `kallisto_samtools_index` can proceed without re-running kallisto samtools sort.
