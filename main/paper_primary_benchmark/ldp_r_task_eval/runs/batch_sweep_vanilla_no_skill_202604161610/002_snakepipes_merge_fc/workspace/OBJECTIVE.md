# Real R-task: snakepipes_merge_fc

**Pipeline provenance:** `maxplanck-ie-snakepipes-finish` (family: `rna`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given three per-sample featureCounts files under `input/` named
`sampleA.counts.txt`, `sampleB.counts.txt`, `sampleC.counts.txt`. Each has 7 tab-delimited
columns: Geneid, Chr, Start, End, Strand, Length, <sample_counts>.

Merge them into `output/merged_counts.tsv` keyed by Geneid using outer join.
The output should be tab-delimited, `quote=FALSE`, `col.names=NA`, rownames = Geneid,
with the original Geneid column dropped (so the final columns are just the sample names).
The basename prefix (everything before `.counts.txt`) is the column name for that sample.

## Deliverables

- At least `output/merged_counts.tsv` must exist when you submit.
- Full output set expected: merged_counts.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
