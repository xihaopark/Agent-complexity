# Paper-sensitive R-task: clusterprofiler_gsea_vs_ora

**Design intent:** enrichment analysis — **ORA (`enrichGO`) on significant genes only** loses ranking information; **GSEA (`gseGO`)** uses full ranked stats. The **clusterProfiler** paper/documentation discusses both.

**Conceptual source:** `epigen-enrichment_analysis-finish`.

## Your goal

You are given:

- `input/de_table.csv` — contains all genes tested in a DE screen with columns at least: `gene_id`, `log2FoldChange`, `padj`.
- `input/org_db.txt` — one line: `org.Hs.eg.db` or `org.Mm.eg.db` (which organism package to use).

You must:

1. Run **`gseGO`** (GSEA mode) on **Gene Ontology BP**, using **ranked genes** (rank by **signed statistic** you derive from `log2FoldChange` and `padj`, e.g. `-sign(LFC)*log10(p)` — document your ranking in code comments).
2. Export **`output/gsea_results.tsv`** with columns at minimum: `ID,Description,NES,pvalue,p.adjust,qvalue` (clusterProfiler defaults).

Optionally also write `output/ora_results.tsv` from **ORA on padj < 0.05** for comparison — **not scored**, but allowed.

## Deliverables

- `output/gsea_results.tsv` (required)

Then `submit_done(success=true)`.
