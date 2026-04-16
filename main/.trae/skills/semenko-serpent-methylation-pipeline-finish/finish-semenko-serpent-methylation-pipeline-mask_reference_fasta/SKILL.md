---
name: finish-semenko-serpent-methylation-pipeline-mask_reference_fasta
description: Use this skill when orchestrating the retained "mask_reference_fasta" step of the semenko serpent methylation pipeline finish finish workflow. It keeps the mask reference fasta stage tied to upstream `get_reference_genome` and the downstream handoff to `biscuit_index`. It tracks completion via `results/finish/mask_reference_fasta.done`.
metadata:
  workflow_id: semenko-serpent-methylation-pipeline-finish
  workflow_name: semenko serpent methylation pipeline finish
  step_id: mask_reference_fasta
  step_name: mask reference fasta
---

# Scope
Use this skill only for the `mask_reference_fasta` step in `semenko-serpent-methylation-pipeline-finish`.

## Orchestration
- Upstream requirements: `get_reference_genome`
- Step file: `finish/semenko-serpent-methylation-pipeline-finish/steps/mask_reference_fasta.smk`
- Config file: `finish/semenko-serpent-methylation-pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/mask_reference_fasta.done`
- Representative outputs: `results/finish/mask_reference_fasta.done`
- Execution targets: `mask_reference_fasta`
- Downstream handoff: `biscuit_index`

## Guardrails
- Treat `results/finish/mask_reference_fasta.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/mask_reference_fasta.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `biscuit_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/mask_reference_fasta.done` exists and `biscuit_index` can proceed without re-running mask reference fasta.
