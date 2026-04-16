---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-kallisto_index
description: Use this skill when orchestrating the retained "kallisto_index" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the kallisto index stage tied to upstream `kallisto_long_quant_tcc` and the downstream handoff to `kallisto_quant`. It tracks completion via `results/finish/kallisto_index.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: kallisto_index
  step_name: kallisto index
---

# Scope
Use this skill only for the `kallisto_index` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `kallisto_long_quant_tcc`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/kallisto_index.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/kallisto_index.done`
- Representative outputs: `results/finish/kallisto_index.done`
- Execution targets: `kallisto_index`
- Downstream handoff: `kallisto_quant`

## Guardrails
- Treat `results/finish/kallisto_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/kallisto_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `kallisto_quant` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/kallisto_index.done` exists and `kallisto_quant` can proceed without re-running kallisto index.
