---
name: finish-snakemake-workflows-rna-longseq-de-isoform-concatenate_beds
description: Use this skill when orchestrating the retained "concatenate_beds" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the concatenate beds stage tied to upstream `bam_to_bed` and the downstream handoff to `build_flair_genome_index`. It tracks completion via `results/finish/concatenate_beds.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: concatenate_beds
  step_name: concatenate beds
---

# Scope
Use this skill only for the `concatenate_beds` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `bam_to_bed`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/concatenate_beds.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/concatenate_beds.done`
- Representative outputs: `results/finish/concatenate_beds.done`
- Execution targets: `concatenate_beds`
- Downstream handoff: `build_flair_genome_index`

## Guardrails
- Treat `results/finish/concatenate_beds.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/concatenate_beds.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `build_flair_genome_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/concatenate_beds.done` exists and `build_flair_genome_index` can proceed without re-running concatenate beds.
