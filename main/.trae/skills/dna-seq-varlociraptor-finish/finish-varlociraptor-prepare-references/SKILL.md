---
name: finish-varlociraptor-prepare-references
description: Use this skill when orchestrating the retained "prepare_references" step of the DNA-seq Varlociraptor finish workflow. It turns inspected inputs into a reusable reference bundle and hands off a stable reference state to read preparation.
metadata:
  workflow_id: dna-seq-varlociraptor-finish
  workflow_name: DNA-seq Varlociraptor Finish Workflow
  step_id: prepare_references
  step_name: Prepare reference bundle
---

# Scope
Use this skill only for the `prepare_references` step in `dna-seq-varlociraptor-finish`.

## Orchestration
- Upstream requirements: `inspect_inputs`
- Step file: `finish/dna-seq-varlociraptor-finish/steps/prepare_references.smk`
- Config file: `finish/dna-seq-varlociraptor-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepare_references.done`
- Representative outputs: `resources/reference_bundle/*`
- Execution targets: `prepare_references_ready`
- Downstream handoff: `prepare_reads`

## Guardrails
- Treat `results/finish/prepare_references.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to the configured reference bundle and optional plugin resources required by downstream calling.

## Done Criteria
Mark this step complete only when the reference bundle is ready and the read-preparation stage can begin without re-inspecting inputs.
