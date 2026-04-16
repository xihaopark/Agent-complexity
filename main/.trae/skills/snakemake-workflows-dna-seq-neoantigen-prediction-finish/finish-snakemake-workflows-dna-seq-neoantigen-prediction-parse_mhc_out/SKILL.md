---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-parse_mhc_out
description: Use this skill when orchestrating the retained "parse_mhc_out" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the parse mhc out stage tied to upstream `netMHCIIpan` and the downstream handoff to `mhc_csv_table`. It tracks completion via `results/finish/parse_mhc_out.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: parse_mhc_out
  step_name: parse mhc out
---

# Scope
Use this skill only for the `parse_mhc_out` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `netMHCIIpan`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/parse_mhc_out.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/parse_mhc_out.done`
- Representative outputs: `results/finish/parse_mhc_out.done`
- Execution targets: `parse_mhc_out`
- Downstream handoff: `mhc_csv_table`

## Guardrails
- Treat `results/finish/parse_mhc_out.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/parse_mhc_out.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `mhc_csv_table` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/parse_mhc_out.done` exists and `mhc_csv_table` can proceed without re-running parse mhc out.
