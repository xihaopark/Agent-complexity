---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-max_read_length
description: Use this skill when orchestrating the retained "max_read_length" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the max read length stage tied to upstream `fastp_pe` and the downstream handoff to `get_aligned_pos`. It tracks completion via `results/finish/max_read_length.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: max_read_length
  step_name: max read length
---

# Scope
Use this skill only for the `max_read_length` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `fastp_pe`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/max_read_length.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/max_read_length.done`
- Representative outputs: `results/finish/max_read_length.done`
- Execution targets: `max_read_length`
- Downstream handoff: `get_aligned_pos`

## Guardrails
- Treat `results/finish/max_read_length.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/max_read_length.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_aligned_pos` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/max_read_length.done` exists and `get_aligned_pos` can proceed without re-running max read length.
