---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-bustools_count
description: Use this skill when orchestrating the retained "bustools_count" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the bustools count stage tied to upstream `bustools_sort` and the downstream handoff to `kallisto_long_quant_tcc`. It tracks completion via `results/finish/bustools_count.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: bustools_count
  step_name: bustools count
---

# Scope
Use this skill only for the `bustools_count` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `bustools_sort`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/bustools_count.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bustools_count.done`
- Representative outputs: `results/finish/bustools_count.done`
- Execution targets: `bustools_count`
- Downstream handoff: `kallisto_long_quant_tcc`

## Guardrails
- Treat `results/finish/bustools_count.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bustools_count.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `kallisto_long_quant_tcc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bustools_count.done` exists and `kallisto_long_quant_tcc` can proceed without re-running bustools count.
