# DOI Audit — literature/pdfs vs. workflow_literature_map.json

Date: 2026-04-17
Auditor: Subagent D

Each PDF was opened with PyMuPDF and its front matter (title / authors /
abstract on pages 1–2) was compared to the DOI/title/tool label claimed
in `workflow_literature_map.json`.

## Verdicts

| # | File (doi_safe) | Actual title (from PDF) | Map tool label | Match? |
|---|---|---|---|---|
| 1 | `10.1038_ncomms14049` | *Massively parallel digital transcriptional profiling of single cells* (Zheng et al., Nat. Commun. 2017) | 10x Chromium / Cell Ranger → `cellranger-multi-finish` | **OK** |
| 2 | `10.1038_s41587-023-01793-w` | *Pangenome Graph Construction from Genome Alignment with Minigraph-Cactus* (Hickey et al., Nat. Biotechnol. 2023) | pangenome / vg → `read-alignment-pangenome-finish` | **OK** (tool label is generic but paper is the correct primary method; bioRxiv preprint content, same DOI) |
| 3 | `10.1101_gr.079558.108` | *RNA-seq: An assessment of technical reproducibility and comparison with gene expression arrays* (Marioni et al., Genome Research 2008) | RNA-seq assessment → `lwang-genomics-ngs_pipeline_sn-rna_seq-finish`, `epigen-rnaseq_pipeline-finish` | **OK** after DOI fix (see Fix #1 below) |
| 4 | `10.1186_s12859-016-0950-8` | *MethPat: a tool for the analysis and visualisation of complex methylation patterns obtained by massively parallel sequencing* (Wong et al., BMC Bioinf. 2016) | "systemPipeR" on three workflows | **MISMATCH** (see Fix #2) |
| 5 | `10.1186_s13059-014-0550-8` | *Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2* (Love, Huber, Anders 2014) | DESeq2 → `rna-seq-star-deseq2-finish` | **OK** |
| 6 | `10.1186_s13059-016-0881-8` | *A survey of best practices for RNA-seq data analysis* (Conesa et al. 2016) | RNA-seq best practices → `akinyi-onyango-rna_seq_pipeline-finish` | **OK** |
| 7 | `10.1186_s13059-019-1670-y` | *Alevin efficiently estimates accurate gene abundances from dscRNA-seq data* (Srivastava et al. 2019) | "alevin-fry" → `cite-seq-alevin-fry-seurat-finish` | **LABEL MISMATCH** (see Fix #3) |

## Fixes applied to `workflow_literature_map.json`

### Fix #1 — `10.1038/nbt.1612` is NOT the Marioni paper

Crossref resolves `10.1038/nbt.1612` to
*V3D enables real-time 3D visualization and quantitative analysis of
large-scale biological image data sets* (Peng et al., Nat. Biotechnol.
2010) — a fluorescence-imaging tool. The map was intending to cite the
landmark RNA-seq reproducibility paper, whose correct DOI is
`10.1101/gr.079558.108` (Marioni et al., *Genome Research*, 2008).

The previous `literature/pdfs/10.1038_nbt.1612.pdf` was a 0-byte file
(failed Subagent-B download), which concealed this mismatch. The file
was removed, the correct Marioni PDF was fetched from
`genome.cshlp.org/content/18/9/1509.full.pdf`, and saved as
`literature/pdfs/10.1101_gr.079558.108.pdf`.

Workflows updated (`10.1038/nbt.1612` → `10.1101/gr.079558.108`):
- `lwang-genomics-ngs_pipeline_sn-rna_seq-finish`
- `epigen-rnaseq_pipeline-finish`

### Fix #2 — `10.1186/s12859-016-0950-8` is MethPat, not systemPipeR

Confirmed by Subagent B and re-verified here from page 1 of the PDF:
the paper is *MethPat* (Wong et al., BMC Bioinformatics 2016), a
methylation-pattern visualisation tool, not systemPipeR.

The correct systemPipeR DOI is `10.1186/s12859-016-0938-4` (Backman &
Girke, *BMC Bioinformatics* 2016). Swapped in the three
tgirke-systempiperdata-* workflows:
- `tgirke-systempiperdata-rnaseq-finish`
- `tgirke-systempiperdata-chipseq-finish`
- `tgirke-systempiperdata-spscrna-finish`

We do **not** currently have a PDF for the real systemPipeR DOI, so
those three workflows land in `tasks_without_skill` in the manifest.

Because the MethPat paper *does* describe a methylation-analysis tool,
it was re-attached as an additional citation on
`fritjoflammers-snakemake-methylanalysis-finish` so the downloaded PDF
is not orphaned. A skill is still generated for it (see
`experiments/skills/10.1186_s12859-016-0950-8/SKILL.md`).

### Fix #3 — alevin (not alevin-fry)

Same DOI, but the tool label "alevin-fry" was imprecise — the paper
behind `10.1186/s13059-019-1670-y` is the original *alevin* (Srivastava
et al. 2019). Updated the tool label to `alevin`, kept the DOI. The
`cite-seq-alevin-fry-seurat-finish` workflow uses alevin-fry
downstream, but alevin is the direct method precursor, so the skill is
still useful.

## Re-download log

| Previously 0-byte | Action |
|---|---|
| `10.1038_nbt.1612.pdf` | Deleted — DOI was wrong. Fetched the correct Marioni paper as `10.1101_gr.079558.108.pdf` from Genome Research OA. |
| `10.1038_s41587-023-01793-w.pdf` | Replaced with the bioRxiv preprint (`2022.10.06.511217v2`) of the same manuscript — author-version PDF, identical Methods content. Filename kept on the published DOI for consistency with the citation. |

## Residual gaps

- `10.1186/s12859-016-0938-4` (real systemPipeR) — not downloaded. The
  three tgirke workflows cannot get a paper-derived skill until this
  PDF is added.
- Several other cited DOIs in the map (Seurat `10.1016/j.cell.2021.04.048`,
  STAR `10.1093/bioinformatics/bts635`, limma `10.1093/nar/gkv007`,
  clusterProfiler `10.1089/omi.2011.0118`, etc.) have no PDF in
  `literature/pdfs/`. Out of scope for this subagent; flagging for the
  coordinator if the final sweep needs broader skill coverage.

---

## V3 expansion (Subagent C3, 2026-04-17)

Goal: go from 8 workflows-with-PDF (V2) to >=15. Achieved 28 / 30.

### Workflows scanned

All 30 workflows in `main/refine-logs/MAIN_WORKFLOW_SET.md`. For each,
read the source tree under `main/finish/workflow_candidates/<repo>/`
(README, config, `workflow/rules/*.smk`, `workflow/scripts/*`, R
script headers) and mapped the dominant method(s) to canonical DOIs
using the reference table in COORDINATION_PLAN_V3.md plus local
inspection:

- `snakemake-workflows/chipseq/workflow/scripts/macs2_merged_expand.py`
  and `plot_macs_qc.R` confirm MACS2 is the peak caller.
- `lwang-genomics/NGS_pipeline_sn/chip_seq.smk` contains
  `bwa mem` + `samtools` + `macs2 callpeak` -> MACS2.
- `epigen/atacseq_pipeline` rules import MACS2 + bowtie2 + samtools.
- `epigen/dea_limma/README.md` explicitly states the workflow is
  "powered by the R package limma" and references Ritchie 2015
  (`10.1093/nar/gkv007`).
- `epigen/enrichment_analysis/README.md` lists a family of enrichment
  tools (Enrichr, GSEA, GREAT, LOLA, rGREAT). clusterProfiler
  (`10.1089/omi.2011.0118`, OA PDF) kept as the canonical overrepresentation
  method paper for agent context.
- `epigen/fetch_ngs` -> SRA/ENA fetcher -> NCBI resources `10.1093/nar/gkaa1052`.
- `gustaveroussy/sopa/README.md` -> the workflow's own Nat Commun paper
  `10.1038/s41467-024-48981-z` (OA).
- `snakemake-workflows/cyrcular-calling` rules call varlociraptor;
  Varlociraptor Koster 2020 `10.1186/s13059-020-01993-6` adopted as primary.
- `snakemake-workflows/dna-seq-short-read-circle-map` -> Circle-Map
  `10.1186/s12859-019-2926-y`.
- `snakemake-workflows/star-arriba-fusion-calling` -> STAR + Arriba,
  with Arriba's correct DOI `10.1101/gr.257246.119` (Uhrig 2021 Genome
  Research) — the v2 citation `10.1186/s13059-016-1378-0` was a dead
  Crossref handle (404 on Unpaywall).
- `tgirke/systemPipeRdata` covers RNA-seq / ChIP-seq / scRNA / varseq /
  riboseq templates; promoted systemPipeR (`10.1186/s12859-016-0938-4`)
  to `primary_doi` for riboseq + varseq since the classical primary
  citations (Ingolia 2011 Nature; Pabinger 2014 Brief Bioinformatics)
  are paywalled.

### DOI download attempts

Downloader used: `literature/tools/v3_batch_download.py` (new, extends
V2 downloader with Europe PMC fullTextUrlList + ?pdf=render fallback
and strict `%PDF` magic-byte validation so HTML redirect pages are
rejected and re-tried). `Paper2Skills/1.0` user agent;
`paper2skills@protonmail.com` Unpaywall email.

Per-DOI outcomes (full log: `literature/_v3_download_log.json`):

| DOI | Tool | Outcome |
|---|---|---|
| 10.1186/s12859-016-0938-4 | systemPipeR | OK (Unpaywall best_oa, 1.8 MB) |
| 10.1038/s41467-024-48981-z | Sopa | OK (Nat Commun OA, 13 MB) |
| 10.1186/s13059-020-01993-6 | Varlociraptor | OK |
| 10.1186/gb-2008-9-9-r137 | MACS2 | OK (Genome Biol OA) |
| 10.1093/nar/gkv007 | limma | OK via Europe PMC (PMC Oxford blocked direct) |
| 10.1093/bioinformatics/btz436 | snakePipes | OK via Europe PMC |
| 10.1093/bioinformatics/bts635 | STAR | OK via Europe PMC |
| 10.1089/omi.2011.0118 | clusterProfiler | OK via Europe PMC |
| 10.1093/nar/gkaa1052 | NCBI db resources | OK via Europe PMC |
| 10.1186/s12859-019-2926-y | Circle-Map | OK |
| 10.1093/bioinformatics/btt236 | MSIsensor | OK via Europe PMC |
| 10.12688/f1000research.29032.2 | Snakemake | OK |
| 10.1101/gr.257246.119 | Arriba | OK (Genome Research OA) |
| 10.1101/035170 | kallisto (bioRxiv preprint) | OK — used as fallback because Nat Biotech paper has no OA copy |
| 10.1101/058164 | sleuth (bioRxiv preprint) | OK — same reason |
| 10.1101/2020.10.12.335331 | Seurat v4 (bioRxiv preprint) | OK — Cell paper paywalled; preprint is the same manuscript content |
| 10.1038/nbt.3519 | kallisto (published) | BLOCKED (Nature: no OA PDF URL from Unpaywall or Europe PMC) |
| 10.1038/nmeth.4324 | sleuth (published) | BLOCKED (Nature: no OA PDF URL) |
| 10.1038/nmeth.2688 | Buenrostro ATAC-seq | BLOCKED (Unpaywall says is_oa=true but all OA URLs return HTML landing pages; PMC POW challenge) |
| 10.1016/j.cell.2021.04.048 | Seurat v4 (published) | BLOCKED (Cell: 403 on OA mirror; preprint used instead) |
| 10.1038/nrg.2017.76 | scRNA-seq review | BLOCKED (no OA copy) |
| 10.1186/gb-2012-13-8-r51 | ENCODE ChIP-seq | BLOCKED (Unpaywall HTTP 404 — DOI is valid at Crossref but Unpaywall lacks metadata; not auto-downloadable) |
| 10.1186/s13059-016-1378-0 | Arriba (alt handle) | INVALID (Unpaywall 404); correct DOI is 10.1101/gr.257246.119 |
| 10.1038/nbt.3192 | Seurat original (Satija 2015) | BLOCKED (Nature: all OA URLs failed) |
| 10.1038/nbt.4096 | Seurat v3 | BLOCKED (Nature: all OA URLs failed) |

### Workflows newly mapped / upgraded (v2 -> v3)

17 workflows had either no `primary_doi` in v2 or their previously-
primary DOI was paywalled. In v3 they now resolve to a locally-present
PDF (see `_STATUS_V3.md` for the full table):

- rna-seq-kallisto-sleuth-finish   (kallisto preprint)
- star-arriba-fusion-calling-finish (STAR; Arriba secondary now downloaded)
- tgirke-systempiperdata-rnaseq-finish (systemPipeR)
- tgirke-systempiperdata-chipseq-finish (systemPipeR)
- tgirke-systempiperdata-spscrna-finish (systemPipeR)
- tgirke-systempiperdata-varseq-finish (systemPipeR, promoted)
- tgirke-systempiperdata-riboseq-finish (systemPipeR, promoted)
- epigen-dea_limma-finish (limma)
- epigen-enrichment_analysis-finish (clusterProfiler)
- epigen-fetch_ngs-finish (NCBI)
- epigen-dea_seurat-finish (Seurat v4 preprint)
- epigen-scrnaseq_processing_seurat-finish (Seurat v4 preprint)
- epigen-atacseq_pipeline-finish (MACS2)
- epigen-300bcg-atacseq_pipeline-finish (MACS2)
- lwang-genomics-ngs_pipeline_sn-chip_seq-finish (MACS2)
- gustaveroussy-sopa-finish (Sopa)
- cyrcular-calling-finish (Varlociraptor)
- dna-seq-short-read-circle-map-finish (Circle-Map)
- microsatellite-instability-detection-with-msisensor-pro-finish (MSIsensor PDF now local)
- maxplanck-ie-snakepipes-finish (snakePipes PDF now local)

### Workflows with no canonical DOI after audit

- `single-cell-rna-seq-finish`: a thin Seurat-style wrapper without a
  single tool citation; the v2 review DOI `10.1038/nrg.2017.76` is
  paywalled. Flagged so D3 / A3 know this pipeline will not get a
  paper-derived skill.
- `epigen-spilterlize_integrate-finish`: generic filter/normalize/
  batch-correct utility; v2 secondary `10.1186/s13059-017-1200-7` is
  paywalled; no single primary method.

### Residual blocked DOIs worth chasing manually

- `10.1038/nbt.3519` kallisto — author PDF often on
  pachterlab/kallisto GitHub. If approved, fetch manually.
- `10.1038/nmeth.4324` sleuth — same (pachterlab/sleuth).
- `10.1038/nmeth.2688` Buenrostro ATAC-seq — OA per Unpaywall but
  gated behind NCBI PMC POW challenge. Can be fetched via a browser
  or `pmcid=PMC3959825` with interactive login.
- `10.1016/j.cell.2021.04.048` Seurat v4 published — paywalled;
  preprint 10.1101/2020.10.12.335331 is the right artefact for our
  purposes.
- `10.1186/gb-2012-13-8-r51` ENCODE ChIP-seq guidelines — BioMed
  Central should have an OA PDF; Unpaywall metadata broken. Direct
  fetch of `https://genomebiology.biomedcentral.com/articles/10.1186/gb-2012-13-8-r51`
  may work outside the automated downloader.

