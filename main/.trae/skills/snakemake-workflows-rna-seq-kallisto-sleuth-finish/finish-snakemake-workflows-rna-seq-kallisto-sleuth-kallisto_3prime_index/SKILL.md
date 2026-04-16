---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-kallisto_3prime_index
description: Use this skill when orchestrating the retained "kallisto_3prime_index" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the kallisto 3prime index stage tied to upstream `get_main_transcript_fastq` and the downstream handoff to `kallisto_3prime_quant`. It tracks completion via `results/finish/kallisto_3prime_index.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: kallisto_3prime_index
  step_name: kallisto 3prime index
---

# Scope
Use this skill only for the `kallisto_3prime_index` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `get_main_transcript_fastq`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/kallisto_3prime_index.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/kallisto_3prime_index.done`
- Representative outputs: `results/finish/kallisto_3prime_index.done`
- Execution targets: `kallisto_3prime_index`
- Downstream handoff: `kallisto_3prime_quant`

## Guardrails
- Treat `results/finish/kallisto_3prime_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/kallisto_3prime_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `kallisto_3prime_quant` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/kallisto_3prime_index.done` exists and `kallisto_3prime_quant` can proceed without re-running kallisto 3prime index.
