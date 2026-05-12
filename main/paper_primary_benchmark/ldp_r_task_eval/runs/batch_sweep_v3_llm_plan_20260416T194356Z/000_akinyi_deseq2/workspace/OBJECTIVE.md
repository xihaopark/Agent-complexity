# Real R-task: akinyi_deseq2

**Pipeline provenance:** `akinyi-onyango-rna_seq_pipeline-finish` (family: `rna`, stage: `late`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given a featureCounts-style count matrix in `input/featureCounts_output.txt`.
It has columns: Geneid, Chr, Start, End, Strand, Length, followed by 6 sample
columns named sample_0..sample_5. The first 3 samples are condition_A and the last
3 are condition_B. Rows starting with `ERCC-` must be dropped.

Run DESeq2 differential expression (`design = ~condition`) and produce two outputs:
  - `output/deseq2_up.txt`: genes with log2FoldChange >= 2 (rownames = Geneid)
  - `output/deseq2_down.txt`: genes with log2FoldChange <= -2
Both must be written with `write.table(..., col.names=TRUE, row.names=TRUE, quote=FALSE)`.
Filter out rows where log2FoldChange or padj is NA before the up/down split.

## Deliverables

- At least `output/deseq2_up.txt` must exist when you submit.
- Full output set expected: deseq2_up.txt, deseq2_down.txt under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
