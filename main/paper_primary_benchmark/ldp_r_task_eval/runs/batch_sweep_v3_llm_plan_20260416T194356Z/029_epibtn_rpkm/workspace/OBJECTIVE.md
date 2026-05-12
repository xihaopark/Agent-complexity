# Real R-task: epibtn_rpkm

**Pipeline provenance:** `joncahn-epigeneticbutton-finish` (family: `rna`, stage: `late`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/genecount.tsv` (featureCounts-style tab-separated table
with a `GID` column plus 6 sample columns; rows with GID matching ^N_ must be
dropped), `input/targets.tsv` (columns `Sample, Replicate`), and
`input/ref_genes.bed` (headerless 6-col BED: `Chr Start Stop Name Value Strand`,
where `Name` contains `ID=gene:<id>;...`).

For each genotype (unique `Sample`), take the per-replicate columns whose names
contain the genotype, compute `avg` across replicates, join with the reference
gene table (on parsed `GID`), compute `RPKM = avg * 1000 / (Stop - Start)`, and
accumulate into a single table `all_rpkm` with columns `GID, Sample, RPKM`.
Write it to `output/results/RNA/DEG/genes_rpkm__runX__mockref.txt` via
`write.table(..., sep='\t', row.names=FALSE, col.names=TRUE, quote=FALSE)`.

## Deliverables

- At least `output/results/RNA/DEG/genes_rpkm__runX__mockref.txt` must exist when you submit.
- Full output set expected: results/RNA/DEG/genes_rpkm__runX__mockref.txt under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
