# Task Quality Audit — 32 real R-tasks (V3 registry)

**Auditor:** Subagent G3-A
**Date:** 2026-04-17
**Scope:** `main/paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.real.json` (schema v5, 32 tasks)
**Method:** Each task evaluated against seven rubric criteria (objective clarity,
input realism, script fidelity vs source, ground truth existence, difficulty
calibration, task-workspace isolation, solvability heuristic).

## Headline

- **All 32 tasks are legitimate, script-backed, and reproducible.** None is fabricated.
- **0/32 tasks show semantic rewrite drift** from their source script. Diffs are
  confined to (a) the V3 device-redirect prelude (≤14 added lines) or (b) stripping
  `svg()` / `plotMA()` / `plot_methylkit_histograms(...)` plot calls (≤3 removed lines).
- **2 tasks flagged for objective-file triviality** (`phantompeak_correlation`,
  `chipseq_plot_frip_score`, `chipseq_plot_peaks_count_macs2` — difficulty-1 concat
  tasks with inputs < 50 B per file); keep-with-caveat.
- **0 cheating leaks detected.** The three `isolation_ok=False` flags are prep
  helpers (`_prep_dds.R`, `_build_rdata.R`) that **build the task input** from an
  upstream stage; they do not expose the task's own reference script.

## Summary table

| task_id | family | stage | diff | objective_ok | input_ok | script_fidelity | gt_ok | isolation_ok | solvable | notes |
|---|---|---|---:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| akinyi_deseq2 | rna | late | 2 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| star_deseq2_init | rna | mid | 2 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| star_deseq2_contrast | rna | late | 3 | ✓ | ✓ | wrapped (−3 plot) | ✓ | ~ | ✓ | `_prep_dds.R` in input/ seeds dds.rds (upstream helper, not reference leak) |
| methylkit_load | methylation | early | 1 | ✓ | ✓ | wrapped (−3 plot) | ✓ | ✓ | ✓ | clean |
| methylkit_unite | methylation | mid | 2 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| methylkit_to_tibble | methylation | late | 3 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| longseq_deseq2_init | rna | mid | 2 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| longseq_deseq2_contrast | rna | late | 3 | ✓ | ✓ | wrapped (+14 device) | ✓ | ~ | ✓ | `_prep_dds.R` input helper |
| snakepipes_merge_fc | rna | early | 1 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean (concat) |
| snakepipes_merge_ct | rna | early | 1 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean (concat) |
| riya_limma | rna | late | 2 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| chipseq_plot_macs_qc | chipseq | late | 2 | ✓ | ✓ | wrapped (+14 device) | ✓ | ✓ | ✓ | clean |
| chipseq_plot_homer_annot | chipseq | late | 2 | ✓ | ✓ | wrapped (+14 device) | ✓ | ✓ | ✓ | clean |
| snakepipes_scrna_merge_coutt | scrna | mid | 2 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| snakepipes_scrna_qc | scrna | mid | 2 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| spilterlize_filter_features | rna | early | 2 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| spilterlize_norm_voom | rna | mid | 2 | ✓ | ✓ | wrapped (+14 device) | ✓ | ✓ | ✓ | clean |
| spilterlize_limma_rbe | rna | late | 3 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| spilterlize_norm_edger | rna | mid | 2 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| dea_limma | rna | late | 3 | ✓ | ✓ | wrapped (+14 device) | ✓ | ✓ | ✓ | clean |
| msisensor_merge | variant | late | 2 | ✓ | ✓* | identical | ✓ | ✓ | ✓ | inputs live under `results/msi/<case>/msi_out.txt` (per OBJECTIVE), not `input/` |
| methylkit_filt_norm | methylation | mid | 2 | ✓ | ✓ | wrapped (−3 plot) | ✓ | ✓ | ✓ | clean |
| methylkit2tibble_split | methylation | late | 3 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| methylkit_remove_snvs | methylation | late | 3 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| phantompeak_correlation | chipseq | late | 1 | ✓ | ~ | identical | ✓ | ~ | ~ | input is 383 B RData + 24 B header; `_build_rdata.R` helper visible; trivial concat/write |
| nearest_gene | chipseq | late | 2 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| chipseq_plot_frip_score | chipseq | late | 1 | ✓ | ~ | wrapped (+14 device) | ✓ | ✓ | ~ | 4 inputs × ~24 B; trivial aggregate |
| chipseq_plot_peaks_count_macs2 | chipseq | late | 1 | ✓ | ~ | wrapped (+14 device) | ✓ | ✓ | ~ | 4 inputs × ~20 B; trivial aggregate |
| chipseq_plot_annotatepeaks_summary_homer | chipseq | late | 1 | ✓ | ✓ | wrapped (+14 device) | ✓ | ✓ | ✓ | clean |
| epibtn_rpkm | rna | late | 2 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean; uses embedded hardcoded output path |
| snakepipes_scrna_report | scrna | late | 1 | ✓ | ✓ | identical | ✓ | ✓ | ✓ | clean |
| clean_histoneHMM | chipseq | late | 2 | ✓ | ✓ | wrapped (+14 device) | ✓ | ✓ | ✓ | clean |

