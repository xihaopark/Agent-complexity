---
name: finish-snakemake-workflows-rna-longseq-de-isoform-map_reads
description: Use this skill when orchestrating the retained "map_reads" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the map reads stage tied to upstream `build_minimap_index` and the downstream handoff to `sam_to_bam`. It tracks completion via `results/finish/map_reads.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: map_reads
  step_name: map reads
---

# Scope
Use this skill only for the `map_reads` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `build_minimap_index`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/map_reads.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/map_reads.done`
- Representative outputs: `results/finish/map_reads.done`
- Execution targets: `map_reads`
- Downstream handoff: `sam_to_bam`

## Guardrails
- Treat `results/finish/map_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/map_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sam_to_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/map_reads.done` exists and `sam_to_bam` can proceed without re-running map reads.
