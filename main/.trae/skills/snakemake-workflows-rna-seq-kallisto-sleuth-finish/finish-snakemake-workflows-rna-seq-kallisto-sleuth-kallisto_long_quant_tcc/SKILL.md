---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-kallisto_long_quant_tcc
description: Use this skill when orchestrating the retained "kallisto_long_quant_tcc" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the kallisto long quant tcc stage tied to upstream `bustools_count` and the downstream handoff to `kallisto_index`. It tracks completion via `results/finish/kallisto_long_quant_tcc.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: kallisto_long_quant_tcc
  step_name: kallisto long quant tcc
---

# Scope
Use this skill only for the `kallisto_long_quant_tcc` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `bustools_count`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/kallisto_long_quant_tcc.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/kallisto_long_quant_tcc.done`
- Representative outputs: `results/finish/kallisto_long_quant_tcc.done`
- Execution targets: `kallisto_long_quant_tcc`
- Downstream handoff: `kallisto_index`

## Guardrails
- Treat `results/finish/kallisto_long_quant_tcc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/kallisto_long_quant_tcc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `kallisto_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/kallisto_long_quant_tcc.done` exists and `kallisto_index` can proceed without re-running kallisto long quant tcc.
