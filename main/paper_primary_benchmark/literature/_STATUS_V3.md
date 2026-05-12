# Literature coverage — V3 status

Generated: 2026-04-17 (Subagent C3).

## Headline counts

- **Workflows with at least one locally-downloaded PDF: 28 / 30** (v2: 8).
- **Total PDFs in `literature/pdfs/`: 23** (v2: 7).
- **DOIs mapped with `primary_doi` in v3: 28 / 30** (`single-cell-rna-seq-finish` and `epigen-spilterlize_integrate-finish` deliberately left null — see blocked-DOIs section).

## Per-workflow table

`Y` = primary_doi PDF is present in `literature/pdfs/` with PDF magic bytes (`%PDF`) and non-trivial size.

| # | workflow_id | primary_tool | primary_doi | pdf? | pdf_size (bytes) |
|---|---|---|---|---|---|
| 1 | rna-seq-kallisto-sleuth-finish | kallisto (bioRxiv preprint) | 10.1101/035170 | Y | 352,751 |
| 2 | star-arriba-fusion-calling-finish | STAR | 10.1093/bioinformatics/bts635 | Y | 381,715 |
| 3 | tgirke-systempiperdata-rnaseq-finish | systemPipeR | 10.1186/s12859-016-0938-4 | Y | 1,795,700 |
| 4 | rna-seq-star-deseq2-finish | DESeq2 | 10.1186/s13059-014-0550-8 | Y | 2,430,626 |
| 5 | epigen-dea_seurat-finish | Seurat v4 (bioRxiv preprint) | 10.1101/2020.10.12.335331 | Y | 12,184,056 |
| 6 | epigen-scrnaseq_processing_seurat-finish | Seurat v4 (bioRxiv preprint) | 10.1101/2020.10.12.335331 | Y | 12,184,056 |
| 7 | cite-seq-alevin-fry-seurat-finish | alevin | 10.1186/s13059-019-1670-y | Y | 1,905,903 |
| 8 | single-cell-rna-seq-finish | — | — | N | — |
| 9 | epigen-fetch_ngs-finish | NCBI / SRA toolkit | 10.1093/nar/gkaa1052 | Y | 1,978,801 |
| 10 | epigen-dea_limma-finish | limma | 10.1093/nar/gkv007 | Y | 1,080,129 |
| 11 | epigen-enrichment_analysis-finish | clusterProfiler | 10.1089/omi.2011.0118 | Y | 709,994 |
| 12 | tgirke-systempiperdata-chipseq-finish | systemPipeR | 10.1186/s12859-016-0938-4 | Y | 1,795,700 |
| 13 | fritjoflammers-snakemake-methylanalysis-finish | MethPat | 10.1186/s12859-016-0950-8 | Y | 3,415,594 |
| 14 | microsatellite-instability-detection-with-msisensor-pro-finish | MSIsensor | 10.1093/bioinformatics/btt236 | Y | 1,155,871 |
| 15 | dna-seq-short-read-circle-map-finish | Circle-Map | 10.1186/s12859-019-2926-y | Y | 34,066,507 |
| 16 | tgirke-systempiperdata-varseq-finish | systemPipeR | 10.1186/s12859-016-0938-4 | Y | 1,795,700 |
| 17 | gustaveroussy-sopa-finish | Sopa | 10.1038/s41467-024-48981-z | Y | 13,315,661 |
| 18 | lwang-genomics-ngs_pipeline_sn-rna_seq-finish | RNA-seq (Marioni 2008) | 10.1101/gr.079558.108 | Y | 710,870 |
| 19 | tgirke-systempiperdata-riboseq-finish | systemPipeR | 10.1186/s12859-016-0938-4 | Y | 1,795,700 |
| 20 | cyrcular-calling-finish | Varlociraptor | 10.1186/s13059-020-01993-6 | Y | 2,546,104 |
| 21 | epigen-300bcg-atacseq_pipeline-finish | MACS2 | 10.1186/gb-2008-9-9-r137 | Y | 405,340 |
| 22 | lwang-genomics-ngs_pipeline_sn-chip_seq-finish | MACS2 | 10.1186/gb-2008-9-9-r137 | Y | 405,340 |
| 23 | cellranger-multi-finish | 10x Chromium / Cell Ranger | 10.1038/ncomms14049 | Y | 1,252,344 |
| 24 | tgirke-systempiperdata-spscrna-finish | systemPipeR | 10.1186/s12859-016-0938-4 | Y | 1,795,700 |
| 25 | epigen-atacseq_pipeline-finish | MACS2 | 10.1186/gb-2008-9-9-r137 | Y | 405,340 |
| 26 | epigen-rnaseq_pipeline-finish | RNA-seq (Marioni 2008) | 10.1101/gr.079558.108 | Y | 710,870 |
| 27 | akinyi-onyango-rna_seq_pipeline-finish | RNA-seq best practices | 10.1186/s13059-016-0881-8 | Y | 1,122,163 |
| 28 | maxplanck-ie-snakepipes-finish | snakePipes | 10.1093/bioinformatics/btz436 | Y | 219,563 |
| 29 | epigen-spilterlize_integrate-finish | — | — | N | — |
| 30 | read-alignment-pangenome-finish | Minigraph-Cactus | 10.1038/s41587-023-01793-w | Y | 3,735,344 |

## PDFs in `literature/pdfs/` (23)

