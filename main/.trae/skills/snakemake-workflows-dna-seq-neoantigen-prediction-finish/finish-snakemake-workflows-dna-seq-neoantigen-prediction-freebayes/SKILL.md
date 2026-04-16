---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-freebayes
description: Use this skill when orchestrating the retained "freebayes" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the freebayes stage tied to upstream `norm_vcf` and the downstream handoff to `scatter_candidates`. It tracks completion via `results/finish/freebayes.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: freebayes
  step_name: freebayes
---

# Scope
Use this skill only for the `freebayes` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `norm_vcf`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/freebayes.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/freebayes.done`
- Representative outputs: `results/finish/freebayes.done`
- Execution targets: `freebayes`
- Downstream handoff: `scatter_candidates`

## Guardrails
- Treat `results/finish/freebayes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/freebayes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `scatter_candidates` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/freebayes.done` exists and `scatter_candidates` can proceed without re-running freebayes.
