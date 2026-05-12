# Real R-task benchmark — V2 curation status

Supersedes `_STATUS.md` (V1). This round follows the paper-first, data-only
rules from `experiments/COORDINATION_PLAN_V2.md` (§Phase 1, Subagent A).

## Final state (V2)

- Total **ready** tasks: **6** — all paper-covered, all data-only.
- Every ground-truth output was produced by actually running the source
  R script (verbatim or with image-writing calls stripped from a temp
  copy) against seeded synthetic inputs. Nothing is fabricated.
- Registry: `ldp_r_task_eval/r_tasks/registry.real.json` (schema v4).
- Wrapper mechanism: for `snakemake@input/output/params`-style scripts, a
  tiny S4 `SnakemakeMock` is emitted into `reference/wrapper.R`, which
  instantiates `snakemake` with the task-specific values and then
  `source()`s the (possibly patched) original script. See
  `tools/build_real_r_tasks.py::_emit_snakemake_wrapper`.

## Per-task table

| task_id | family | stage | diff | workflow_id | paper? | wrapper | eval_files | compliance |
|---|---|---|---:|---|---|---|---|---|
| `akinyi_deseq2` | rna | late | 2 | `akinyi-onyango-rna_seq_pipeline-finish` | yes | commandArgs | `deseq2_up.txt`, `deseq2_down.txt` | kept (already data-only) |
| `star_deseq2_init` | rna | mid | 2 | `rna-seq-star-deseq2-finish` | yes | snakemake | `normalized_counts.tsv` | newly added |
| `star_deseq2_contrast` | rna | late | 3 | `rna-seq-star-deseq2-finish` | yes | snakemake | `contrast_results.tsv` | newly added (SVG stripped from copy) |
| `methylkit_load` | methylation | early | 1 | `fritjoflammers-snakemake-methylanalysis-finish` | yes | snakemake | `mk_raw.rds` | newly added (PDF/SVG plot calls stripped) |
| `methylkit_unite` | methylation | mid | 2 | `fritjoflammers-snakemake-methylanalysis-finish` | yes | snakemake | `unite_stats.tsv` | newly added |
| `methylkit_to_tibble` | methylation | late | 3 | `fritjoflammers-snakemake-methylanalysis-finish` | yes | snakemake | `mean_mcpg.tsv` | newly added |

## Counts

- **Total ready:** 6 (all paper-covered — 100% coverage against
  `experiments/skills/manifest.json::by_workflow_id`)
- By family:
  - `rna`: 3 (akinyi_deseq2, star_deseq2_init, star_deseq2_contrast)
  - `methylation`: 3 (methylkit_load, methylkit_unite, methylkit_to_tibble)
- By stage:
  - `early`: 1
  - `mid`: 2
  - `late`: 3
- By difficulty:
  - 1 (easy): 1
  - 2 (medium): 3
  - 3 (harder): 2
- By wrapper kind:
  - `commandArgs`: 1
  - `snakemake`: 5

## Audit of the V1 twelve

| V1 task_id | V1 workflow_id | paper? | V1 deliverables | V2 action | reason |
|---|---|---|---|---|---|
| `akinyi_deseq2` | akinyi-onyango-rna_seq_pipeline-finish | yes | `deseq2_up.txt`, `deseq2_down.txt` | **KEPT** | pure data, paper-covered |
| `riya_limma` | RiyaDua-cervical-cancer-snakemake-workflow | no | `deg_results.csv`, `volcano.png` | **DROPPED** | workflow not in paper-covered set |
| `snakepipes_merge_fc` | maxplanck-ie-snakepipes-finish | no | `merged_counts.tsv` | **DROPPED** | workflow not in paper-covered set |
| `snakepipes_merge_ct` | maxplanck-ie-snakepipes-finish | no | `merged_tpm.tsv` | **DROPPED** | workflow not in paper-covered set |
| `chipseq_plot_peak_intersect` | snakemake-workflows-chipseq | no | `peak_intersect_upset.pdf` | **DROPPED** | not paper-covered + image-only |
| `chipseq_plot_macs_qc` | snakemake-workflows-chipseq | no | `macs_qc.pdf`, `macs_qc_summary.tsv` | **DROPPED** | workflow not in paper-covered set |
| `chipseq_plot_homer_annot` | snakemake-workflows-chipseq | no | `homer_annot.pdf`, `homer_annot_summary.tsv` | **DROPPED** | workflow not in paper-covered set |
| `snakepipes_scrna_merge_coutt` | maxplanck-ie-snakepipes-finish | no | `merged_coutt.tsv`, `merged_coutt.cell_names.tsv` | **DROPPED** | workflow not in paper-covered set |
| `snakepipes_scrna_qc` | maxplanck-ie-snakepipes-finish | no | 2 TSV + 4 PNG | **DROPPED** | workflow not in paper-covered set |
| `epigenbutton_mapping_stats` | joncahn-epigeneticbutton | no | `mapping_stats.pdf` | **DROPPED** | not paper-covered + image-only |
| `epigenbutton_peak_stats` | joncahn-epigeneticbutton | no | `peak_stats.pdf` | **DROPPED** | not paper-covered + image-only |
| `smartseqtotal_violin` | gersteinlab-ASTRO | no | `violin_scores.png` | **DROPPED** | not paper-covered + image-only |

