---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-get_selected_transcripts_aligned_read_bins
description: Use this skill when orchestrating the retained "get_selected_transcripts_aligned_read_bins" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the get selected transcripts aligned read bins stage tied to upstream `get_aligned_pos` and the downstream handoff to `get_selected_transcripts_sample_QC_histogram`. It tracks completion via `results/finish/get_selected_transcripts_aligned_read_bins.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: get_selected_transcripts_aligned_read_bins
  step_name: get selected transcripts aligned read bins
---

# Scope
Use this skill only for the `get_selected_transcripts_aligned_read_bins` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `get_aligned_pos`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/get_selected_transcripts_aligned_read_bins.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_selected_transcripts_aligned_read_bins.done`
- Representative outputs: `results/finish/get_selected_transcripts_aligned_read_bins.done`
- Execution targets: `get_selected_transcripts_aligned_read_bins`
- Downstream handoff: `get_selected_transcripts_sample_QC_histogram`

## Guardrails
- Treat `results/finish/get_selected_transcripts_aligned_read_bins.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_selected_transcripts_aligned_read_bins.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_selected_transcripts_sample_QC_histogram` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_selected_transcripts_aligned_read_bins.done` exists and `get_selected_transcripts_sample_QC_histogram` can proceed without re-running get selected transcripts aligned read bins.
