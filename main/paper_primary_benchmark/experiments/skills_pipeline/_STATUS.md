# Pipeline-Source Skill Generation — Status (Subagent B2)

Generated: 2026-04-17 (UTC). Generator: `experiments/skills_pipeline/tools/generate_pipeline_skill.py` + `build_manifest.py`. Model: `openrouter/openai/gpt-4o`.

## What this is

For each of the 8 paper-covered workflows in `experiments/skills/manifest.json::by_workflow_id`, we collected the workflow's own source (Snakefile / `*.smk` / `*.R` / `*.Rmd` / `*.py` / `config*.yaml` / `env*.yaml` / `README*`), concatenated with `=== FILE: <relpath> ===` separators (per-file cap 8 000 chars, total cap 80 000 chars), and asked `gpt-4o` via OpenRouter to distil a 4-section SKILL.md with the same contract as the paper vision adapter (`## Method`, `## Parameters`, `## Commands / Code Snippets`, `## Notes for R-analysis agent`).

Output tree under `experiments/skills_pipeline/`:

- `<workflow_id>/SKILL.md` — skill with YAML front matter.
- `<workflow_id>/run_manifest.json` — token usage, runtime, files considered / included, truncation flag.
- `manifest.json` — per-`workflow_id` index with a stripped `skill_md_inline` (≤ 4 000 chars).
- `tools/generate_pipeline_skill.py` — the tool.
- `tools/build_manifest.py` — rolls per-workflow manifests into `manifest.json`.

## Per-workflow table

| workflow_id | files considered | files included | chars used | prompt tok | completion tok | runtime (s) | SKILL.md (bytes) | input $ | output $ | total $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| akinyi-onyango-rna_seq_pipeline-finish | 3 | 3 | 6 408 | 2 104 | 771 | 7.4 | 3 467 | 0.0053 | 0.0077 | 0.0130 |
| rna-seq-star-deseq2-finish | 21 | 21 | 41 966 | 11 447 | 1 043 | 9.4 | 4 533 | 0.0286 | 0.0104 | 0.0391 |
| fritjoflammers-snakemake-methylanalysis-finish† | 33 | 33 | 80 000 | 22 846 | 968 | 18.8 | 4 248 | 0.0571 | 0.0097 | 0.0668 |
| lwang-genomics-ngs_pipeline_sn-rna_seq-finish | 5 | 5 | 28 339 | 7 746 | 601 | 11.0 | 3 093 | 0.0194 | 0.0060 | 0.0254 |
| cellranger-multi-finish | 13 | 13 | 47 000 | 12 021 | 778 | 9.1 | 3 658 | 0.0301 | 0.0078 | 0.0378 |
| epigen-rnaseq_pipeline-finish | 16 | 16 | 51 282 | 12 930 | 1 290 | 22.4 | 5 660 | 0.0323 | 0.0129 | 0.0452 |
| cite-seq-alevin-fry-seurat-finish | 18 | 18 | 19 722 | 6 188 | 1 050 | 7.0 | 4 544 | 0.0155 | 0.0105 | 0.0260 |
| read-alignment-pangenome-finish | 19 | 19 | 46 391 | 12 749 | 743 | 6.6 | 3 571 | 0.0319 | 0.0074 | 0.0393 |
| **totals** | 128 | 128 | 321 108 | 88 031 | 7 244 | 92.7 | 32 774 | 0.2200 | 0.0724 | **0.2924** |

† methylanalysis hit the 80 KB total blob cap (`truncated: true` in `run_manifest.json`); the last ~18.7 KB of lower-priority source never reached the model.

Cost columns use the public OpenRouter GPT-4o rate card ($2.50 / M prompt, $10.00 / M completion) — actual OpenRouter invoice may differ slightly. Well under the $0.40 budget.

0 workflows skipped — every source tree produced ≥ 6 KB of meaningful code (well above the `--min-blob-chars 1024` stub threshold).

## Quality notes

### Did each output contain an actionable `## Commands / Code Snippets`?

| workflow | actionable R snippet(s)? | notes |
|---|---|---|
| akinyi-onyango-rna_seq_pipeline-finish | **yes** | Verbatim `scripts/deseq_analysis.r` (DESeq2 with command-line args). Directly runnable in R-task env. Strongest of the 8 because the source is small enough that the whole DESeq2 script fits in context. |
| rna-seq-star-deseq2-finish | **yes** | Two correctly extracted `snakemake@`-style DESeq2 blocks (init + contrast with `lfcShrink(type="ashr")`). Will need the `snakemake` adapter (already in the v2 plan) to execute stand-alone. |
| fritjoflammers-snakemake-methylanalysis-finish | partial | Extracted `load_metadata` + `calc_PCA` utility helpers from `scripts/R/*.R`. Useful but not a complete analysis; likely because the DMR / MACAU call sites were in the 18.7 KB that got truncated. |
| lwang-genomics-ngs_pipeline_sn-rna_seq-finish | no (honest) | Emits exactly `(No R code snippets visible in the pipeline source.)` — correct: the source is Snakemake + shell only, no `.R` files. |
| cellranger-multi-finish | yes (partial) | Pulled `create_cellranger_multi_config_csv.R` (tidyverse / `separate_wider_regex`). This is config plumbing, not downstream analysis; honest about that. |
| epigen-rnaseq_pipeline-finish | **yes** | Full biomaRt + GenomicRanges/rtracklayer annotation script with the 4-mirror fallback loop intact. High-fidelity. |
| cite-seq-alevin-fry-seurat-finish | **yes** | `load_fry` + `CreateSeuratObject` + `HTODemux` blocks captured from `workflow/scripts/*.R`. |
| read-alignment-pangenome-finish | no (honest) | Emits the `(No R code snippets visible…)` sentinel — correct: this pipeline is pure Snakemake + vg/bwa/fastp shell. |

