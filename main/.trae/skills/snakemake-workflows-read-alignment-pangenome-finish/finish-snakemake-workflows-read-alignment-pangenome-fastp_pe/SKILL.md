---
name: finish-snakemake-workflows-read-alignment-pangenome-fastp_pe
description: Use this skill when orchestrating the retained "fastp_pe" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the fastp pe stage tied to upstream `fastp_se` and the downstream handoff to `merge_trimmed_fastqs`. It tracks completion via `results/finish/fastp_pe.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: fastp_pe
  step_name: fastp pe
---

# Scope
Use this skill only for the `fastp_pe` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `fastp_se`
- Step file: `finish/read-alignment-pangenome-finish/steps/fastp_pe.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastp_pe.done`
- Representative outputs: `results/finish/fastp_pe.done`
- Execution targets: `fastp_pe`
- Downstream handoff: `merge_trimmed_fastqs`

## Guardrails
- Treat `results/finish/fastp_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastp_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_trimmed_fastqs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastp_pe.done` exists and `merge_trimmed_fastqs` can proceed without re-running fastp pe.
