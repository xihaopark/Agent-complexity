---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-get_known_variants
description: Use this skill when orchestrating the retained "get_known_variants" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the get known variants stage tied to upstream `genome_dict` and the downstream handoff to `remove_iupac_codes`. It tracks completion via `results/finish/get_known_variants.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: get_known_variants
  step_name: get known variants
---

# Scope
Use this skill only for the `get_known_variants` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `genome_dict`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/get_known_variants.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_known_variants.done`
- Representative outputs: `results/finish/get_known_variants.done`
- Execution targets: `get_known_variants`
- Downstream handoff: `remove_iupac_codes`

## Guardrails
- Treat `results/finish/get_known_variants.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_known_variants.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `remove_iupac_codes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_known_variants.done` exists and `remove_iupac_codes` can proceed without re-running get known variants.
