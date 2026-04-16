---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-kallisto_quant
description: Use this skill when orchestrating the retained "kallisto_quant" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the kallisto quant stage tied to upstream `kallisto_index` and the downstream handoff to `bwa_index`. It tracks completion via `results/finish/kallisto_quant.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: kallisto_quant
  step_name: kallisto quant
---

# Scope
Use this skill only for the `kallisto_quant` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `kallisto_index`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/kallisto_quant.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/kallisto_quant.done`
- Representative outputs: `results/finish/kallisto_quant.done`
- Execution targets: `kallisto_quant`
- Downstream handoff: `bwa_index`

## Guardrails
- Treat `results/finish/kallisto_quant.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/kallisto_quant.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bwa_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/kallisto_quant.done` exists and `bwa_index` can proceed without re-running kallisto quant.
