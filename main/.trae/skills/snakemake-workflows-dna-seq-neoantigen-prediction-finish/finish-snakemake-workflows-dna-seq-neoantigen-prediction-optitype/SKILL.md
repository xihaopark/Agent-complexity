---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-optitype
description: Use this skill when orchestrating the retained "OptiType" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the OptiType stage tied to upstream `bam2fq` and the downstream handoff to `parse_Optitype`. It tracks completion via `results/finish/OptiType.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: OptiType
  step_name: OptiType
---

# Scope
Use this skill only for the `OptiType` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `bam2fq`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/OptiType.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/OptiType.done`
- Representative outputs: `results/finish/OptiType.done`
- Execution targets: `OptiType`
- Downstream handoff: `parse_Optitype`

## Guardrails
- Treat `results/finish/OptiType.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/OptiType.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `parse_Optitype` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/OptiType.done` exists and `parse_Optitype` can proceed without re-running OptiType.
