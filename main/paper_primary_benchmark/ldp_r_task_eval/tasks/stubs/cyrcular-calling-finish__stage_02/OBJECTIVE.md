# R-task stub: `cyrcular-calling-finish` / `stage_02`

> **Status:** stub — evaluation inputs, metrics, and gold outputs are **not** filled in yet.
> Pipeline overlay comes from `paper_primary_benchmark/task_definitions/cyrcular-calling-finish.json`.

## Stage

- **Label:** Automated stage 2 (5 finish steps)
- **Order:** 2
- **Finish manifest (reference):** `finish/cyrcular-calling-finish/manifest.json`

## Snakemake steps in this stage

- `download_gene_annotation`
- `minimap2_bam`
- `merge_fastqs`
- `samtools_index`
- `samtools_faidx`

## Summary (from task_definitions metadata)

Contiguous partition from finish manifest order; refine labels and IO as needed.

### Declared inputs (path hints)
- **upstream** — (from steps: download_gene_annotation)

### Declared outputs (path hints)
- **checkpoint_last_step** — `results/finish/samtools_faidx.done` — (from steps: samtools_faidx)

## TODO — fill before marking `status: ready` in registry

1. **Data:** Place minimal inputs under `input/` (or document symlinks/capsules). Do not commit large raw data without LFS or external URLs.
2. **Objective:** Replace this stub text with precise success criteria (files, metrics, thresholds).
3. **Gold / baseline:** Optional path to expected artifacts or a Snakemake/finish command used to produce reference outputs.
4. **Environment:** Note R/Bioconductor/conda requirements if different from the default pilot.

## Default env hint

`RTaskEvalEnv` expects a success artifact (see registry `success_artifact_glob`, default `output/result.txt`) before `submit_done(success=true)` with reward.
