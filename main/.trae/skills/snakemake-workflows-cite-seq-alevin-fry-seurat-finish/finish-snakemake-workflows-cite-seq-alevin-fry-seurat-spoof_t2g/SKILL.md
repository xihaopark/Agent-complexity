---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-spoof_t2g
description: Use this skill when orchestrating the retained "spoof_t2g" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the spoof t2g stage tied to upstream `build_splici_transcriptome` and the downstream handoff to `salmon_index`. It tracks completion via `results/finish/spoof_t2g.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: spoof_t2g
  step_name: spoof t2g
---

# Scope
Use this skill only for the `spoof_t2g` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `build_splici_transcriptome`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/spoof_t2g.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/spoof_t2g.done`
- Representative outputs: `results/finish/spoof_t2g.done`
- Execution targets: `spoof_t2g`
- Downstream handoff: `salmon_index`

## Guardrails
- Treat `results/finish/spoof_t2g.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/spoof_t2g.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `salmon_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/spoof_t2g.done` exists and `salmon_index` can proceed without re-running spoof t2g.
