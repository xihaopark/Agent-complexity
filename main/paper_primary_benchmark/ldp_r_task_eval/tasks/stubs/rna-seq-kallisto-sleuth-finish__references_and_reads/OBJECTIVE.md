# R-task stub: `rna-seq-kallisto-sleuth-finish` / `references_and_reads`

> **Status:** stub — evaluation inputs, metrics, and gold outputs are **not** filled in yet.
> Pipeline overlay comes from `paper_primary_benchmark/task_definitions/rna-seq-kallisto-sleuth-finish.json`.

## Stage

- **Label:** 参考序列与读段准备
- **Order:** 2
- **Finish manifest (reference):** `finish/rna-seq-kallisto-sleuth-finish/manifest.json`

## Snakemake steps in this stage

- `prepare_references`
- `prepare_reads`

## Summary (from task_definitions metadata)

Build kallisto index resources and prepare reads for quantification.

### Declared inputs (path hints)
- **normalized_config** — Uses config after normalize_inputs — (from steps: normalize_inputs)

### Declared outputs (path hints)
- **reference_artifacts** — `resources/transcriptome.cdna.fasta` — (from steps: prepare_references)
- **read_prep_checkpoint** — `results/finish/prepare_reads.done` — (from steps: prepare_reads)

## TODO — fill before marking `status: ready` in registry

1. **Data:** Place minimal inputs under `input/` (or document symlinks/capsules). Do not commit large raw data without LFS or external URLs.
2. **Objective:** Replace this stub text with precise success criteria (files, metrics, thresholds).
3. **Gold / baseline:** Optional path to expected artifacts or a Snakemake/finish command used to produce reference outputs.
4. **Environment:** Note R/Bioconductor/conda requirements if different from the default pilot.

## Default env hint

`RTaskEvalEnv` expects a success artifact (see registry `success_artifact_glob`, default `output/result.txt`) before `submit_done(success=true)` with reward.
