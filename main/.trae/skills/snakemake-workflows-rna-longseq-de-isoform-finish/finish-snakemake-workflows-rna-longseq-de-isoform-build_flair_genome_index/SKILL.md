---
name: finish-snakemake-workflows-rna-longseq-de-isoform-build_flair_genome_index
description: Use this skill when orchestrating the retained "build_flair_genome_index" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the build flair genome index stage tied to upstream `concatenate_beds` and the downstream handoff to `flair_align`. It tracks completion via `results/finish/build_flair_genome_index.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: build_flair_genome_index
  step_name: build flair genome index
---

# Scope
Use this skill only for the `build_flair_genome_index` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `concatenate_beds`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/build_flair_genome_index.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/build_flair_genome_index.done`
- Representative outputs: `results/finish/build_flair_genome_index.done`
- Execution targets: `build_flair_genome_index`
- Downstream handoff: `flair_align`

## Guardrails
- Treat `results/finish/build_flair_genome_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/build_flair_genome_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `flair_align` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/build_flair_genome_index.done` exists and `flair_align` can proceed without re-running build flair genome index.
