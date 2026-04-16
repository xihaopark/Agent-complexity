---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-bwa_index
description: Use this skill when orchestrating the retained "bwa_index" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the bwa index stage tied to upstream `kallisto_quant` and the downstream handoff to `bwa_mem`. It tracks completion via `results/finish/bwa_index.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: bwa_index
  step_name: bwa index
---

# Scope
Use this skill only for the `bwa_index` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `kallisto_quant`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/bwa_index.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_index.done`
- Representative outputs: `results/finish/bwa_index.done`
- Execution targets: `bwa_index`
- Downstream handoff: `bwa_mem`

## Guardrails
- Treat `results/finish/bwa_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bwa_mem` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_index.done` exists and `bwa_mem` can proceed without re-running bwa index.
