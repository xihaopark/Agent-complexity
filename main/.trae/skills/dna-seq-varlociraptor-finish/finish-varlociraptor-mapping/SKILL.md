---
name: finish-varlociraptor-mapping
description: Use this skill when orchestrating the retained "mapping" step of the DNA-seq Varlociraptor finish workflow. It ties prepared reads to genome alignment outputs and defines the BAM artifacts that feed candidate calling.
metadata:
  workflow_id: dna-seq-varlociraptor-finish
  workflow_name: DNA-seq Varlociraptor Finish Workflow
  step_id: mapping
  step_name: Map reads to the reference genome
---

# Scope
Use this skill only for the `mapping` step in `dna-seq-varlociraptor-finish`.

## Orchestration
- Upstream requirements: `prepare_reads`
- Step file: `finish/dna-seq-varlociraptor-finish/steps/mapping.smk`
- Config file: `finish/dna-seq-varlociraptor-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/mapping.done`
- Representative outputs: `results/alignment/*.bam`, `results/alignment/*.bai`
- Downstream handoff: `candidate_calling`

## Guardrails
- Treat `results/finish/mapping.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage focused on durable alignment artifacts that candidate calling can reuse directly.

## Done Criteria
Mark this step complete only when indexed BAM outputs exist for the planned samples and candidate calling can start from the produced alignments.
