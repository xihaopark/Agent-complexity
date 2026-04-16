---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-netmhcpan
description: Use this skill when orchestrating the retained "netMHCpan" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the netMHCpan stage tied to upstream `parse_Optitype` and the downstream handoff to `netMHCIIpan`. It tracks completion via `results/finish/netMHCpan.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: netMHCpan
  step_name: netMHCpan
---

# Scope
Use this skill only for the `netMHCpan` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `parse_Optitype`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/netMHCpan.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/netMHCpan.done`
- Representative outputs: `results/finish/netMHCpan.done`
- Execution targets: `netMHCpan`
- Downstream handoff: `netMHCIIpan`

## Guardrails
- Treat `results/finish/netMHCpan.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/netMHCpan.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `netMHCIIpan` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/netMHCpan.done` exists and `netMHCIIpan` can proceed without re-running netMHCpan.
