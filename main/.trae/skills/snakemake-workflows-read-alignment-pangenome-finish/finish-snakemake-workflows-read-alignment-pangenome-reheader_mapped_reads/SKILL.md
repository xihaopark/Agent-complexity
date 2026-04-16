---
name: finish-snakemake-workflows-read-alignment-pangenome-reheader_mapped_reads
description: Use this skill when orchestrating the retained "reheader_mapped_reads" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the reheader mapped reads stage tied to upstream `map_reads_vg` and the downstream handoff to `fix_mate`. It tracks completion via `results/finish/reheader_mapped_reads.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: reheader_mapped_reads
  step_name: reheader mapped reads
---

# Scope
Use this skill only for the `reheader_mapped_reads` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `map_reads_vg`
- Step file: `finish/read-alignment-pangenome-finish/steps/reheader_mapped_reads.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/reheader_mapped_reads.done`
- Representative outputs: `results/finish/reheader_mapped_reads.done`
- Execution targets: `reheader_mapped_reads`
- Downstream handoff: `fix_mate`

## Guardrails
- Treat `results/finish/reheader_mapped_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/reheader_mapped_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fix_mate` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/reheader_mapped_reads.done` exists and `fix_mate` can proceed without re-running reheader mapped reads.
