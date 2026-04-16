---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-samtools_sort_candidates
description: Use this skill when orchestrating the retained "samtools_sort_candidates" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the samtools sort candidates stage tied to upstream `circle_map_extract_reads` and the downstream handoff to `circle_map_realign`. It tracks completion via `results/finish/samtools_sort_candidates.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: samtools_sort_candidates
  step_name: samtools sort candidates
---

# Scope
Use this skill only for the `samtools_sort_candidates` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `circle_map_extract_reads`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/samtools_sort_candidates.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/samtools_sort_candidates.done`
- Representative outputs: `results/finish/samtools_sort_candidates.done`
- Execution targets: `samtools_sort_candidates`
- Downstream handoff: `circle_map_realign`

## Guardrails
- Treat `results/finish/samtools_sort_candidates.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/samtools_sort_candidates.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `circle_map_realign` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/samtools_sort_candidates.done` exists and `circle_map_realign` can proceed without re-running samtools sort candidates.
