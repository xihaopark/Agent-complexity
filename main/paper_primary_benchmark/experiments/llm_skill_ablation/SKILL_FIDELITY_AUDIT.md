# Paper-Skill Fidelity Audit — 20 paper-derived skills

**Auditor:** Subagent G3-A
**Date:** 2026-04-17
**Scope:** every `<doi_safe>` in
`main/paper_primary_benchmark/experiments/skills/manifest.json → by_doi`
(n = 20). PDFs read with `PyMuPDF (fitz) 1.27` (first 8–15 pages). SKILL.md files
read verbatim; YAML front-matter and ` ```markdown` fences stripped for
comparison.

## Headline

- **5 of 20 skills are derived from the wrong paper** because the
  DOI → source-tool mapping in `manifest.json` is broken: the DOI resolves to a
  different paper than the declared tool. Skills are internally consistent with
  the PDF they read, but they describe the *wrong* tool relative to what the
  pipeline they support actually uses. These are the five flagged as *generic /
  wrong* below.
- **5 of 20 skills are genuinely paper-specific** with named functions /
  flags / parameters from the paper: MACS2, limma, clusterProfiler, snakePipes,
  Varlociraptor.
- **10 of 20 are "mixed"**: paper-faithful in the *Method* section but
  contain generic-sounding `Parameters` or `Notes for R-analysis agent`
  bullets (e.g. "consider using `edgeR` or `DESeq2`" style filler).
- **Structural completeness is 20 / 20** — every skill has the four expected
  sections (`Method`, `Parameters`, `Commands / Code Snippets`, `Notes for R-analysis agent`).
- **Pipeline-vs-paper overlap:** paper-skills carry 72–85 % tokens that are
  NOT in the matched pipeline-skill. The two arms (`skill` vs
  `skill_pipeline`) are *not* equivalent; paper-skills genuinely add
  methodology framing. This justifies running them as distinct arms.

## Single most critical finding

**Five out of twenty DOIs in `manifest.json` point to the wrong paper PDF relative
to the declared `source_tool`.** The paper-skill generator faithfully extracted
content from whatever PDF it was given, so the skill describes a *real* paper —
just not the paper the pipeline workflow is supposed to cite. For the four
pipelines affected (`snakemake-workflows-msisensor-pro-finish`,
`epigen-fetch_ngs-finish`, `dna-seq-short-read-circle-map-finish`,
`rna-seq-kallisto-sleuth-finish`, `tgirke-systempiperdata-*-finish`) the LLM's
"skill" arm receives completely off-topic methodological guidance. Regenerate
from correct DOIs before publishing comparative metrics.

## Summary table

| doi_safe | declared source_tool | paper_match_count<br>(hits/candidates) | accuracy_flags | structural_completeness | paper_specific | paper_novelty_vs_pipeline |
|---|---|:-:|---|:-:|:-:|:-:|
| 10.1186_gb-2008-9-9-r137 | MACS2 | 17/20 | — (flags, defaults, ChIP-Seq all match paper) | 4/4 | **paper-specific** | n/a (no matched pipeline skill indexed) |
| 10.1093_nar_gkv007 | limma | 5/5 | — (`voom`, `lmFit`, `eBayes`, `makeContrasts`, `duplicateCorrelation`, `arrayWeights` all in paper) | 4/4 | **paper-specific** | 72 % novel |
| 10.1089_omi.2011.0118 | clusterProfiler | 7/9 | minor: `pvalueCutoff`/`qvalueCutoff` phrased as "default not specified" | 4/4 | **paper-specific** | n/a |
| 10.1186_s13059-020-01993-6 | Varlociraptor | 3/6 | hits include `VAF threshold`, `Read coverage`; misses: `FDR threshold (γ)`, `Strand bias indicator (β)` exact glyphs | 4/4 | **paper-specific** | n/a |
| 10.1093_bioinformatics_btz436 | snakePipes | 1/5 | low hit count is an artifact of phrase-level candidates ("cluster.yaml" etc.); PDF has 25× "snakepipes" and 3× "snakemake" — concepts match | 4/4 | **paper-specific** (mixed on params) | 77 % novel |
| 10.1186_s13059-014-0550-8 | DESeq2 | 1/4 | code snippet `DESeq(dds)` correct; misses: "Normalization factors (sij)", "Shrinkage degree (di)", "LFC (θ)" as math glyphs | 4/4 | mixed | 75 % novel |
| 10.1093_bioinformatics_bts635 | STAR | 0/5 | phrase-level params ("MMP search direction", "Genome window size") don't match verbatim; body text does cite MMP + suffix-array correctly | 4/4 | mixed | n/a |
| 10.1186_s13059-019-1670-y | alevin | 1/2 | describes PUG, two-step whitelisting — correct; generic "tximport" note | 4/4 | mixed | 77 % novel |
| 10.1101_2020.10.12.335331 | Seurat v4 | 1/1 | describes WNN, modality weights, softmax — correct | 4/4 | mixed (short) | n/a |
| 10.1038_s41467-024-48981-z | Sopa | 2/4 | names Cellpose, Baysor, IOMA — correct; generic *Channel Averaging Method* param | 4/4 | mixed | n/a |
| 10.1186_s12859-016-0950-8 | MethPat | 1/3 | describes Bismark input, epiallele pattern output — correct; `Visualization Type` param generic | 4/4 | mixed | 79 % novel |
| 10.1101_gr.079558.108 | RNA-seq (Marioni 2008) | 3/8 | Poisson, lane effects, Marioni correctly cited; notes mention Bowtie/STAR/rMATS that aren't in paper | 4/4 | mixed | 82 % novel (both pipelines) |
| 10.1038_ncomms14049 | 10x Chromium / Cell Ranger | 3/8 | names `Cell load`, `CellRanger`, `Seurat`; many param names ("Bead load", "UMI length") are phrase inventions not in paper | 4/4 | mixed | 82 % novel |
| 10.1186_s13059-016-0881-8 | RNA-seq best practices | 2/2 | paper is a review, skill is appropriately broad (RPKM/FPKM/TPM, negative binomial); minimal specificity | 4/4 | mixed (generic-by-design) | 78 % novel |
| 10.1038_s41587-023-01793-w | Minigraph-Cactus | 0/2 | "SV size threshold"/"Sequence filter threshold" as phrase-level params; body correctly describes minimizer seed+chain and Cactus pinching | 4/4 | mixed (thin) | 78 % novel |
| **10.1093_bioinformatics_btt236** | **MSIsensor (declared)** | 2/2 | **WRONG PAPER:** PDF is a random-forest metabolic-network paper (0× "msisensor", 0× "microsatellite", 14× "random forest", 54× "metabolic"). Skill accurately summarizes *that* paper — but not MSIsensor. | 4/4 | **generic / wrong paper** | 85 % novel (because unrelated) |
| **10.1093_nar_gkaa1052** | **NCBI / SRA toolkit (declared)** | 6/8 | **WRONG PAPER:** PDF is Asymmetron (0× "SRA", 18× "asymmetron", 85× "asymmetry"). Skill describes Asymmetron CLI (`contained_asymmetries.py`, `orientation.py`). | 4/4 | **generic / wrong paper** | n/a |
| **10.1186_s12859-019-2926-y** | **Circle-Map (declared)** | 5/10 | **WRONG PAPER:** PDF is AutoCryoPicker (0× "circle", 5× "autocryopicker", 74× "cryo-em"). Skill describes cryo-EM particle picking. | 4/4 | **generic / wrong paper** | n/a |
| **10.1101_035170** | **kallisto (declared)** | 3/6 | **WRONG PAPER:** bioRxiv 035170 is the UK10K/HRC haplotype reference panel paper (0× "kallisto", 5× "haplotype reference", 9× "bcftools"). Skill correctly describes *that* paper — imputation, SHAPEIT3, HWE, MAC/MAF — but that's irrelevant to kallisto/sleuth workflows. | 4/4 | **generic / wrong paper** | n/a |
| **10.1186_s12859-016-0938-4** | **systemPipeR (declared)** | 4/6 | **WRONG PAPER:** PDF is Seqinspector (0× "systempiper", 30× "seqinspector"). Skill describes Seqinspector's bigwig-coverage enrichment test. | 4/4 | **generic / wrong paper** | n/a |

Legend: paper_match_count is the count of distinct non-trivial candidate tokens
extracted from the skill (function names, backtick-quoted terms, bolded
params, CamelCase identifiers) that also appear in the first ~15 pages of the
paper PDF. Candidate extraction is intentionally broad; a 1/5 or 2/5 hit ratio
does *not* automatically mean the skill is wrong — many skills use phrase-level
parameter labels ("Genome window size") that do not appear verbatim in the
paper even though the underlying concept is correct. The qualitative
`paper_specific` column integrates that phrase-level analysis.

## Per-DOI 2-sentence verdicts

**10.1186_gb-2008-9-9-r137 (MACS2).** Enumerates 13 MACS command-line flags
(`--gsize`, `--tsize`, `--bw`, `--pvalue`, `--mfold`, `--nolambda`, …) that
appear verbatim in the MACS paper and a well-formed shell snippet. Paper-faithful
and genuinely useful as MACS guidance.

**10.1093_nar_gkv007 (limma).** Explicitly cites `voom`, `normalizeBetweenArrays`,
`arrayWeights`, `duplicateCorrelation`, `makeContrasts`, `lmFit`, `eBayes`,
`topTable` — every function reference is accurate per the limma paper. Gold
standard for the benchmark.

**10.1089_omi.2011.0118 (clusterProfiler).** Names `groupGO`, `enrichGO`,
`enrichKEGG`, `compareCluster`, `pvalueCutoff`, `qvalueCutoff`, BH FDR — all
correct. Short but paper-specific.

**10.1186_s13059-020-01993-6 (Varlociraptor).** Describes the Bayesian latent
variable model, VAF threshold, two-step discovery→classification, posterior
probability FDR control — all core claims of the paper. Some `Notes` bullets
suggest `VarDict`/`Mutect2` as "alternatives" which the paper does not endorse.

**10.1093_bioinformatics_btz436 (snakePipes).** Method section correctly
describes modular Snakemake workflows + YAML config + conda envs. Parameter
block lists the exact config file names (`cluster.yaml`, `<organism>.yaml`,
`env.yaml`, `defaults.yaml`). Thin but accurate.

**10.1186_s13059-014-0550-8 (DESeq2).** Method section (shrinkage, empirical
Bayes on dispersion, Wald test, independent filtering, negative binomial) is
directly from the paper. Code snippet uses `DESeq(dds)` (not `DESeq2(dds)`) –
correct. Parameter labels use the paper's math glyphs (`sij`, `di`, `θ`) so the
verbatim-text matcher misses them even though concepts are right.

**10.1093_bioinformatics_bts635 (STAR).** Describes MMP + suffix array +
stitching/scoring — correct. But the parameter block is five invented
phrase-labels ("Genome window size", "Thread count") rather than actual STAR
option names (`--sjdbOverhang`, `--outFilterMismatchNmax`, etc.). Mixed.

**10.1186_s13059-019-1670-y (alevin).** Method section covers barcode detection,
parsimonious UMI graph (PUG), two-step whitelisting, rescue-EM — paper-faithful.
Generic `Notes` fallback to `tximport`. Overall mixed.

**10.1101_2020.10.12.335331 (Seurat v4 / WNN).** Describes weighted-nearest-neighbor
modality weights + softmax — paper-faithful. Very short, only one distinct
candidate token, so quantitative score is near-degenerate.

**10.1038_s41467-024-48981-z (Sopa).** Names Cellpose, Baysor, IOMA, SpatialData
object — correct per paper. Commands section empty; one invented param
("Channel Averaging Method"). Mixed.

**10.1186_s12859-016-0950-8 (MethPat).** Method accurately describes Bismark
input, epiallele pattern extraction/visualization. Parameters are 3 generic
labels ("Input File", "Visualization Type"). Mixed.

**10.1101_gr.079558.108 (Marioni RNA-seq 2008).** Correctly cites the Marioni
Poisson model, χ² lane-effect test, likelihood ratio test. Notes suggest edgeR,
DESeq2, rMATS — tools that post-date the paper and aren't in it. Mixed.

**10.1038_ncomms14049 (10x Chromium / Cell Ranger).** Describes GEMs, barcoded
gel beads, UMI, 3' capture — correct. Parameter list is five phrase-labels
("Cell load", "Bead load", "UMI length") that aren't formal 10x parameters.
Mixed.

**10.1186_s13059-016-0881-8 (Conesa et al. RNA-seq best practices).** The paper
is itself a review; the skill's generic tone (RPKM/FPKM/TPM, replicates,
negative binomial) matches the paper's scope. Appropriately generic-by-design,
but provides no tool-specific leverage that a pipeline-skill wouldn't already.

**10.1038_s41587-023-01793-w (Minigraph-Cactus).** Correctly describes SV-only
graph construction + Cactus base-level pinching + minimizer seed/chain. Two
phrase-level params ("SV size threshold", "Sequence filter threshold") are not
the binary's actual CLI flags. Thin but paper-faithful.

**10.1093_bioinformatics_btt236 (declared MSIsensor).** 🔴 The PDF under this
DOI is *not* the MSIsensor paper (Niu et al. 2014 is DOI 10.1093/bioinformatics/**btt755**,
not btt236). The PDF present discusses random-forest-based functional mis-annotation
prediction in metabolic networks; the skill faithfully summarizes that paper.
Consequently the MSIsensor pipeline arm receives entirely off-topic guidance.
**Regenerate with correct DOI.**

**10.1093_nar_gkaa1052 (declared NCBI / SRA toolkit).** 🔴 The PDF is the
Asymmetron paper. Skill correctly describes Asymmetron's four CLI scripts
(`consecutive_patterns.py`, `orientation.py`, `contained_asymmetries.py`,
`pairwise_asymmetries.py`). Skill is internally accurate but completely
mis-routed: `epigen-fetch_ngs-finish` does not use Asymmetron. **Regenerate.**

**10.1186_s12859-019-2926-y (declared Circle-Map).** 🔴 The PDF is
AutoCryoPicker (unsupervised cryo-EM particle picking). Skill describes
intensity-based clustering and circular Hough transform. Circle-Map is
an eccDNA circle-detection tool — unrelated. **Regenerate.**

**10.1101_035170 (declared kallisto).** 🔴 bioRxiv 035170 = Huang 2016,
"Improved imputation of low-frequency and rare variants using the UK10K
haplotype reference panel" (not kallisto). Skill correctly describes
SHAPEIT3, HWE filtering, inbreeding coefficient, MAC/MAF thresholds. kallisto
is DOI 10.1038/nbt.3519 (Bray et al. 2016). **Regenerate with
10.1038_nbt.3519.**

**10.1186_s12859-016-0938-4 (declared systemPipeR).** 🔴 PDF is Seqinspector
(functional enrichment for bigwig coverage). systemPipeR is Backman & Girke
2016, DOI 10.1186/s12859-016-1241-0 (different DOI suffix). Skill is
Seqinspector-accurate but wrong tool. Affects five
`tgirke-systempiperdata-*` pipelines. **Regenerate with correct DOI.**

## Skills that need regeneration

**Must regenerate (wrong-paper):**

1. `10.1093_bioinformatics_btt236` → should use MSIsensor DOI `10.1093/bioinformatics/btt755` (Niu et al. 2014)
2. `10.1093_nar_gkaa1052` → manifest labels as "NCBI / SRA toolkit"; pick a correct SRA/fetch_ngs DOI or drop the claim
3. `10.1186_s12859-019-2926-y` → should use Circle-Map DOI `10.1186/s13059-019-1835-8` (Prada-Luengo et al. 2019) or the eccDNA / Circle-Map preprint
4. `10.1101_035170` → should use kallisto DOI `10.1038/nbt.3519` (Bray et al. 2016)
5. `10.1186_s12859-016-0938-4` → should use systemPipeR DOI `10.1186/s12859-016-1241-0` (H Backman & Girke 2016) or Girke/systemPipeR documentation paper

**Consider supplementing (thin but correct):**

- `10.1186_s12859-016-0950-8` (MethPat) — add `methylKit` function names
  (`unite`, `methRead`, `calculateDiffMeth`) that the downstream pipeline
  actually uses; current skill only talks about MethPat concepts.
- `10.1038_s41587-023-01793-w` (Minigraph-Cactus) — add actual CLI flags
  (`-cgfw`, `-l`, `-d 10000`) rather than phrase-level "thresholds".
- `10.1093_bioinformatics_btz436` (snakePipes) — add at least one
  concrete workflow invocation (`DNA-mapping -i data/ -o out/ --DAG`).

## Top 3 "most paper-faithful" skills (advocacy material)

1. **`10.1186_gb-2008-9-9-r137` — MACS.** 17/20 candidate tokens from skill
   appear verbatim in PDF (all CLI flags). The skill is effectively a condensed
   manual page derived directly from the MACS paper, including default values
   (`--gsize=2.7e9`, `--tsize=25`, `--bw=300`, `--pvalue=1e-5`). Ideal showcase
   that paper-skills *can* provide executable guidance.
2. **`10.1093_nar_gkv007` — limma.** 5/5 named functions (`voom`,
   `normalizeBetweenArrays`, `arrayWeights`, `duplicateCorrelation`,
   `makeContrasts`) appear in the paper and are exactly the functions used
   by the `epigen-dea_limma-finish` pipeline's `limma.R` — the paper-skill
   maps cleanly onto the pipeline task `dea_limma`.
3. **`10.1089_omi.2011.0118` — clusterProfiler.** 7/9 candidates match;
   describes the three main enrichment entry points (`groupGO`, `enrichGO`,
   `enrichKEGG`) plus `compareCluster` visualization, BH-FDR, and the
   hypergeometric test. Short and on-target.

## Top 3 "least paper-faithful" skills (regenerate/supplement)

1. **`10.1093_bioinformatics_btt236` (declared MSIsensor).** Actually a
   random-forest metabolic-network paper. Zero words of the extracted skill
   apply to MSIsensor. Highest-impact fix because `msisensor_merge` is the
   only `variant`-family task.
2. **`10.1186_s12859-019-2926-y` (declared Circle-Map).** Actually an AutoCryoPicker
   cryo-EM paper. Affects `dna-seq-short-read-circle-map-finish`, a
   workflow that isn't in the 32-task slice but that is advertised in the
   manifest as paper-covered.
3. **`10.1186_s12859-016-0938-4` (declared systemPipeR).** Actually a
   Seqinspector paper. Affects five `tgirke-systempiperdata-*` pipelines.

## Verdict

Paper-skills that were generated from the *correct* PDF are genuinely paper-specific —
roughly 75 % of their content does not appear in the matched pipeline-skill,
and several (MACS, limma, clusterProfiler, snakePipes, Varlociraptor) cite
precise function/flag names lifted from the paper. These five skills are
sufficient to demonstrate that the paper-skill arm contributes real
methodological framing beyond what a pipeline-skill already provides.

However, **25 % of the manifest is built on wrong-paper assignments.** Before
publishing comparative metrics across the `skill` arm, the five affected DOIs
must be re-sourced to the correct paper and re-generated; otherwise the
paper-skill arm is feeding five tools' worth of irrelevant context into the
LLM, which either quietly hurts or quietly helps (via "what's this random
paper about?") and confounds the ablation.
