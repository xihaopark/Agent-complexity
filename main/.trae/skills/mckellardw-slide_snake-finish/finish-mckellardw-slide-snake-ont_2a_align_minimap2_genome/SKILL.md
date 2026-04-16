---
name: finish-mckellardw-slide-snake-ont_2a_align_minimap2_genome
description: Use this skill when orchestrating the retained "ont_2a_align_minimap2_genome" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2a align minimap2 genome stage tied to upstream `ont_2a_generate_junction_bed` and the downstream handoff to `ont_2a_sort_compress_output`. It tracks completion via `results/finish/ont_2a_align_minimap2_genome.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2a_align_minimap2_genome
  step_name: ont 2a align minimap2 genome
---

# Scope
Use this skill only for the `ont_2a_align_minimap2_genome` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2a_generate_junction_bed`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2a_align_minimap2_genome.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2a_align_minimap2_genome.done`
- Representative outputs: `results/finish/ont_2a_align_minimap2_genome.done`
- Execution targets: `ont_2a_align_minimap2_genome`
- Downstream handoff: `ont_2a_sort_compress_output`

## Guardrails
- Treat `results/finish/ont_2a_align_minimap2_genome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2a_align_minimap2_genome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2a_sort_compress_output` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2a_align_minimap2_genome.done` exists and `ont_2a_sort_compress_output` can proceed without re-running ont 2a align minimap2 genome.