```
10.1038_ncomms14049.pdf             Zheng 2017, 10x Chromium
10.1038_s41467-024-48981-z.pdf      Sopa 2024
10.1038_s41587-023-01793-w.pdf      Minigraph-Cactus 2023
10.1089_omi.2011.0118.pdf           clusterProfiler 2012
10.1093_bioinformatics_bts635.pdf   STAR 2013
10.1093_bioinformatics_btt236.pdf   MSIsensor 2014
10.1093_bioinformatics_btz436.pdf   snakePipes 2019
10.1093_nar_gkaa1052.pdf            NCBI db resources 2021
10.1093_nar_gkv007.pdf              limma 2015
10.1101_035170.pdf                  kallisto (bioRxiv preprint, 2015)
10.1101_058164.pdf                  sleuth (bioRxiv preprint, 2016)
10.1101_2020.10.12.335331.pdf       Seurat v4 (bioRxiv preprint, 2020)
10.1101_gr.079558.108.pdf           Marioni 2008 RNA-seq
10.1101_gr.257246.119.pdf           Arriba 2021
10.1186_gb-2008-9-9-r137.pdf        MACS 2008
10.1186_s12859-016-0938-4.pdf       systemPipeR 2016
10.1186_s12859-016-0950-8.pdf       MethPat 2016
10.1186_s12859-019-2926-y.pdf       Circle-Map 2019
10.1186_s13059-014-0550-8.pdf       DESeq2 2014
10.1186_s13059-016-0881-8.pdf       RNA-seq best practices 2016
10.1186_s13059-019-1670-y.pdf       alevin 2019
10.1186_s13059-020-01993-6.pdf      Varlociraptor 2020
10.12688_f1000research.29032.2.pdf  Snakemake 2021
```

## Blocked / skipped DOIs

| DOI | tool | reason |
|---|---|---|
| 10.1038/nbt.3519 | kallisto (published) | Nature Biotech — no OA PDF URL in Unpaywall or Europe PMC. Preprint 10.1101/035170 used instead. |
| 10.1038/nmeth.4324 | sleuth (published) | Nature Methods — no OA PDF URL. Preprint 10.1101/058164 used instead. |
| 10.1038/nmeth.2688 | Buenrostro ATAC-seq | Unpaywall says `is_oa=true` but every OA URL (Nature / Europe PMC) returned HTML (NCBI PMC proof-of-work challenge). |
| 10.1016/j.cell.2021.04.048 | Seurat v4 (Cell 2021) | Cell Press — 403 on all OA mirrors. Preprint 10.1101/2020.10.12.335331 used instead. |
| 10.1038/nrg.2017.76 | scRNA-seq review (Natureblurb) | no OA copy anywhere. Would need library access. |
| 10.1186/gb-2012-13-8-r51 | ENCODE ChIP-seq guidelines | Unpaywall returns HTTP 404 on this DOI even though it exists at Crossref and BMC. Must be fetched via the BMC landing page outside the automated downloader. |
| 10.1186/s13059-016-1378-0 | (claimed Arriba DOI, v2) | Unpaywall 404; this is NOT the Arriba DOI. Correct one is 10.1101/gr.257246.119 (already downloaded). |
| 10.1038/nbt.3192 | Seurat original (Satija 2015) | Nature Biotech — no OA URL worked. |
| 10.1038/nbt.4096 | Seurat v3 (Stuart 2018) | Nature Biotech — no OA URL worked. |

## Recommended next DOIs to chase (manual)

1. **ENCODE ChIP-seq guidelines** (`10.1186/gb-2012-13-8-r51`) — direct-fetch the PDF from `https://genomebiology.biomedcentral.com/articles/10.1186/gb-2012-13-8-r51` with a full browser UA; Unpaywall metadata is incomplete.
2. **Buenrostro ATAC-seq** (`10.1038/nmeth.2688`, PMC3959825) — the official PDF is at `europepmc.org/articles/PMC3959825` but only behind the NCBI POW challenge. A headless browser or PMC FTP (`ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/...`) can retrieve it.
3. **kallisto** (`10.1038/nbt.3519`) and **sleuth** (`10.1038/nmeth.4324`) — we already have bioRxiv preprints, which is sufficient for paper-derived skills. The published versions would only improve citation fidelity.
4. **Seurat Satija 2015** (`10.1038/nbt.3192`) and **Seurat v3 Stuart 2018** (`10.1038/nbt.4096`) — useful for `epigen-dea_seurat-finish` and `epigen-scrnaseq_processing_seurat-finish`; currently covered by the v4 preprint.
5. **Batch-effects review** (`10.1186/s13059-017-1200-7`) — useful for `epigen-spilterlize_integrate-finish`. No OA copy; alternative: a batch-correction method paper such as Combat-seq (`10.1093/nargab/lqaa078`, OA) or Harmony (`10.1038/s41592-019-0619-0`) could be a better-matched primary method.

## What D3 should do with these results

- `literature/workflow_literature_map.json` is v3 (preserves all v2 entries, adds `primary_doi` + `primary_tool` + `rationale` per workflow, plus a `changes_from_v2` changelog).
- 23 PDFs are ready for the vision adapter; D3 can diff against `experiments/skills/manifest.json.by_workflow_id` (which today still lists 8 entries) to know which 16 new `SKILL.md` files to generate.
- The two uncovered workflows (`single-cell-rna-seq-finish`, `epigen-spilterlize_integrate-finish`) will remain paper-skill-less after D3; A3 should fall back to the pipeline-skill or llm-plan arm for their tasks.
