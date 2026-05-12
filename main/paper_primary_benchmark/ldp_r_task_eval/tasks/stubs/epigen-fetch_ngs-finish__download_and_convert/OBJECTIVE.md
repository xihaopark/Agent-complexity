# R-task stub: `epigen-fetch_ngs-finish` / `download_and_convert`

> **Status:** stub — evaluation inputs, metrics, and gold outputs are **not** filled in yet.
> Pipeline overlay comes from `paper_primary_benchmark/task_definitions/epigen-fetch_ngs-finish.json`.

## Stage

- **Label:** 公共数据下载与格式转换
- **Order:** 2
- **Finish manifest (reference):** `finish/epigen-fetch_ngs-finish/manifest.json`

## Snakemake steps in this stage

- `iseq_download`
- `fastq_to_bam`
- `fetch_file`

## Summary (from task_definitions metadata)

Download sequencing data and convert to BAM; additional file fetch.

### Declared inputs (path hints)
- **config_after_export** — (from steps: config_export)

### Declared outputs (path hints)
- **intermediate_fetch** — `results/finish/fetch_file.done` — (from steps: fetch_file)

## TODO — fill before marking `status: ready` in registry

1. **Data:** Place minimal inputs under `input/` (or document symlinks/capsules). Do not commit large raw data without LFS or external URLs.
2. **Objective:** Replace this stub text with precise success criteria (files, metrics, thresholds).
3. **Gold / baseline:** Optional path to expected artifacts or a Snakemake/finish command used to produce reference outputs.
4. **Environment:** Note R/Bioconductor/conda requirements if different from the default pilot.

## Default env hint

`RTaskEvalEnv` expects a success artifact (see registry `success_artifact_glob`, default `output/result.txt`) before `submit_done(success=true)` with reward.
