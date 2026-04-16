---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-parse_hla_la
description: Use this skill when orchestrating the retained "parse_HLA_LA" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the parse HLA LA stage tied to upstream `HLA_LA` and the downstream handoff to `razers3`. It tracks completion via `results/finish/parse_HLA_LA.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: parse_HLA_LA
  step_name: parse HLA LA
---

# Scope
Use this skill only for the `parse_HLA_LA` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `HLA_LA`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/parse_HLA_LA.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/parse_HLA_LA.done`
- Representative outputs: `results/finish/parse_HLA_LA.done`
- Execution targets: `parse_HLA_LA`
- Downstream handoff: `razers3`

## Guardrails
- Treat `results/finish/parse_HLA_LA.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/parse_HLA_LA.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `razers3` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/parse_HLA_LA.done` exists and `razers3` can proceed without re-running parse HLA LA.
