---
name: finish-snakemake-workflows-rna-seq-star-deseq2-get_annotation
description: Use this skill when orchestrating the retained "get_annotation" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the get annotation stage tied to upstream `get_genome` and the downstream handoff to `genome_faidx`. It tracks completion via `results/finish/get_annotation.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: get_annotation
  step_name: get annotation
---

# Scope
Use this skill only for the `get_annotation` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `get_genome`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/get_annotation.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_annotation.done`
- Representative outputs: `results/finish/get_annotation.done`
- Execution targets: `get_annotation`
- Downstream handoff: `genome_faidx`

## Guardrails
- Treat `results/finish/get_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `genome_faidx` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_annotation.done` exists and `genome_faidx` can proceed without re-running get annotation.
