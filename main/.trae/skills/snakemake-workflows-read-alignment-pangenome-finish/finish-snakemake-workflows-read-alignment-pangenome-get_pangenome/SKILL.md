---
name: finish-snakemake-workflows-read-alignment-pangenome-get_pangenome
description: Use this skill when orchestrating the retained "get_pangenome" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the get pangenome stage tied to upstream `bwa_index` and the downstream handoff to `get_sra`. It tracks completion via `results/finish/get_pangenome.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: get_pangenome
  step_name: get pangenome
---

# Scope
Use this skill only for the `get_pangenome` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `bwa_index`
- Step file: `finish/read-alignment-pangenome-finish/steps/get_pangenome.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_pangenome.done`
- Representative outputs: `results/finish/get_pangenome.done`
- Execution targets: `get_pangenome`
- Downstream handoff: `get_sra`

## Guardrails
- Treat `results/finish/get_pangenome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_pangenome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_sra` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_pangenome.done` exists and `get_sra` can proceed without re-running get pangenome.
