---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-get_genome
description: Use this skill when orchestrating the retained "get_genome" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the get genome stage tied to upstream `get_sra` and the downstream handoff to `get_annotation`. It tracks completion via `results/finish/get_genome.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: get_genome
  step_name: get genome
---

# Scope
Use this skill only for the `get_genome` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `get_sra`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/get_genome.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_genome.done`
- Representative outputs: `results/finish/get_genome.done`
- Execution targets: `get_genome`
- Downstream handoff: `get_annotation`

## Guardrails
- Treat `results/finish/get_genome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_genome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_genome.done` exists and `get_annotation` can proceed without re-running get genome.
