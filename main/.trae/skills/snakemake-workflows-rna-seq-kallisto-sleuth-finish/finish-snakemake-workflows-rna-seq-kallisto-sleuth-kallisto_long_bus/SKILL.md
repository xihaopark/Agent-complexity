---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-kallisto_long_bus
description: Use this skill when orchestrating the retained "kallisto_long_bus" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the kallisto long bus stage tied to upstream `kallisto_long_index` and the downstream handoff to `bustools_sort`. It tracks completion via `results/finish/kallisto_long_bus.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: kallisto_long_bus
  step_name: kallisto long bus
---

# Scope
Use this skill only for the `kallisto_long_bus` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `kallisto_long_index`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/kallisto_long_bus.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/kallisto_long_bus.done`
- Representative outputs: `results/finish/kallisto_long_bus.done`
- Execution targets: `kallisto_long_bus`
- Downstream handoff: `bustools_sort`

## Guardrails
- Treat `results/finish/kallisto_long_bus.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/kallisto_long_bus.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bustools_sort` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/kallisto_long_bus.done` exists and `bustools_sort` can proceed without re-running kallisto long bus.