Legend: ✓ pass, ~ pass-with-caveat, ✗ fail. "wrapped (+14 device)" = V3 `_patch_redirect_devices` prelude prepended, semantics identical. "wrapped (−3 plot)" = incidental plot calls stripped (content-preserving).

## Distribution (family × difficulty)

| family       | d1 | d2 | d3 | total |
|--------------|---:|---:|---:|------:|
| rna          |  2 |  8 |  4 |    14 |
| methylation  |  1 |  2 |  3 |     6 |
| chipseq      |  4 |  4 |  0 |     8 |
| scrna        |  1 |  2 |  0 |     3 |
| variant      |  0 |  1 |  0 |     1 |
| **all**      |  8 | 17 |  7 |    32 |

- No family is 100 % difficulty-1. `chipseq` is tilted toward d1 (4/8 = 50 %) — four
  tasks (`phantompeak_correlation`, `chipseq_plot_frip_score`,
  `chipseq_plot_peaks_count_macs2`, `chipseq_plot_annotatepeaks_summary_homer`) are
  trivial aggregate/concat operations from the same source pipeline. The
  `variant` family has only a single task, so is structurally under-represented.
- 20/32 registry scripts are **byte-identical** to their source; 12/32 use
  narrow harness wrapping (device redirects or plot-call strips). **No semantic
  rewrites.**

## Ground truth integrity

All 36 expected files (across 32 tasks) exist, are non-zero size, and parse as
their declared type (TSV/CSV/TXT/BED/RDS). Smallest: `methylkit_remove_snvs/snv_stats.tsv`
(45 B, header-plus-one-row). Largest: `star_deseq2_init/normalized_counts.tsv`
(58 217 B). Every file begins with a plausible header row.

## Flagged tasks with actionable gaps

No task needs to be dropped outright. Four deserve caveats.

### Keep-with-caveat (difficulty-1 triviality)

1. **`phantompeak_correlation`** — inputs are a 383 B `run_spp.RData`
   containing a single pre-computed crosscorr table and a 24 B `header.csv`;
   the task is to `load()`, extract `crosscorr$cross.correlation`, and write it
   as CSV with the header's column names. This is ≤ 10 LOC and tests nothing
   biological — effectively a serialization exercise. Registry difficulty = 1;
   consistent but consider demoting to "warmup" bucket for publication slice.
2. **`chipseq_plot_frip_score`**, **`chipseq_plot_peaks_count_macs2`** — both
   read 4 × ~20 B two-field TSVs and concatenate them. Solvable in ≤ 15 LOC
   of base R. The difficulty-1 label is appropriate; they are useful as
   "sanity-ceiling" baselines (every arm should solve them) but shouldn't be
   used to rank skill-enabled LLMs.
3. **`snakepipes_scrna_report`** (d1) — aggregates library metrics from
   `.tsv` counts into a 4-column report; also trivial, similar in feel.

### Keep-with-context (prep-helper visibility)

4. **`star_deseq2_contrast`**, **`longseq_deseq2_contrast`** — each has
   `_prep_dds.R` in `input/` that uses the SnakemakeMock harness to
   source the **upstream** `deseq2-init.R` and emit `dds.rds`. This is not a
   leak of the task's own reference (that would be `deseq2.R`), but it does
   expose the SnakemakeMock pattern and the upstream pipeline stage. For the
   paired `*_init` task the corresponding mock script would still constitute
   a leak; verified that no `_prep_init.R` / `_prep_*deseq2-init*.R` lives
   inside `star_deseq2_init/input/` or `longseq_deseq2_init/input/`
   (confirmed clean). Safe to keep as-is; document the convention in the
   benchmark README so graders know these are prep helpers.
