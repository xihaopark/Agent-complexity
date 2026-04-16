---
name: finish-kallisto-sleuth-quantify
description: Use this skill when orchestrating the retained "quantify" step of the RNA-seq Kallisto Sleuth finish workflow. It binds kallisto quantification to prepared reads and defines the abundance outputs that feed sleuth initialization.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: RNA-seq Kallisto Sleuth Finish Workflow
  step_id: quantify
  step_name: Run kallisto quantification
---

# Scope
Use this skill only for the `quantify` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `prepare_reads`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/quantify.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/quantify.done`
- Representative outputs: `results/kallisto_cdna/transcripts.cdna.idx`, `results/kallisto_cdna/A-1`, `results/kallisto_cdna/B-1`, `results/kallisto_cdna/B-2`, `results/kallisto_cdna/C-1`, `results/kallisto_cdna/D-1`
- Execution targets: `results/kallisto_cdna/transcripts.cdna.idx`, `results/kallisto_cdna/A-1`, `results/kallisto_cdna/B-1`, `results/kallisto_cdna/B-2`, `results/kallisto_cdna/C-1`, `results/kallisto_cdna/D-1`
- Downstream handoff: `init_sleuth`

## Guardrails
- Treat `results/finish/quantify.done` as the authoritative completion signal for the wrapped finish step.
- Keep quantification target-driven: build the index plus one kallisto output directory per sample-unit pair, not an `all --until` slice.

## Done Criteria
Mark this step complete only when abundance tables exist for every planned sample and the sleuth initialization stage can reuse them directly.
