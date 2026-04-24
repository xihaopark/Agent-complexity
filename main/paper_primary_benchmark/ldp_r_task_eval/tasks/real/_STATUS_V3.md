# Real R-task benchmark — V3 curation status

Supersedes `_STATUS_V2.md`. V3 follows the updated rules from
`experiments/COORDINATION_PLAN_V3.md`, which **relax** the strict paper-coverage
gate that shrank V2 to 6 tasks. Subagent C3 handles paper-covered workflow
expansion separately; A3's mandate here is to maximize **ready, data-only,
script-backed tasks** across every pipeline-skill-able source tree.

## Final state (V3)

- **Total ready tasks: 32** (all `status: ready`, all passed real `--all --force`
  rebuild against seeded synthetic inputs).
- Every ground-truth output was produced by actually running the source
  R script (verbatim or with a narrow patched copy) — nothing fabricated.
- Registry: `ldp_r_task_eval/r_tasks/registry.real.json` (schema v5, 32 tasks).
- All V2 tasks are preserved unchanged; 26 new tasks have been added.
- Wrapper mechanisms (unchanged from V2 but more heavily exercised):
  - `snakemake` — S4 `SnakemakeMock` emitted into
    `reference/wrapper.R` which instantiates `snakemake` and
    `source()`s the (possibly patched) original script.
  - `commandArgs` — thin Rscript invocation with positional args.
- New universal patch helper `_patch_redirect_devices` installs global
  overrides for `pdf`/`png`/`svg`/`jpeg`/`ggsave` that redirect to
  `tempfile(...)` so data-producing scripts that incidentally also draw can
  be wrapped without fabricating output.
- New `_RVec` marker + `_r_quote` extension lets us emit genuine R character
  vectors (e.g. for `reformulate`, for `snakemake@input` where `lapply` is
  called) rather than length-1 lists.

## Summary counts

| | V2 | V3 |
|---|---:|---:|
| Total ready | 6 | **32** |
| `rna` | 3 | 14 |
| `methylation` | 3 | 6 |
| `chipseq` | 0 | 8 |
| `scrna` | 0 | 3 |
| `variant` | 0 | 1 |
| Unique source workflows | 2 | 11 |
| `paper_covered == true` | 6 | 9 |
| `wrapper_kind == snakemake` | 5 | 22 |
| `wrapper_kind == commandArgs` | 1 | 10 |

Soft-target coverage per COORDINATION_PLAN_V3 (≥10 RNA, ≥6 methylation,
≥5 ChIP/ATAC, ≥3 scRNA): **met for all four families**. Hard target of ≥30
ready tasks: **met (32)**.

## Per-task inventory (V3)

