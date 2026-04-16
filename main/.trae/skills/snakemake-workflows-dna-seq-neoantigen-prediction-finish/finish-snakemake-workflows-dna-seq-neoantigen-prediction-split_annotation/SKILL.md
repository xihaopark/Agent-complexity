---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-split_annotation
description: Use this skill when orchestrating the retained "split_annotation" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the split annotation stage tied to upstream `STAR_index` and the downstream handoff to `genome_faidx`. It tracks completion via `results/finish/split_annotation.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: split_annotation
  step_name: split annotation
---

# Scope
Use this skill only for the `split_annotation` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `STAR_index`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/split_annotation.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/split_annotation.done`
- Representative outputs: `results/finish/split_annotation.done`
- Execution targets: `split_annotation`
- Downstream handoff: `genome_faidx`

## Guardrails
- Treat `results/finish/split_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/split_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `genome_faidx` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/split_annotation.done` exists and `genome_faidx` can proceed without re-running split annotation.
