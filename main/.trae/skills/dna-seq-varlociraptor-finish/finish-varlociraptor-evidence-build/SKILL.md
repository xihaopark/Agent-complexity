---
name: finish-varlociraptor-evidence-build
description: Use this skill when orchestrating the retained "evidence_build" step of the DNA-seq Varlociraptor finish workflow. It turns candidate variants into evidence tracks and prepares the final calling stage with the expected intermediate artifacts.
metadata:
  workflow_id: dna-seq-varlociraptor-finish
  workflow_name: DNA-seq Varlociraptor Finish Workflow
  step_id: evidence_build
  step_name: Build evidence tracks for final calling
---

# Scope
Use this skill only for the `evidence_build` step in `dna-seq-varlociraptor-finish`.

## Orchestration
- Upstream requirements: `candidate_calling`
- Step file: `finish/dna-seq-varlociraptor-finish/steps/evidence_build.smk`
- Config file: `finish/dna-seq-varlociraptor-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/evidence_build.done`
- Representative outputs: `results/evidence/*`
- Downstream handoff: `calling`

## Guardrails
- Treat `results/finish/evidence_build.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage focused on evidence artifacts required by final calling, not on final variant packaging.

## Done Criteria
Mark this step complete only when evidence outputs are present and the final calling stage can use them without regenerating candidate calls.