| task_id | family | stage | diff | workflow_id | paper? | wrapper | eval_files | notes |
|---|---|---|---:|---|---|---|---|---|
| `akinyi_deseq2` | rna | late | 2 | akinyi-onyango-rna_seq_pipeline-finish | yes | commandArgs | `deseq2_up.txt`, `deseq2_down.txt` | V2; unchanged |
| `star_deseq2_init` | rna | mid | 2 | rna-seq-star-deseq2-finish | yes | snakemake | `normalized_counts.tsv` | V2; unchanged |
| `star_deseq2_contrast` | rna | late | 3 | rna-seq-star-deseq2-finish | yes | snakemake | `contrast_results.tsv` | V2; SVG stripped |
| `methylkit_load` | methylation | early | 1 | fritjoflammers-…-methylanalysis-finish | yes | snakemake | `mk_raw.rds` | V2; plot calls stripped |
| `methylkit_unite` | methylation | mid | 2 | fritjoflammers-…-methylanalysis-finish | yes | snakemake | `unite_stats.tsv` | V2; unchanged |
| `methylkit_to_tibble` | methylation | late | 3 | fritjoflammers-…-methylanalysis-finish | yes | snakemake | `mean_mcpg.tsv` | V2; unchanged |
| `longseq_deseq2_init` | rna | mid | 2 | snakemake-workflows-rna-longseq-de-isoform | no | snakemake | `normalized_counts.tsv` | V3 new |
| `longseq_deseq2_contrast` | rna | late | 3 | snakemake-workflows-rna-longseq-de-isoform | no | snakemake | `contrast_results.tsv` | V3 new; devices redirected |
| `snakepipes_merge_fc` | rna | early | 1 | maxplanck-ie-snakepipes-finish | no | commandArgs | `merged_counts.tsv` | V3 new; V1 script rescued |
| `snakepipes_merge_ct` | rna | early | 1 | maxplanck-ie-snakepipes-finish | no | commandArgs | `merged_tpm.tsv` | V3 new; V1 script rescued |
| `riya_limma` | rna | late | 2 | RiyaDua-cervical-cancer-snakemake-workflow | no | commandArgs | `deg_results.csv` | V3 new; volcano disabled via arg elision |
| `chipseq_plot_macs_qc` | chipseq | late | 2 | snakemake-workflows-chipseq-finish | no | commandArgs | `macs_qc_summary.tsv` | V3 new; devices redirected |
| `chipseq_plot_homer_annot` | chipseq | late | 2 | snakemake-workflows-chipseq-finish | no | commandArgs | `homer_annot_summary.tsv` | V3 new; devices redirected |
| `chipseq_plot_frip_score` | chipseq | late | 1 | snakemake-workflows-chipseq-finish | no | snakemake | `frip_scores.tsv` | V3 new; TSV via post-source hook |
| `chipseq_plot_peaks_count_macs2` | chipseq | late | 1 | snakemake-workflows-chipseq-finish | no | snakemake | `peaks_count.tsv` | V3 new; TSV via post-source hook |
| `chipseq_plot_annotatepeaks_summary_homer` | chipseq | late | 1 | snakemake-workflows-chipseq-finish | no | snakemake | `homer_long.tsv` | V3 new; TSV via post-source hook |
| `phantompeak_correlation` | chipseq | late | 1 | snakemake-workflows-chipseq-finish | no | snakemake | `crosscorr.csv` | V3 new |
| `nearest_gene` | chipseq | late | 2 | maxplanck-ie-snakepipes-finish | no | snakemake | `annotated.bed` | V3 new |
| `clean_histoneHMM` | chipseq | late | 2 | maxplanck-ie-snakepipes-finish | no | snakemake | `sampleA_avgp0.5.bed`, `sampleB_avgp0.5.bed` | V3 new; devices redirected |
| `snakepipes_scrna_merge_coutt` | scrna | mid | 2 | maxplanck-ie-snakepipes-finish | no | commandArgs | `merged_coutt.tsv`, `merged_coutt.cell_names.tsv` | V3 new; V1 script rescued |
| `snakepipes_scrna_qc` | scrna | mid | 2 | maxplanck-ie-snakepipes-finish | no | commandArgs | `scqc.libstats_reads.tsv`, `scqc.libstats_pct.tsv` | V3 new; plot arg elided |
| `snakepipes_scrna_report` | scrna | late | 1 | maxplanck-ie-snakepipes-finish | no | snakemake | `scrna_report.tsv` | V3 new |
| `spilterlize_filter_features` | rna | early | 2 | epigen-spilterlize_integrate-finish | no | snakemake | `filtered_counts.csv` | V3 new |
| `spilterlize_norm_voom` | rna | mid | 2 | epigen-spilterlize_integrate-finish | no | snakemake | `normalized_counts.csv` | V3 new; voom plot redirected |
| `spilterlize_limma_rbe` | rna | late | 3 | epigen-spilterlize_integrate-finish | no | snakemake | `integrated_data.csv` | V3 new; `_RVec` for character params |
| `spilterlize_norm_edger` | rna | mid | 2 | epigen-spilterlize_integrate-finish | no | snakemake | `all/normTMM.csv` | V3 new |
| `dea_limma` | rna | late | 3 | epigen-dea_limma-finish | no | snakemake | `dea_results.csv`, `model_matrix.csv` | V3 new; devices redirected |
| `msisensor_merge` | variant | late | 2 | snakemake-workflows-msisensor-pro-finish | no | snakemake | `merged_msi.tsv` | V3 new; `setwd(workdir)` pre-hook |
| `methylkit_filt_norm` | methylation | mid | 2 | fritjoflammers-…-methylanalysis-finish | yes | snakemake | `filt_norm_stats.tsv` | V3 new; custom `plot_methylkit_histograms` strip |
| `methylkit2tibble_split` | methylation | late | 3 | fritjoflammers-…-methylanalysis-finish | yes | snakemake | `mean_mcpg_split.tsv` | V3 new; upstream `mku` RDS built in pre-hook |
| `methylkit_remove_snvs` | methylation | late | 3 | fritjoflammers-…-methylanalysis-finish | yes | snakemake | `snv_stats.tsv` | V3 new |
| `epibtn_rpkm` | rna | late | 2 | joncahn-epigeneticbutton-finish | no | commandArgs | `results/RNA/DEG/genes_rpkm__runX__mockref.txt` | V3 new; hardcoded path handled via `setwd` wrapper |

## Rescue techniques used

- **`snakemake@`-only scripts rescued with `SnakemakeMock`:** 17 new
  snakemake-style tasks became executable standalone.
- **`_patch_redirect_devices` (universal device shim):** installed on 9
  tasks whose scripts incidentally call `pdf/png/svg/jpeg/ggsave`; redirects
  to `tempfile(...)` so the data writes succeed without cluttering outputs.
