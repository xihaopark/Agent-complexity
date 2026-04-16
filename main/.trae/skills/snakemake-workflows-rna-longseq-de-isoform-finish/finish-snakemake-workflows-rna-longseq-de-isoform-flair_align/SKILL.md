---
name: finish-snakemake-workflows-rna-longseq-de-isoform-flair_align
description: Use this skill when orchestrating the retained "flair_align" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the flair align stage tied to upstream `build_flair_genome_index` and the downstream handoff to `flair_correct`. It tracks completion via `results/finish/flair_align.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: flair_align
  step_name: flair align
---

# Scope
Use this skill only for the `flair_align` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `build_flair_genome_index`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/flair_align.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/flair_align.done`
- Representative outputs: `results/finish/flair_align.done`
- Execution targets: `flair_align`
- Downstream handoff: `flair_correct`

## Guardrails
- Treat `results/finish/flair_align.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/flair_align.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `flair_correct` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/flair_align.done` exists and `flair_correct` can proceed without re-running flair align.
