# Real R-task: snakepipes_merge_fc

**Pipeline provenance:** `maxplanck-ie-snakepipes-finish` (family: `rna`, stage: `early`, difficulty: `1`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given four per-sample featureCounts outputs under `input/`:
`sampleA.counts.txt`, `sampleB.counts.txt`, `sampleC.counts.txt`,
`sampleD.counts.txt` — tab-separated with columns
`Geneid, Chr, Start, End, Strand, Length, <sampleBAM>`.

Merge all four files by `Geneid` (outer join) into a single counts matrix whose
rownames are `Geneid` and whose columns are the basenames (with `.counts.txt`
stripped) of each input. Save to `output/merged_counts.tsv` using
`write.table(..., sep='\t', quote=F, col.names=NA)`.

## Deliverables

- At least `output/merged_counts.tsv` must exist when you submit.
- Full output set expected: merged_counts.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