5. **`phantompeak_correlation/input/_build_rdata.R`** — a 13-line helper
   that writes the `crosscorr` RData. Trivial, not leakage (the reference
   script is a 6-line calculator over that RData).

### Missing-skill note

Both contrast tasks and all four trivial chipseq d1 tasks appear in
`manifest.json → tasks_without_skill`, meaning the paper-skill-enabled arm
receives no skill context for them. That is a **coverage gap in manifest.json
v3**, not a task defect, but should be disclosed when reporting arm-level
deltas.

## Top 3 "most impressive" tasks (publication showcase)

1. **`dea_limma`** (difficulty 3, rna, `epigen-dea_limma-finish`)
   End-to-end limma-voom DE with model matrix construction, covariate
   handling, and two eval files (`dea_results.csv`, `model_matrix.csv`). The
   reference script is 101 LOC from epigen / dea_limma and exercises
   `voom`, `lmFit`, `eBayes`, `topTable`, `makeContrasts`. Evaluates
   whether an agent can reproduce a real DE workflow and save *both*
   the design matrix and the result table.
2. **`spilterlize_limma_rbe`** (difficulty 3, rna, `epigen-spilterlize_integrate-finish`)
   `limma::removeBatchEffect` with a genuine `_RVec` character-vector
   parameter (reformulate) — tests correct handling of a multi-column design
   formula + batch covariates. Non-trivial, produces a 21 KB
   `integrated_data.csv` that matches row/column-wise against the seeded
   reference.
3. **`star_deseq2_contrast`** (difficulty 3, rna,
   `rna-seq-star-deseq2-finish`) The snakemake-workflows official DE contrast
   script, with shrinkage (`ashr`), contrast construction from config, and
   a 53 KB `contrast_results.tsv`. Good balance: realistic upstream
   (`dds.rds` from `deseq2-init.R`), real DESeq2 API surface, clean tabular
   scoring.

Honorable mention: **`methylkit_remove_snvs`** (d3, methylation) — genuinely
non-trivial methylKit + VCF position filtering with summary statistics.

## Top 3 "weakest" tasks (consider demoting/dropping from publication slice)

1. **`phantompeak_correlation`** — RData unpack + rename; effectively an
   I/O test. If the benchmark wants to emphasize biological reasoning,
   drop.
2. **`chipseq_plot_frip_score`** — 4×2-field TSV concat; 99 % of the
   information content is in 4 × 24-byte files.
3. **`chipseq_plot_peaks_count_macs2`** — same pattern as #2; concat of
   4 × 1-row peak-count files. Suggest keeping at most **one** of
   `{frip_score, peaks_count, annotatepeaks_summary_homer}` as a d1
   warmup and dropping the other two to avoid over-weighting trivial
   sanity checks inside the chipseq family.

## Methodological notes

- **Fidelity diffs were computed with `diff -u src ref` for every task.** The
  full allowlist of acceptable changes is: the 14-line
  `_patch_redirect_devices` prelude; removal of `svg(...) / png(...) /
  pdf(...) / ggsave(...) / plot_methylkit_histograms(...) / plotMA(...)`
  calls; `setwd(...)` additions in the wrapper (not the reference script).
  None of the 32 reference scripts contain business-logic rewrites.
- **Isolation:** no task's `output/` already contains a copy of the
  reference output, and no `.R` file matching the reference script name
  appears under `tasks/real/<tid>/`. The three prep helpers (`_prep_dds.R`,
  `_build_rdata.R`) are either upstream-stage mockers or synthetic-data
  builders, labeled with a leading underscore; they do not reproduce the
  task's reference solution.
- **Ground-truth sizes vary from 45 B to 58 KB.** All outputs parse with
  their declared format (`readr::read_tsv` / `read.csv` / `readRDS`).

## Verdict

All 32 tasks pass the audit. Publication-quality core: ≈ 24 tasks of
difficulty 2–3 with non-trivial biological content; the 8 difficulty-1
tasks are useful as ceiling baselines but should be reported separately
from the headline per-family accuracy. Recommend demoting or dropping
`phantompeak_correlation`, `chipseq_plot_frip_score`, and
`chipseq_plot_peaks_count_macs2` from the headline table.
