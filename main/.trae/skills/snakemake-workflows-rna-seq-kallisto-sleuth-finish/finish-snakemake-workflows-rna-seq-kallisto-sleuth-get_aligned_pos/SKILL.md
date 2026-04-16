---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-get_aligned_pos
description: Use this skill when orchestrating the retained "get_aligned_pos" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the get aligned pos stage tied to upstream `max_read_length` and the downstream handoff to `get_selected_transcripts_aligned_read_bins`. It tracks completion via `results/finish/get_aligned_pos.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: get_aligned_pos
  step_name: get aligned pos
---

# Scope
Use this skill only for the `get_aligned_pos` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `max_read_length`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/get_aligned_pos.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_aligned_pos.done`
- Representative outputs: `results/finish/get_aligned_pos.done`
- Execution targets: `get_aligned_pos`
- Downstream handoff: `get_selected_transcripts_aligned_read_bins`

## Guardrails
- Treat `results/finish/get_aligned_pos.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_aligned_pos.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_selected_transcripts_aligned_read_bins` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_aligned_pos.done` exists and `get_selected_transcripts_aligned_read_bins` can proceed without re-running get aligned pos.
