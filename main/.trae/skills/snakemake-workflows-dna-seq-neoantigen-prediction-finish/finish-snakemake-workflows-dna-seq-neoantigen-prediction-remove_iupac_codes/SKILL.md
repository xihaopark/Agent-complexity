---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-remove_iupac_codes
description: Use this skill when orchestrating the retained "remove_iupac_codes" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the remove iupac codes stage tied to upstream `get_known_variants` and the downstream handoff to `bwa_index`. It tracks completion via `results/finish/remove_iupac_codes.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: remove_iupac_codes
  step_name: remove iupac codes
---

# Scope
Use this skill only for the `remove_iupac_codes` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `get_known_variants`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/remove_iupac_codes.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/remove_iupac_codes.done`
- Representative outputs: `results/finish/remove_iupac_codes.done`
- Execution targets: `remove_iupac_codes`
- Downstream handoff: `bwa_index`

## Guardrails
- Treat `results/finish/remove_iupac_codes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/remove_iupac_codes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bwa_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/remove_iupac_codes.done` exists and `bwa_index` can proceed without re-running remove iupac codes.
