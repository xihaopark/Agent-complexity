---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-bustools_sort
description: Use this skill when orchestrating the retained "bustools_sort" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the bustools sort stage tied to upstream `kallisto_long_bus` and the downstream handoff to `bustools_count`. It tracks completion via `results/finish/bustools_sort.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: bustools_sort
  step_name: bustools sort
---

# Scope
Use this skill only for the `bustools_sort` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `kallisto_long_bus`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/bustools_sort.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bustools_sort.done`
- Representative outputs: `results/finish/bustools_sort.done`
- Execution targets: `bustools_sort`
- Downstream handoff: `bustools_count`

## Guardrails
- Treat `results/finish/bustools_sort.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bustools_sort.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bustools_count` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bustools_sort.done` exists and `bustools_count` can proceed without re-running bustools sort.
