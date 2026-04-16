---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-kallisto_3prime_quant
description: Use this skill when orchestrating the retained "kallisto_3prime_quant" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the kallisto 3prime quant stage tied to upstream `kallisto_3prime_index` and the downstream handoff to `kallisto_samtools_sort`. It tracks completion via `results/finish/kallisto_3prime_quant.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: kallisto_3prime_quant
  step_name: kallisto 3prime quant
---

# Scope
Use this skill only for the `kallisto_3prime_quant` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `kallisto_3prime_index`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/kallisto_3prime_quant.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/kallisto_3prime_quant.done`
- Representative outputs: `results/finish/kallisto_3prime_quant.done`
- Execution targets: `kallisto_3prime_quant`
- Downstream handoff: `kallisto_samtools_sort`

## Guardrails
- Treat `results/finish/kallisto_3prime_quant.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/kallisto_3prime_quant.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `kallisto_samtools_sort` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/kallisto_3prime_quant.done` exists and `kallisto_samtools_sort` can proceed without re-running kallisto 3prime quant.
