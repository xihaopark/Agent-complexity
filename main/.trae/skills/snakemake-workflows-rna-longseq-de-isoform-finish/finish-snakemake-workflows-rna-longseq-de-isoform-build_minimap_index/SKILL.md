---
name: finish-snakemake-workflows-rna-longseq-de-isoform-build_minimap_index
description: Use this skill when orchestrating the retained "build_minimap_index" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the build minimap index stage tied to upstream `filter_reads` and the downstream handoff to `map_reads`. It tracks completion via `results/finish/build_minimap_index.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: build_minimap_index
  step_name: build minimap index
---

# Scope
Use this skill only for the `build_minimap_index` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `filter_reads`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/build_minimap_index.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/build_minimap_index.done`
- Representative outputs: `results/finish/build_minimap_index.done`
- Execution targets: `build_minimap_index`
- Downstream handoff: `map_reads`

## Guardrails
- Treat `results/finish/build_minimap_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/build_minimap_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `map_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/build_minimap_index.done` exists and `map_reads` can proceed without re-running build minimap index.
