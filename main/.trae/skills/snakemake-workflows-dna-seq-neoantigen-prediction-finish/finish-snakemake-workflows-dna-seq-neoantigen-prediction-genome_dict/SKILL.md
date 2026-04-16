---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-genome_dict
description: Use this skill when orchestrating the retained "genome_dict" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the genome dict stage tied to upstream `genome_faidx` and the downstream handoff to `get_callregions`. It tracks completion via `results/finish/genome_dict.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: genome_dict
  step_name: genome dict
---

# Scope
Use this skill only for the `genome_dict` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `genome_faidx`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/genome_dict.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/genome_dict.done`
- Representative outputs: `results/finish/genome_dict.done`
- Execution targets: `genome_dict`
- Downstream handoff: `get_callregions`

## Guardrails
- Treat `results/finish/genome_dict.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/genome_dict.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_callregions` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/genome_dict.done` exists and `get_callregions` can proceed without re-running genome dict.
