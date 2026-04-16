---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-bwa_mem
description: Use this skill when orchestrating the retained "bwa_mem" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the bwa mem stage tied to upstream `bwa_index` and the downstream handoff to `get_only_main_transcript_reads_closest_to_3_prime`. It tracks completion via `results/finish/bwa_mem.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: bwa_mem
  step_name: bwa mem
---

# Scope
Use this skill only for the `bwa_mem` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `bwa_index`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/bwa_mem.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_mem.done`
- Representative outputs: `results/finish/bwa_mem.done`
- Execution targets: `bwa_mem`
- Downstream handoff: `get_only_main_transcript_reads_closest_to_3_prime`

## Guardrails
- Treat `results/finish/bwa_mem.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_mem.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_only_main_transcript_reads_closest_to_3_prime` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_mem.done` exists and `get_only_main_transcript_reads_closest_to_3_prime` can proceed without re-running bwa mem.
