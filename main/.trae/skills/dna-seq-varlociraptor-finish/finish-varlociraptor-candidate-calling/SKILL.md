---
name: finish-varlociraptor-candidate-calling
description: Use this skill when orchestrating the retained "candidate_calling" step of the DNA-seq Varlociraptor finish workflow. It defines how mapped reads become candidate variant calls and how those candidates hand off into evidence construction.
metadata:
  workflow_id: dna-seq-varlociraptor-finish
  workflow_name: DNA-seq Varlociraptor Finish Workflow
  step_id: candidate_calling
  step_name: Generate candidate variants
---

# Scope
Use this skill only for the `candidate_calling` step in `dna-seq-varlociraptor-finish`.

## Orchestration
- Upstream requirements: `mapping`
- Step file: `finish/dna-seq-varlociraptor-finish/steps/candidate_calling.smk`
- Config file: `finish/dna-seq-varlociraptor-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/candidate_calling.done`
- Representative outputs: `results/candidates/*.bcf`
- Downstream handoff: `evidence_build`

## Guardrails
- Treat `results/finish/candidate_calling.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage limited to candidate generation; evidence construction remains the downstream responsibility.

## Done Criteria
Mark this step complete only when candidate BCF outputs exist and the evidence-building stage can consume them without re-running mapping.
