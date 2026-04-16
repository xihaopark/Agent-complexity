---
name: finish-sumone-compbio-dge-analysis-using-snakemake-r-gsea
description: Use this skill when orchestrating the retained "gsea" step of the sumone compbio dge analysis using snakemake r finish finish workflow. It keeps the gsea stage tied to upstream `volcano` and the downstream handoff to `all`. It tracks completion via `results/finish/gsea.done`.
metadata:
  workflow_id: sumone-compbio-dge-analysis-using-snakemake-r-finish
  workflow_name: sumone compbio dge analysis using snakemake r finish
  step_id: gsea
  step_name: gsea
---

# Scope
Use this skill only for the `gsea` step in `sumone-compbio-dge-analysis-using-snakemake-r-finish`.

## Orchestration
- Upstream requirements: `volcano`
- Step file: `finish/sumone-compbio-dge-analysis-using-snakemake-r-finish/steps/gsea.smk`
- Config file: `finish/sumone-compbio-dge-analysis-using-snakemake-r-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gsea.done`
- Representative outputs: `results/finish/gsea.done`
- Execution targets: `gsea`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/gsea.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gsea.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gsea.done` exists and `all` can proceed without re-running gsea.
