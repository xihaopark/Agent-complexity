---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-parse_optitype
description: Use this skill when orchestrating the retained "parse_Optitype" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the parse Optitype stage tied to upstream `OptiType` and the downstream handoff to `netMHCpan`. It tracks completion via `results/finish/parse_Optitype.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: parse_Optitype
  step_name: parse Optitype
---

# Scope
Use this skill only for the `parse_Optitype` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `OptiType`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/parse_Optitype.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/parse_Optitype.done`
- Representative outputs: `results/finish/parse_Optitype.done`
- Execution targets: `parse_Optitype`
- Downstream handoff: `netMHCpan`

## Guardrails
- Treat `results/finish/parse_Optitype.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/parse_Optitype.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `netMHCpan` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/parse_Optitype.done` exists and `netMHCpan` can proceed without re-running parse Optitype.
