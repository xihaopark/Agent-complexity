---
name: finish-sumone-compbio-dge-analysis-using-snakemake-r-volcano
description: Use this skill when orchestrating the retained "volcano" step of the sumone compbio dge analysis using snakemake r finish finish workflow. It keeps the volcano stage tied to upstream `deseq2` and the downstream handoff to `gsea`. It tracks completion via `results/finish/volcano.done`.
metadata:
  workflow_id: sumone-compbio-dge-analysis-using-snakemake-r-finish
  workflow_name: sumone compbio dge analysis using snakemake r finish
  step_id: volcano
  step_name: volcano
---

# Scope
Use this skill only for the `volcano` step in `sumone-compbio-dge-analysis-using-snakemake-r-finish`.

## Orchestration
- Upstream requirements: `deseq2`
- Step file: `finish/sumone-compbio-dge-analysis-using-snakemake-r-finish/steps/volcano.smk`
- Config file: `finish/sumone-compbio-dge-analysis-using-snakemake-r-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/volcano.done`
- Representative outputs: `results/finish/volcano.done`
- Execution targets: `volcano`
- Downstream handoff: `gsea`

## Guardrails
- Treat `results/finish/volcano.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/volcano.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gsea` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/volcano.done` exists and `gsea` can proceed without re-running volcano.
