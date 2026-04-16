---
name: finish-varlociraptor-annotation-filtering
description: Use this skill when orchestrating the retained "annotation_filtering" step of the DNA-seq Varlociraptor finish workflow. It captures how final calls are annotated and filtered before delivery reporting.
metadata:
  workflow_id: dna-seq-varlociraptor-finish
  workflow_name: DNA-seq Varlociraptor Finish Workflow
  step_id: annotation_filtering
  step_name: Annotate and filter final calls
---

# Scope
Use this skill only for the `annotation_filtering` step in `dna-seq-varlociraptor-finish`.

## Orchestration
- Upstream requirements: `calling`
- Step file: `finish/dna-seq-varlociraptor-finish/steps/annotation_filtering.smk`
- Config file: `finish/dna-seq-varlociraptor-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotation_filtering.done`
- Representative outputs: `results/annotated/*`, `results/maf/*`
- Downstream handoff: `delivery_report`

## Guardrails
- Treat `results/finish/annotation_filtering.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage focused on annotation and filtering outputs; delivery packaging belongs to the final step.

## Done Criteria
Mark this step complete only when annotated and filtered outputs are present and the delivery-report step can package them as final artifacts.
