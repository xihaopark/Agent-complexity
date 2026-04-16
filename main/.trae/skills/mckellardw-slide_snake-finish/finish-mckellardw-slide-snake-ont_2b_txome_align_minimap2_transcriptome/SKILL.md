---
name: finish-mckellardw-slide-snake-ont_2b_txome_align_minimap2_transcriptome
description: Use this skill when orchestrating the retained "ont_2b_txome_align_minimap2_transcriptome" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2b txome align minimap2 transcriptome stage tied to upstream `ont_2a_cache_seurat` and the downstream handoff to `ont_2b_txome_add_corrected_barcodes`. It tracks completion via `results/finish/ont_2b_txome_align_minimap2_transcriptome.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2b_txome_align_minimap2_transcriptome
  step_name: ont 2b txome align minimap2 transcriptome
---

# Scope
Use this skill only for the `ont_2b_txome_align_minimap2_transcriptome` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2a_cache_seurat`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2b_txome_align_minimap2_transcriptome.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2b_txome_align_minimap2_transcriptome.done`
- Representative outputs: `results/finish/ont_2b_txome_align_minimap2_transcriptome.done`
- Execution targets: `ont_2b_txome_align_minimap2_transcriptome`
- Downstream handoff: `ont_2b_txome_add_corrected_barcodes`

## Guardrails
- Treat `results/finish/ont_2b_txome_align_minimap2_transcriptome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2b_txome_align_minimap2_transcriptome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2b_txome_add_corrected_barcodes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2b_txome_align_minimap2_transcriptome.done` exists and `ont_2b_txome_add_corrected_barcodes` can proceed without re-running ont 2b txome align minimap2 transcriptome.
