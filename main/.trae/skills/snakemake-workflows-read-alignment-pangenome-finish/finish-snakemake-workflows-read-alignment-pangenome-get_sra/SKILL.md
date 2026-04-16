---
name: finish-snakemake-workflows-read-alignment-pangenome-get_sra
description: Use this skill when orchestrating the retained "get_sra" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the get sra stage tied to upstream `get_pangenome` and the downstream handoff to `fastp_pipe`. It tracks completion via `results/finish/get_sra.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: get_sra
  step_name: get sra
---

# Scope
Use this skill only for the `get_sra` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `get_pangenome`
- Step file: `finish/read-alignment-pangenome-finish/steps/get_sra.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_sra.done`
- Representative outputs: `results/finish/get_sra.done`
- Execution targets: `get_sra`
- Downstream handoff: `fastp_pipe`

## Guardrails
- Treat `results/finish/get_sra.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_sra.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastp_pipe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_sra.done` exists and `fastp_pipe` can proceed without re-running get sra.
