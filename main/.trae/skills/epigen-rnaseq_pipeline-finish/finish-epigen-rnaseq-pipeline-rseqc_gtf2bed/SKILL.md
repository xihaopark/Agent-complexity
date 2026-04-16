---
name: finish-epigen-rnaseq-pipeline-rseqc_gtf2bed
description: Use this skill when orchestrating the retained "rseqc_gtf2bed" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the rseqc gtf2bed stage tied to upstream `star_index` and the downstream handoff to `rseqc_junction_annotation`. It tracks completion via `results/finish/rseqc_gtf2bed.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: rseqc_gtf2bed
  step_name: rseqc gtf2bed
---

# Scope
Use this skill only for the `rseqc_gtf2bed` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `star_index`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/rseqc_gtf2bed.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rseqc_gtf2bed.done`
- Representative outputs: `results/finish/rseqc_gtf2bed.done`
- Execution targets: `rseqc_gtf2bed`
- Downstream handoff: `rseqc_junction_annotation`

## Guardrails
- Treat `results/finish/rseqc_gtf2bed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rseqc_gtf2bed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rseqc_junction_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rseqc_gtf2bed.done` exists and `rseqc_junction_annotation` can proceed without re-running rseqc gtf2bed.
