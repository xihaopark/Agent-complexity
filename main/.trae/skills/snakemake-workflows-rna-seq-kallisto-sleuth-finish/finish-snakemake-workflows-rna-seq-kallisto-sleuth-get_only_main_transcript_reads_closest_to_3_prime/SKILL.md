---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-get_only_main_transcript_reads_closest_to_3_prime
description: Use this skill when orchestrating the retained "get_only_main_transcript_reads_closest_to_3_prime" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the get only main transcript reads closest to 3 prime stage tied to upstream `bwa_mem` and the downstream handoff to `get_main_transcript_fastq`. It tracks completion via `results/finish/get_only_main_transcript_reads_closest_to_3_prime.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: get_only_main_transcript_reads_closest_to_3_prime
  step_name: get only main transcript reads closest to 3 prime
---

# Scope
Use this skill only for the `get_only_main_transcript_reads_closest_to_3_prime` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `bwa_mem`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/get_only_main_transcript_reads_closest_to_3_prime.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_only_main_transcript_reads_closest_to_3_prime.done`
- Representative outputs: `results/finish/get_only_main_transcript_reads_closest_to_3_prime.done`
- Execution targets: `get_only_main_transcript_reads_closest_to_3_prime`
- Downstream handoff: `get_main_transcript_fastq`

## Guardrails
- Treat `results/finish/get_only_main_transcript_reads_closest_to_3_prime.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_only_main_transcript_reads_closest_to_3_prime.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_main_transcript_fastq` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_only_main_transcript_reads_closest_to_3_prime.done` exists and `get_main_transcript_fastq` can proceed without re-running get only main transcript reads closest to 3 prime.
