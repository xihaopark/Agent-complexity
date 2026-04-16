---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-circle_map_extract_reads
description: Use this skill when orchestrating the retained "circle_map_extract_reads" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the circle map extract reads stage tied to upstream `samtools_queryname_sort` and the downstream handoff to `samtools_sort_candidates`. It tracks completion via `results/finish/circle_map_extract_reads.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: circle_map_extract_reads
  step_name: circle map extract reads
---

# Scope
Use this skill only for the `circle_map_extract_reads` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `samtools_queryname_sort`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/circle_map_extract_reads.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/circle_map_extract_reads.done`
- Representative outputs: `results/finish/circle_map_extract_reads.done`
- Execution targets: `circle_map_extract_reads`
- Downstream handoff: `samtools_sort_candidates`

## Guardrails
- Treat `results/finish/circle_map_extract_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/circle_map_extract_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_sort_candidates` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/circle_map_extract_reads.done` exists and `samtools_sort_candidates` can proceed without re-running circle map extract reads.
