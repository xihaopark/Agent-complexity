---
name: finish-snakemake-workflows-dna-seq-benchmark-get_vep_plugins
description: Use this skill when orchestrating the retained "get_vep_plugins" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the get vep plugins stage tied to upstream `get_vep_cache` and the downstream handoff to `download_revel`. It tracks completion via `results/finish/get_vep_plugins.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: get_vep_plugins
  step_name: get vep plugins
---

# Scope
Use this skill only for the `get_vep_plugins` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `get_vep_cache`
- Step file: `finish/dna-seq-benchmark-finish/steps/get_vep_plugins.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_vep_plugins.done`
- Representative outputs: `results/finish/get_vep_plugins.done`
- Execution targets: `get_vep_plugins`
- Downstream handoff: `download_revel`

## Guardrails
- Treat `results/finish/get_vep_plugins.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_vep_plugins.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `download_revel` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_vep_plugins.done` exists and `download_revel` can proceed without re-running get vep plugins.
