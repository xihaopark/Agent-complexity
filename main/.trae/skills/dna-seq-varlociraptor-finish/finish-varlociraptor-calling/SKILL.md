---
name: finish-varlociraptor-calling
description: Use this skill when orchestrating the retained "calling" step of the DNA-seq Varlociraptor finish workflow. It binds evidence construction to final varlociraptor calling outputs and prepares the annotation and filtering stage.
metadata:
  workflow_id: dna-seq-varlociraptor-finish
  workflow_name: DNA-seq Varlociraptor Finish Workflow
  step_id: calling
  step_name: Run final varlociraptor calling
---

# Scope
Use this skill only for the `calling` step in `dna-seq-varlociraptor-finish`.

## Orchestration
- Upstream requirements: `evidence_build`
- Step file: `finish/dna-seq-varlociraptor-finish/steps/calling.smk`
- Config file: `finish/dna-seq-varlociraptor-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/calling.done`
- Representative outputs: `results/final-calls/{group}/{group}.variants.annotated.bcf`
- Downstream handoff: `annotation_filtering`

## Guardrails
- Treat `results/finish/calling.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to final callset generation so annotation and filtering remain separable.

## Done Criteria
Mark this step complete only when grouped annotated BCF callsets exist and the annotation-filtering stage can proceed without rebuilding evidence tracks.
