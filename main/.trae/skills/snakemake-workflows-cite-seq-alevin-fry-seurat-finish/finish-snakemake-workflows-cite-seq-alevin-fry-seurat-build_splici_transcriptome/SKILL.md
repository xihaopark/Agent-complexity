---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-build_splici_transcriptome
description: Use this skill when orchestrating the retained "build_splici_transcriptome" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the build splici transcriptome stage tied to upstream `get_geneid2name` and the downstream handoff to `spoof_t2g`. It tracks completion via `results/finish/build_splici_transcriptome.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: build_splici_transcriptome
  step_name: build splici transcriptome
---

# Scope
Use this skill only for the `build_splici_transcriptome` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `get_geneid2name`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/build_splici_transcriptome.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/build_splici_transcriptome.done`
- Representative outputs: `results/finish/build_splici_transcriptome.done`
- Execution targets: `build_splici_transcriptome`
- Downstream handoff: `spoof_t2g`

## Guardrails
- Treat `results/finish/build_splici_transcriptome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/build_splici_transcriptome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `spoof_t2g` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/build_splici_transcriptome.done` exists and `spoof_t2g` can proceed without re-running build splici transcriptome.
