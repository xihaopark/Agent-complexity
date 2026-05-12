# Real R-task: nearest_gene

**Pipeline provenance:** `maxplanck-ie-snakepipes-finish` (family: `chipseq`, stage: `late`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/peaks_with_nearest.bed` (24-column bedtools-closest
output: 18 CSAW DB columns + 6 nearest-gene columns), `input/t2g.tsv`
(txid → gene_id), and `input/gene_symbol.tsv` (gene_id → symbol). For each
peak, join GeneID via V22=tx and GeneSymbol via the gene_id, and save a TSV
to `output/annotated.bed` with columns
`Chromosome, Start, End, Width, Strand, Score, nWindows, logFC.up, logFC.down,
PValue, FDR, direction, rep.test, rep.logFC, best.logFC, best.test, best.start,
Name, GeneStrand, Distance, GeneID, GeneSymbol` (write.table tab-sep, no row
names, no quotes).

## Deliverables

- At least `output/annotated.bed` must exist when you submit.
- Full output set expected: annotated.bed under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
