---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-razers3
description: Use this skill when orchestrating the retained "razers3" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the razers3 stage tied to upstream `parse_HLA_LA` and the downstream handoff to `bam2fq`. It tracks completion via `results/finish/razers3.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: razers3
  step_name: razers3
---

# Scope
Use this skill only for the `razers3` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `parse_HLA_LA`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/razers3.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/razers3.done`
- Representative outputs: `results/finish/razers3.done`
- Execution targets: `razers3`
- Downstream handoff: `bam2fq`

## Guardrails
- Treat `results/finish/razers3.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/razers3.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bam2fq` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/razers3.done` exists and `bam2fq` can proceed without re-running razers3.
