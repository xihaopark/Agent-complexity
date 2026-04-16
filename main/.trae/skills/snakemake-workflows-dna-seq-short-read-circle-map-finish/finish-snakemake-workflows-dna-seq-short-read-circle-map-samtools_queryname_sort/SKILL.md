---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-samtools_queryname_sort
description: Use this skill when orchestrating the retained "samtools_queryname_sort" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the samtools queryname sort stage tied to upstream `apply_bqsr` and the downstream handoff to `circle_map_extract_reads`. It tracks completion via `results/finish/samtools_queryname_sort.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: samtools_queryname_sort
  step_name: samtools queryname sort
---

# Scope
Use this skill only for the `samtools_queryname_sort` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `apply_bqsr`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/samtools_queryname_sort.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_queryname_sort.done`
- Representative outputs: `results/finish/samtools_queryname_sort.done`
- Execution targets: `samtools_queryname_sort`
- Downstream handoff: `circle_map_extract_reads`

## Guardrails
- Treat `results/finish/samtools_queryname_sort.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_queryname_sort.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `circle_map_extract_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_queryname_sort.done` exists and `circle_map_extract_reads` can proceed without re-running samtools queryname sort.
