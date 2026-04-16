---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-netmhciipan
description: Use this skill when orchestrating the retained "netMHCIIpan" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the netMHCIIpan stage tied to upstream `netMHCpan` and the downstream handoff to `parse_mhc_out`. It tracks completion via `results/finish/netMHCIIpan.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: netMHCIIpan
  step_name: netMHCIIpan
---

# Scope
Use this skill only for the `netMHCIIpan` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `netMHCpan`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/netMHCIIpan.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/netMHCIIpan.done`
- Representative outputs: `results/finish/netMHCIIpan.done`
- Execution targets: `netMHCIIpan`
- Downstream handoff: `parse_mhc_out`

## Guardrails
- Treat `results/finish/netMHCIIpan.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/netMHCIIpan.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `parse_mhc_out` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/netMHCIIpan.done` exists and `parse_mhc_out` can proceed without re-running netMHCIIpan.
