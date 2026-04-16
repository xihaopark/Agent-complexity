---
name: finish-sumone-compbio-dge-analysis-using-snakemake-r-deseq2
description: Use this skill when orchestrating the retained "deseq2" step of the sumone compbio dge analysis using snakemake r finish finish workflow. It keeps the deseq2 stage and the downstream handoff to `volcano`. It tracks completion via `results/finish/deseq2.done`.
metadata:
  workflow_id: sumone-compbio-dge-analysis-using-snakemake-r-finish
  workflow_name: sumone compbio dge analysis using snakemake r finish
  step_id: deseq2
  step_name: deseq2
---

# Scope
Use this skill only for the `deseq2` step in `sumone-compbio-dge-analysis-using-snakemake-r-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/sumone-compbio-dge-analysis-using-snakemake-r-finish/steps/deseq2.smk`
- Config file: `finish/sumone-compbio-dge-analysis-using-snakemake-r-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/deseq2.done`
- Representative outputs: `results/finish/deseq2.done`
- Execution targets: `deseq2`
- Downstream handoff: `volcano`

## Guardrails
- Treat `results/finish/deseq2.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/deseq2.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `volcano` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/deseq2.done` exists and `volcano` can proceed without re-running deseq2.