Net: **1 kept, 11 dropped.** The common V1 driver was workflow breadth;
V2 is paper-covered depth.

## Refactorings (image calls stripped from a patched copy of the source)

All patches are applied to `tasks/real_ground_truth/<task_id>/reference/script.R`
(the in-task copy of the source), leaving `main/finish/workflow_candidates/**`
untouched.

- `star_deseq2_contrast` (source: `snakemake-workflows__rna-seq-star-deseq2/workflow/scripts/deseq2.R`):
  stripped the SVG MA-plot block. Specifically, `re.sub`-removed every
  line matching `^\s*svg\(...\)` / `^\s*plotMA\(...\)` / `^\s*dev.off\(\)`.
  The contrast-table write (`write.table(..., file = snakemake@output[["table"]])`)
  is preserved as-is. See `build_real_r_tasks.py::_patch_strip_svg`.
- `methylkit_load` (source:
  `fritjoflammers__snakemake-methylanalysis/workflow/scripts/methylkit_load.R`):
  stripped the two trailing `plot_methylkit_histograms(..., "pdf")` /
  `plot_methylkit_histograms(..., "svg")` calls. The `saveRDS(mk_raw, ...)`
  write is preserved. See `build_real_r_tasks.py::_patch_strip_methylkit_load_plots`.

## Newly-added tasks

### `star_deseq2_init`
- Source: `main/finish/workflow_candidates/snakemake-workflows__rna-seq-star-deseq2/workflow/scripts/deseq2-init.R`
- Wrapper: `snakemake` (SnakemakeMock emitted at
  `reference/wrapper.R`, injects `config[["samples"]]`, `config[["diffexp"]]`,
  `input[["counts"]]`, and `output[[1]]` / `output[[2]]`).
- Inputs: synthetic `counts.tsv` (500 genes × 6 samples, 3-vs-3 treated/untreated)
  + `samples.tsv` (`sample_name, condition`).
- Output: `normalized_counts.tsv` (DESeq2-normalized counts, tab-sep,
  `sep="\t"` + `row.names=FALSE` per source).

### `star_deseq2_contrast`
- Source: `main/finish/workflow_candidates/snakemake-workflows__rna-seq-star-deseq2/workflow/scripts/deseq2.R`
- Wrapper: `snakemake` + patched copy (SVG block stripped).
- Inputs: a `dds.rds` pre-built via the init wrapper inside the per-task
  `_gen` helper (`_gen_star_deseq2_contrast` synthesizes counts+samples,
  then runs a one-shot `deseq2-init.R` wrapper to produce `dds.rds`).
- Output: `contrast_results.tsv` (gene, baseMean, log2FoldChange, lfcSE,
  pvalue, padj — sorted by padj, `ashr` shrinkage applied).
- Requires the `ashr` CRAN package (installed during this round).

### `methylkit_load`
- Source: `main/finish/workflow_candidates/fritjoflammers__snakemake-methylanalysis/workflow/scripts/methylkit_load.R`
- Wrapper: `snakemake` + patched copy (plot calls stripped).
- `scriptdir` in the mock points at the original scripts dir so the
  script's own `source(file.path(scriptdir, "methylkit_common.R"))`
  resolves without vendoring anything.
- Inputs: 3 × synthetic bismark-coverage files, passed as **relative**
  paths so the serialised methylRawList is portable across workdirs.
- Output: `mk_raw.rds`.

### `methylkit_unite`
- Source: `main/finish/workflow_candidates/fritjoflammers__snakemake-methylanalysis/workflow/scripts/methylkit_unite.R`
- Wrapper: `snakemake` with a **pre-source hook** that runs
  `methylKit::methRead(...)` in-process (4 synthetic `.bismark.cov` files,
  treatment vector `c(0,0,1,1)`) and serialises the resulting methylRawList
  to `input/mk_raw.rds`. The mock's `snakemake@input[[1]]` is then pointed
  at that RDS before the original script sources and calls `unite()`.
- Output: `unite_stats.tsv` (single-row stats). `db_file` is declared as
  a **relative** path so the resulting `db_path` cell is portable.

