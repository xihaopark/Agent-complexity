---
name: finish-snakemake-workflows-cyrcular-calling-minimap2_bam
description: Use this skill when orchestrating the retained "minimap2_bam" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the minimap2 bam stage tied to upstream `download_gene_annotation` and the downstream handoff to `merge_fastqs`. It tracks completion via `results/finish/minimap2_bam.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: minimap2_bam
  step_name: minimap2 bam
---

# Scope
Use this skill only for the `minimap2_bam` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `download_gene_annotation`
- Step file: `finish/cyrcular-calling-finish/steps/minimap2_bam.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/minimap2_bam.done`
- Representative outputs: `results/finish/minimap2_bam.done`
- Execution targets: `minimap2_bam`
- Downstream handoff: `merge_fastqs`

## Guardrails
- Treat `results/finish/minimap2_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/minimap2_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_fastqs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/minimap2_bam.done` exists and `merge_fastqs` can proceed without re-running minimap2 bam.
