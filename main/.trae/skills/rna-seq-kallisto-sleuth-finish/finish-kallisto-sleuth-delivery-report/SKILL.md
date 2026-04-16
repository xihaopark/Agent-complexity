---
name: finish-kallisto-sleuth-delivery-report
description: Use this skill when orchestrating the retained "delivery_report" step of the RNA-seq Kallisto Sleuth finish workflow. It defines the final packaging stage, the optional-modules dependency, and the terminal delivery artifacts that close the workflow.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: RNA-seq Kallisto Sleuth Finish Workflow
  step_id: delivery_report
  step_name: Assemble final delivery report
---

# Scope
Use this skill only for the `delivery_report` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `optional_modules`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/delivery_report.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/delivery_report.done`
- Representative outputs: `results/tables/diffexp/model_X.genes-representative.diffexp_postprocessed.tsv`, `results/tables/diffexp/model_X.transcripts.diffexp_postprocessed.tsv`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/delivery_report.done` as the authoritative completion signal for the wrapped finish step.
- Keep this stage packaging-oriented: finalize delivery tables without recomputing upstream quantification or diffexp state.

## Done Criteria
Mark this step complete only when the delivery-facing diffexp tables exist and summarize the latest analysis state for handoff or review. Treat datavzrd HTML reports as optional extras.
