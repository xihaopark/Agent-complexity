---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-change_samplenames
description: Use this skill when orchestrating the retained "change_samplenames" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the change samplenames stage tied to upstream `merge_calls` and the downstream handoff to `reheader_varlociraptor`. It tracks completion via `results/finish/change_samplenames.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: change_samplenames
  step_name: change samplenames
---

# Scope
Use this skill only for the `change_samplenames` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `merge_calls`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/change_samplenames.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/change_samplenames.done`
- Representative outputs: `results/finish/change_samplenames.done`
- Execution targets: `change_samplenames`
- Downstream handoff: `reheader_varlociraptor`

## Guardrails
- Treat `results/finish/change_samplenames.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/change_samplenames.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `reheader_varlociraptor` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/change_samplenames.done` exists and `reheader_varlociraptor` can proceed without re-running change samplenames.
