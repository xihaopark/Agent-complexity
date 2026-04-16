---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-bam2fq
description: Use this skill when orchestrating the retained "bam2fq" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the bam2fq stage tied to upstream `razers3` and the downstream handoff to `OptiType`. It tracks completion via `results/finish/bam2fq.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: bam2fq
  step_name: bam2fq
---

# Scope
Use this skill only for the `bam2fq` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `razers3`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/bam2fq.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bam2fq.done`
- Representative outputs: `results/finish/bam2fq.done`
- Execution targets: `bam2fq`
- Downstream handoff: `OptiType`

## Guardrails
- Treat `results/finish/bam2fq.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bam2fq.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `OptiType` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bam2fq.done` exists and `OptiType` can proceed without re-running bam2fq.
