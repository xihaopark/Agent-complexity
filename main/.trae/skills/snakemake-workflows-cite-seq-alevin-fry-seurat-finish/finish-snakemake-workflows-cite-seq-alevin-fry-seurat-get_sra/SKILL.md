---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-get_sra
description: Use this skill when orchestrating the retained "get_sra" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the get sra stage and the downstream handoff to `get_genome`. It tracks completion via `results/finish/get_sra.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: get_sra
  step_name: get sra
---

# Scope
Use this skill only for the `get_sra` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/get_sra.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_sra.done`
- Representative outputs: `results/finish/get_sra.done`
- Execution targets: `get_sra`
- Downstream handoff: `get_genome`

## Guardrails
- Treat `results/finish/get_sra.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_sra.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_genome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_sra.done` exists and `get_genome` can proceed without re-running get sra.
