---
name: finish-snakemake-workflows-read-alignment-pangenome-add_read_group
description: Use this skill when orchestrating the retained "add_read_group" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the add read group stage tied to upstream `fix_mate` and the downstream handoff to `sort_alignments`. It tracks completion via `results/finish/add_read_group.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: add_read_group
  step_name: add read group
---

# Scope
Use this skill only for the `add_read_group` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `fix_mate`
- Step file: `finish/read-alignment-pangenome-finish/steps/add_read_group.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/add_read_group.done`
- Representative outputs: `results/finish/add_read_group.done`
- Execution targets: `add_read_group`
- Downstream handoff: `sort_alignments`

## Guardrails
- Treat `results/finish/add_read_group.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/add_read_group.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sort_alignments` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/add_read_group.done` exists and `sort_alignments` can proceed without re-running add read group.
