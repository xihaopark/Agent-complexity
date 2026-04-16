---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-tabix_known_variants
description: Use this skill when orchestrating the retained "tabix_known_variants" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the tabix known variants stage tied to upstream `remove_iupac_codes` and the downstream handoff to `cutadapt_pe`. It tracks completion via `results/finish/tabix_known_variants.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: tabix_known_variants
  step_name: tabix known variants
---

# Scope
Use this skill only for the `tabix_known_variants` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `remove_iupac_codes`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/tabix_known_variants.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/tabix_known_variants.done`
- Representative outputs: `results/finish/tabix_known_variants.done`
- Execution targets: `tabix_known_variants`
- Downstream handoff: `cutadapt_pe`

## Guardrails
- Treat `results/finish/tabix_known_variants.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/tabix_known_variants.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cutadapt_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/tabix_known_variants.done` exists and `cutadapt_pe` can proceed without re-running tabix known variants.
