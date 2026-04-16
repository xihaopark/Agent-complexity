---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-get_main_transcript_fastq
description: Use this skill when orchestrating the retained "get_main_transcript_fastq" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the get main transcript fastq stage tied to upstream `get_only_main_transcript_reads_closest_to_3_prime` and the downstream handoff to `kallisto_3prime_index`. It tracks completion via `results/finish/get_main_transcript_fastq.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: get_main_transcript_fastq
  step_name: get main transcript fastq
---

# Scope
Use this skill only for the `get_main_transcript_fastq` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `get_only_main_transcript_reads_closest_to_3_prime`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/get_main_transcript_fastq.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_main_transcript_fastq.done`
- Representative outputs: `results/finish/get_main_transcript_fastq.done`
- Execution targets: `get_main_transcript_fastq`
- Downstream handoff: `kallisto_3prime_index`

## Guardrails
- Treat `results/finish/get_main_transcript_fastq.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_main_transcript_fastq.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `kallisto_3prime_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_main_transcript_fastq.done` exists and `kallisto_3prime_index` can proceed without re-running get main transcript fastq.