### `methylkit_to_tibble`
- Source: `main/finish/workflow_candidates/fritjoflammers__snakemake-methylanalysis/workflow/scripts/methylkit2tibble.R`
- Wrapper: `snakemake` with a pre-source hook that chains
  `methRead(..., dbtype="tabix")` → `unite(..., save.db=TRUE)` to produce
  a `methylBaseDB` object (the source script accesses `@dbpath`, which
  exists only on methylBaseDB). Result is serialised and pointed at via
  `snakemake@input$rds`.
- Output: `mean_mcpg.tsv` (sample × chr × mean mCpG).

## Dropped / rejected candidates

- `snakemake-workflows__cellranger-multi/.../create_cellranger_multi_config_csv.R`:
  initially built as `cellranger_multi_config`, ran successfully, but the
  source calls `normalizePath(dirname(filename))` and embeds the absolute
  fastqs path in the output CSV. That cell is not portable across
  reference/agent workdirs, so the task would always be non-byte-identical
  at eval time. Dropped.
- `snakemake-workflows__rna-seq-star-deseq2/.../plot-pca.R`: produces SVG
  only; adding a TSV export would be fabrication (new behaviour, not
  preservation). Dropped per "image-only" rule.
- `snakemake-workflows__rna-seq-star-deseq2/.../gene2symbol.R`: `biomaRt`
  with required network access. Dropped.
- `snakemake-workflows__cite-seq-alevin-fry-seurat/...`: `Seurat` not
  installed per workflow constraint; all 8 R files skipped.
- `epigen__rnaseq_pipeline/.../plot_sample_annotation.R`: only produces
  PNG + HTML (via plotly/htmlwidgets::saveWidget); no tabular data
  output. Image-only, dropped.
- `epigen__rnaseq_pipeline/.../annotate_genes.R`: requires `biomaRt`
  (network) + `rtracklayer` + `Rsamtools` (not installed). Dropped.
- `lwang-genomics__NGS_pipeline_sn` / `snakemake-workflows__read-alignment-pangenome`:
  no R scripts in repo. Nothing to add.
- `fritjoflammers__snakemake-methylanalysis/.../methylkit_dmr.R`,
  `.../methylkit_clustering.R`, `.../methylkit_pca.R`,
  `.../methylkit_remove_snvs.R`, `.../methylkit_filt_norm.R`,
  `.../methylkit_split.R`, `.../methylkit_get_repeats.R`,
  `.../methylkit_unite_per_chr.R`, `.../methylkit_unite_from_bgz.R`,
  `.../methylkit2tibble_split.R`, `.../species_correlation.R`,
  `.../parse_macau.R`, `.../calc_pca.R`, `.../load_metadata.R`:
  either need `DSS` / `bsseq` (not installed), write only images, depend
  on upstream artefacts that are out of scope for this batch, or need
  external `sample_metadata.tsv` / `species_metadata.tsv` /
  `colors_file.tsv` that aren't included in the workflow repo.

## Installed R packages (this round)

- `ashr` (CRAN, required by `star_deseq2_contrast`'s `lfcShrink(type="ashr")`).
- `tidyverse` (CRAN meta-package, required by the methylanalysis
  workflow; all sub-packages were already present).
- `methylKit` (Bioconductor, required by the three methylation tasks).
- `here` (CRAN, loaded by methylanalysis sources).

## Reproduction commands

```sh
# from repo root (/Users/park/code/Paper2Skills-main)
python3 main/paper_primary_benchmark/ldp_r_task_eval/tools/build_real_r_tasks.py --list
python3 main/paper_primary_benchmark/ldp_r_task_eval/tools/build_real_r_tasks.py --all --force
```

Per-task rebuild:

```sh
python3 main/paper_primary_benchmark/ldp_r_task_eval/tools/build_real_r_tasks.py --task star_deseq2_init --force
```

A successful rebuild produces `tasks/real/<id>/{OBJECTIVE.md,input/,meta.json}`
+ `tasks/real_ground_truth/<id>/{reference/{script.R,wrapper.R,run.*.log,run.cmd.json},reference_output/<eval_files>,meta.json}`,
and the `_build_summary.json` at `tasks/real/_build_summary.json` shows
`"status": "ready"` for every task.

## Known limitations / notes for downstream agents

- The three methylation tasks require Bioconductor `methylKit` to be
  loadable at evaluation time. Document this in the agent environment
  readme alongside DESeq2 and `ashr`.
- `methylkit_load`'s deliverable is an RDS. methylKit serialises
  deterministically when given the same inputs at the same relative
  paths; the build uses relative paths inside the task workdir so the
  byte-identical check is achievable by agents that do the same.
- `star_deseq2_contrast`'s ground truth requires `lfcShrink(type="ashr")`.
  Agents must install/ensure `ashr` is available (or fall back to
  type="normal" but accept partial-credit verdicts since output values
  will differ).

## Final task_id list

```
akinyi_deseq2
star_deseq2_init
star_deseq2_contrast
methylkit_load
methylkit_unite
methylkit_to_tibble
```
