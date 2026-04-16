---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-get_geneid2name
description: Use this skill when orchestrating the retained "get_geneid2name" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the get geneid2name stage tied to upstream `get_annotation` and the downstream handoff to `build_splici_transcriptome`. It tracks completion via `results/finish/get_geneid2name.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: get_geneid2name
  step_name: get geneid2name
---

# Scope
Use this skill only for the `get_geneid2name` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `get_annotation`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/get_geneid2name.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_geneid2name.done`
- Representative outputs: `results/finish/get_geneid2name.done`
- Execution targets: `get_geneid2name`
- Downstream handoff: `build_splici_transcriptome`

## Guardrails
- Treat `results/finish/get_geneid2name.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_geneid2name.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `build_splici_transcriptome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_geneid2name.done` exists and `build_splici_transcriptome` can proceed without re-running get geneid2name.
