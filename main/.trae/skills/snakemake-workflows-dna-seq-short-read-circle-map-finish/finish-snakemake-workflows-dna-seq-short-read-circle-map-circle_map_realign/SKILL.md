---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-circle_map_realign
description: Use this skill when orchestrating the retained "circle_map_realign" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the circle map realign stage tied to upstream `samtools_sort_candidates` and the downstream handoff to `clean_circle_map_realign_output`. It tracks completion via `results/finish/circle_map_realign.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: circle_map_realign
  step_name: circle map realign
---

# Scope
Use this skill only for the `circle_map_realign` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `samtools_sort_candidates`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/circle_map_realign.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/circle_map_realign.done`
- Representative outputs: `results/finish/circle_map_realign.done`
- Execution targets: `circle_map_realign`
- Downstream handoff: `clean_circle_map_realign_output`

## Guardrails
- Treat `results/finish/circle_map_realign.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/circle_map_realign.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `clean_circle_map_realign_output` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/circle_map_realign.done` exists and `clean_circle_map_realign_output` can proceed without re-running circle map realign.
