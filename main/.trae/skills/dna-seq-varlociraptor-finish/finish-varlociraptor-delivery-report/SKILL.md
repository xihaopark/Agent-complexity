---
name: finish-varlociraptor-delivery-report
description: Use this skill when orchestrating the retained "delivery_report" step of the DNA-seq Varlociraptor finish workflow. It defines the final delivery packaging stage, the annotation dependency, and the terminal review artifacts.
metadata:
  workflow_id: dna-seq-varlociraptor-finish
  workflow_name: DNA-seq Varlociraptor Finish Workflow
  step_id: delivery_report
  step_name: Assemble final delivery reports
---

# Scope
Use this skill only for the `delivery_report` step in `dna-seq-varlociraptor-finish`.

## Orchestration
- Upstream requirements: `annotation_filtering`
- Step file: `finish/dna-seq-varlociraptor-finish/steps/delivery_report.smk`
- Config file: `finish/dna-seq-varlociraptor-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/delivery_report.done`
- Representative outputs: `results/maf/{group}/{group}.present.variants.fdr-controlled.maf`, `results/tables/{group}/{group}.present.variants.fdr-controlled.tsv`, `results/tables/{group}/{group}.present.variants.fdr-controlled.xlsx`
- Execution targets: `results/maf/{group}/{group}.present.variants.fdr-controlled.maf`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/delivery_report.done` as the authoritative completion signal for this wrapped finish step.
- Keep this terminal stage packaging-oriented and avoid recomputing upstream calling or annotation state.

## Done Criteria
Mark this step complete only when the delivery tables and MAF artifacts are present for review. Treat datavzrd dashboards as optional packaging extras, not hard blockers for the wrapped finish step.
