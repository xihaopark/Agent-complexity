---
name: finish-maxplanck-ie-snakepipes-macs2_peak_qc
description: Use this skill when orchestrating the retained "MACS2_peak_qc" step of the maxplanck ie snakepipes finish finish workflow. It keeps the MACS2 peak qc stage tied to upstream `plotFingerprint_allelic` and the downstream handoff to `CSAW`. It tracks completion via `results/finish/MACS2_peak_qc.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: MACS2_peak_qc
  step_name: MACS2 peak qc
---

# Scope
Use this skill only for the `MACS2_peak_qc` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `plotFingerprint_allelic`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/MACS2_peak_qc.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/MACS2_peak_qc.done`
- Representative outputs: `results/finish/MACS2_peak_qc.done`
- Execution targets: `MACS2_peak_qc`
- Downstream handoff: `CSAW`

## Guardrails
- Treat `results/finish/MACS2_peak_qc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/MACS2_peak_qc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `CSAW` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/MACS2_peak_qc.done` exists and `CSAW` can proceed without re-running MACS2 peak qc.
