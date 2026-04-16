---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-get_main_transcripts_fasta
description: Use this skill when orchestrating the retained "get_main_transcripts_fasta" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the get main transcripts fasta stage tied to upstream `cds_polyA_T_removal` and the downstream handoff to `kallisto_long_index`. It tracks completion via `results/finish/get_main_transcripts_fasta.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: get_main_transcripts_fasta
  step_name: get main transcripts fasta
---

# Scope
Use this skill only for the `get_main_transcripts_fasta` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `cds_polyA_T_removal`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/get_main_transcripts_fasta.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_main_transcripts_fasta.done`
- Representative outputs: `results/finish/get_main_transcripts_fasta.done`
- Execution targets: `get_main_transcripts_fasta`
- Downstream handoff: `kallisto_long_index`

## Guardrails
- Treat `results/finish/get_main_transcripts_fasta.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_main_transcripts_fasta.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `kallisto_long_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_main_transcripts_fasta.done` exists and `kallisto_long_index` can proceed without re-running get main transcripts fasta.
