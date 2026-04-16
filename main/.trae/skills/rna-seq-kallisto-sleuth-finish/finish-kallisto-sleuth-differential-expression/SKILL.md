---
name: finish-kallisto-sleuth-differential-expression
description: Use this skill when orchestrating the retained "differential_expression" step of the RNA-seq Kallisto Sleuth finish workflow. It captures the sleuth analysis dependency, the expected differential-expression reports, and the handoff into optional modules.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: RNA-seq Kallisto Sleuth Finish Workflow
  step_id: differential_expression
  step_name: Run sleuth differential expression
---

# Scope
Use this skill only for the `differential_expression` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `init_sleuth`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/differential_expression.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/differential_expression.done`
- Representative outputs: `results/tables/diffexp/model_X.transcripts.diffexp.tsv`, `results/tables/diffexp/model_X.genes-aggregated.diffexp.tsv`, `results/tables/diffexp/model_X.genes-representative.diffexp.tsv`, `results/plots/volcano/model_X.volcano-plots.pdf`, `results/plots/ma/model_X.ma-plots.pdf`, `results/plots/qq/model_X.qq-plots.pdf`
- Execution targets: `results/tables/diffexp/model_X.transcripts.diffexp.tsv`, `results/tables/diffexp/model_X.genes-aggregated.diffexp.tsv`, `results/tables/diffexp/model_X.genes-representative.diffexp.tsv`
- Downstream handoff: `optional_modules`

## Guardrails
- Treat `results/finish/differential_expression.done` as the authoritative completion signal for the wrapped finish step.
- Keep this stage focused on core diffexp outputs and core QC plots; optional enrichment and delivery reporting belong to later steps.

## Done Criteria
Mark this step complete only when the sleuth differential-expression reports are present and optional comparison modules can consume the same analysis outputs.