### Hallucination check

Spot-checked each `## Commands / Code Snippets` block against the source files:

- All R blocks match code that exists verbatim in the source tree (allowing for whitespace folding / truncation comments).
- No fabricated DESeq2 / Seurat / MethylKit calls were introduced when none existed in the source. The two pipelines without R code (`lwang-…-rna_seq`, `read-alignment-pangenome`) correctly emit the sentinel line rather than inventing analysis code.
- `## Parameters` sections cite config keys that exist in the pipeline's `config*.yaml` / Snakefile `params:` blocks (verified for akinyi, rna-seq-star-deseq2, epigen-rnaseq, read-alignment-pangenome).

### Subjective quality vs. paper-skills

| workflow | pipeline-skill vs paper-skill for `akinyi_deseq2`-style R tasks |
|---|---|
| akinyi-onyango | pipeline-skill **wins** for re-executing the pipeline's own DESeq2 script (gives the actual column layout + ERCC filter + LFC≥2 thresholds); paper-skill is more general methodological framing. |
| rna-seq-star-deseq2 | pipeline-skill **wins** for snakemake-adapter tasks — it shows the exact `snakemake@input/config/wildcards` API the reference scripts use. Paper-skill (Love 2014) is better for explaining DESeq2 itself. |
| fritjoflammers | pipeline-skill is partial (truncated); paper-skill (Wong 2016 MethPat) is arguably more useful for method framing right now. Worth re-running with `--max-total 120000` if we want coverage of the DMR call sites. |
| lwang-…-rna_seq | pipeline-skill is thin (no R code → sentinel) but parameter section is better than the paper's (Marioni 2008 is just a 15-year-old Poisson model). Pipeline-skill wins on config/params, loses on method. |
| cellranger-multi | both are weak for an R-task arm — pipeline-skill captures the plumbing R script but no downstream analysis; paper-skill (Zheng 2017) is product-description level. |
| epigen-rnaseq_pipeline | pipeline-skill **wins** — biomaRt annotation script with mirror retries is directly reusable in the R-task env; paper-skill for Marioni 2008 is not pipeline-specific. |
| cite-seq-alevin-fry-seurat | pipeline-skill **wins** for Seurat HTODemux tasks; paper-skill (Srivastava 2019 alevin) is quantifier-focused and will still be dropped per the v2 plan (Seurat not installed). |
| read-alignment-pangenome | neither arm is well-suited for an R task (both honestly say so). |

Net observation: **pipeline-skill consistently beats paper-skill for workflows where downstream analysis lives in the repo's own `.R` scripts** (akinyi, rna-seq-star-deseq2, epigen-rnaseq, cite-seq). For workflows dominated by shell/Python (`lwang-…-rna_seq`, `read-alignment-pangenome`, most of `cellranger-multi`) the pipeline-skill is still useful for parameters but won't generate R code — that's consistent with the v2 plan's "mostly shell; likely no R task" notes.

## Known gaps / follow-ups

- `fritjoflammers-snakemake-methylanalysis-finish` is the only workflow that truncated. 33 files competed for the 80 KB budget; the low-priority ones (README + config) were included but some mid-priority R helper scripts fell off the tail. Re-running with `--max-total 120000` would fit everything (the raw sum of included-sized files was ~99 KB) and would likely surface the actual MethylKit DMR / DSS call sites. Cost impact: +~$0.02.
- `lwang-genomics__NGS_pipeline_sn` hosts rna_seq / chip_seq / atac_seq in the same directory. The generated skill covers all three because we pass the whole dir; if we only want the rna_seq view we'd need a per-assay file filter (`include only rna_seq.smk + shared config + README`). Punted to Subagent D's injection layer.
- `read-alignment-pangenome-finish` and `lwang-…-rna_seq-finish` emit no R code snippets by design. If an R-task arm needs code for these, the paper-skill or llm-plan-skill is the better choice, not pipeline-skill.
- Token counts here are OpenRouter's usage report (`resp.usage.prompt_tokens`, `resp.usage.completion_tokens`). Prompt-cache discounts (if any) are not reflected in the cost column.

## Total spend

**≈ $0.29** for the 8 workflows (vs. $0.40 budget). Rerunning methylanalysis at 120 KB cap would push this to ~$0.31.
