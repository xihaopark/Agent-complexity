---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-reheader_varlociraptor
description: Use this skill when orchestrating the retained "reheader_varlociraptor" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the reheader varlociraptor stage tied to upstream `change_samplenames` and the downstream handoff to `microphaser_somatic`. It tracks completion via `results/finish/reheader_varlociraptor.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: reheader_varlociraptor
  step_name: reheader varlociraptor
---

# Scope
Use this skill only for the `reheader_varlociraptor` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `change_samplenames`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/reheader_varlociraptor.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/reheader_varlociraptor.done`
- Representative outputs: `results/finish/reheader_varlociraptor.done`
- Execution targets: `reheader_varlociraptor`
- Downstream handoff: `microphaser_somatic`

## Guardrails
- Treat `results/finish/reheader_varlociraptor.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/reheader_varlociraptor.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `microphaser_somatic` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/reheader_varlociraptor.done` exists and `microphaser_somatic` can proceed without re-running reheader varlociraptor.
