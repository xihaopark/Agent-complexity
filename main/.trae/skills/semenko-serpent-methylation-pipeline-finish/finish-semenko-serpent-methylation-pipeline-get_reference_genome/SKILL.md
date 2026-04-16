---
name: finish-semenko-serpent-methylation-pipeline-get_reference_genome
description: Use this skill when orchestrating the retained "get_reference_genome" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the get reference genome stage and the downstream handoff to `mask_reference_fasta`. It tracks completion via `results/finish/get_reference_genome.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: get_reference_genome
  step_name: get reference genome
---

# Scope
Use this skill only for the `get_reference_genome` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/get_reference_genome.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_reference_genome.done`
- Representative outputs: `results/finish/get_reference_genome.done`
- Execution targets: `get_reference_genome`
- Downstream handoff: `mask_reference_fasta`

## Guardrails
- Treat `results/finish/get_reference_genome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_reference_genome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `mask_reference_fasta` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_reference_genome.done` exists and `mask_reference_fasta` can proceed without re-running get reference genome.
