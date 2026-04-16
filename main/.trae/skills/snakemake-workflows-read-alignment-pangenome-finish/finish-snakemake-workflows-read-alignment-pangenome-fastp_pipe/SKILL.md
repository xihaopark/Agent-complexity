---
name: finish-snakemake-workflows-read-alignment-pangenome-fastp_pipe
description: Use this skill when orchestrating the retained "fastp_pipe" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the fastp pipe stage tied to upstream `get_sra` and the downstream handoff to `fastp_se`. It tracks completion via `results/finish/fastp_pipe.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: fastp_pipe
  step_name: fastp pipe
---

# Scope
Use this skill only for the `fastp_pipe` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `get_sra`
- Step file: `finish/read-alignment-pangenome-finish/steps/fastp_pipe.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fastp_pipe.done`
- Representative outputs: `results/finish/fastp_pipe.done`
- Execution targets: `fastp_pipe`
- Downstream handoff: `fastp_se`

## Guardrails
- Treat `results/finish/fastp_pipe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fastp_pipe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastp_se` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fastp_pipe.done` exists and `fastp_se` can proceed without re-running fastp pipe.