- **Script-specific strippers:** `_patch_strip_svg` (V2), `_patch_strip_methylkit_load_plots`
  (V2), `_patch_strip_methylkit_plotfn` (V3) for cases where a device
  redirect was insufficient.
- **Argument elision:** `riya_limma` and `snakepipes_scrna_qc` disable
  their optional plotting by omitting the trailing positional arg so the
  script's `if (!is.na(...))` branch skips.
- **`_RVec` marker:** lets `_r_quote` emit genuine R character vectors for
  Snakemake params that downstream calls `reformulate` / `[[` / `lapply`
  over (fixing `spilterlize_limma_rbe`, `spilterlize_norm_edger`, etc.).
- **Pre-source hooks:** used to build upstream artifacts in-process
  (`methylkit2tibble_split` pre-builds two `mku`-merged `.rds` files) or
  to chdir into the task workdir when a script has embedded relative
  path expectations (`msisensor_merge`).
- **Post-source hooks:** used for scripts whose only "persistent" output is
  a plot; after `source()`, we read the tibble the script left in the
  global env (`frip_scores`, `counts`, `homer_data`) and write it as TSV.
- **Hardcoded output paths:** `epibtn_rpkm` writes to
  `results/RNA/DEG/genes_rpkm__<analysis>__<refgenome>.txt`; handled by
  `setwd(reference_output)` + `commandArgs` override in the wrapper.

## Dropped / skipped scripts (V3 survey)

Scripts surveyed but **not** promoted to tasks, with reasons:

- `snakemake-workflows__chipseq/plot_peak_intersect.R` — pure PDF only, no tabular output.
- `snakemake-workflows__chipseq/featurecounts_deseq2.R` — requires `vsn` (absent) and uses existence-check to skip steps, not idempotent on fresh runs.
- `snakemake-workflows__chipseq/run_spp.R` — uses forbidden `spp` package.
- `maxplanck-ie__snakePipes/shared/rscripts/chipqc.R` — requires `ChIPQC`, heavy deps.
- `maxplanck-ie__snakePipes/shared/rscripts/WGBS_mergeStats.R` — depends on `bsseq` (absent).
- `maxplanck-ie__snakePipes/shared/rscripts/scRNAseq_EmptyDrops.R` — forbidden `Seurat`.
- `maxplanck-ie__snakePipes/shared/rscripts/scRNAseq_merge_loom.R` — forbidden `Seurat`/`velocyto.R`.
- `maxplanck-ie__snakePipes/shared/rscripts/scRNAseq_splitAlevinVelocityMatrices.R` — forbidden `scater`.
- `maxplanck-ie__snakePipes/shared/rscripts/scRNAseq_cell_filter_monocle.R` — forbidden `Monocle3`.
- `maxplanck-ie__snakePipes/shared/rscripts/scRNAseq_cell_filter_raceid.R` — requires `RaceID` (absent).
- `maxplanck-ie__snakePipes/shared/rscripts/sleuth.R` / `sleuth_allelic.R` — forbidden `sleuth`.
- `maxplanck-ie__snakePipes/shared/rscripts/wasabi.R` — requires `wasabi` (absent).
- `maxplanck-ie__snakePipes/shared/rscripts/extractIntronSeqs.R` / `extractTxSeqs.R` — library-helper only (no standalone executable semantics).
- `joncahn__epigeneticbutton/workflow/scripts/R_sizes_stats.R`, `R_mapping_stats.R` — PDF-only.
- `epigen__dea_limma/workflow/scripts/aggregate.R`, `heatmap.R`, `volcanos.R`, `ova_stats_plot.R`, `one_vs_all_contrasts.R` — either image-only or requires outputs from a multi-split upstream that would be prohibitively complex to synthesize.
- `RiyaDua/preprocessing.R`, `.../pca.R`, `.../summary_statistics.R` — respectively need `GEOquery` (network), Seurat (forbidden), `pca.R` input is missing, `summary_statistics.R` requires Seurat.

## Out-of-scope / untouched

- No files under `experiments/skills*/`, `batch_runner.py`, `r_task_env.py`,
  `rollout.py`, or the evaluator were modified.
- No original R scripts under `main/finish/workflow_candidates/**` were
  modified — all patches operate on temp copies under
  `tasks/real_ground_truth/<task>/reference/script.R`.

## Reproducibility

- Every synthesizer uses a task-specific seeded `random.Random`; no network
  access is required at build time.
- `python3 tools/build_real_r_tasks.py --all --force` on a checkout with the
  installed R package set (R 4.5.1 at `/usr/local/bin/Rscript`) rebuilds all
  32 tasks in ≈2 minutes end-to-end.
