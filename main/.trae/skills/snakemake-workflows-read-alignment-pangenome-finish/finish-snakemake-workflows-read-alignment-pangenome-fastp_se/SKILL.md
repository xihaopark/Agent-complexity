---
name: finish-snakemake-workflows-read-alignment-pangenome-fastp_se
description: Use this skill when orchestrating the retained "fastp_se" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the fastp se stage tied to upstream `fastp_pipe` and the downstream handoff to `fastp_pe`. It tracks completion via `results/finish/fastp_se.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: fastp_se
  step_name: fastp se
---

# Scope
Use this skill only for the `fastp_se` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `fastp_pipe`
- Step file: `finish/read-alignment-pangenome-finish/steps/fastp_se.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastp_se.done`
- Representative outputs: `results/finish/fastp_se.done`
- Execution targets: `fastp_se`
- Downstream handoff: `fastp_pe`

## Guardrails
- Treat `results/finish/fastp_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastp_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastp_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastp_se.done` exists and `fastp_pe` can proceed without re-running fastp se.
