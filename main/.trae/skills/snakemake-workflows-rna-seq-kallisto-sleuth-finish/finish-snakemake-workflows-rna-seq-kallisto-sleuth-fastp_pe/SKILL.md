---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-fastp_pe
description: Use this skill when orchestrating the retained "fastp_pe" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the fastp pe stage tied to upstream `fastp_se` and the downstream handoff to `max_read_length`. It tracks completion via `results/finish/fastp_pe.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: fastp_pe
  step_name: fastp pe
---

# Scope
Use this skill only for the `fastp_pe` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `fastp_se`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/fastp_pe.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastp_pe.done`
- Representative outputs: `results/finish/fastp_pe.done`
- Execution targets: `fastp_pe`
- Downstream handoff: `max_read_length`

## Guardrails
- Treat `results/finish/fastp_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastp_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `max_read_length` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastp_pe.done` exists and `max_read_length` can proceed without re-running fastp pe.
