---
name: finish-snakemake-workflows-read-alignment-pangenome-fix_mate
description: Use this skill when orchestrating the retained "fix_mate" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the fix mate stage tied to upstream `reheader_mapped_reads` and the downstream handoff to `add_read_group`. It tracks completion via `results/finish/fix_mate.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: fix_mate
  step_name: fix mate
---

# Scope
Use this skill only for the `fix_mate` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `reheader_mapped_reads`
- Step file: `finish/read-alignment-pangenome-finish/steps/fix_mate.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fix_mate.done`
- Representative outputs: `results/finish/fix_mate.done`
- Execution targets: `fix_mate`
- Downstream handoff: `add_read_group`

## Guardrails
- Treat `results/finish/fix_mate.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fix_mate.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `add_read_group` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fix_mate.done` exists and `add_read_group` can proceed without re-running fix mate.
