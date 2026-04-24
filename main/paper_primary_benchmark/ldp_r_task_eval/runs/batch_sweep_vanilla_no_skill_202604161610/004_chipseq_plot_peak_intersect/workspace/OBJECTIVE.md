# Real R-task: chipseq_plot_peak_intersect

**Pipeline provenance:** `snakemake-workflows-chipseq` (family: `chipseq`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/peak_intersect.tsv`, a two-column tab-separated file where the
first column is an ampersand-delimited combination of sample names (e.g.
`H3K27ac_A&H3K4me3_B`) and the second is the size of that intersection.

Build an UpSetR plot from this combination table (using `UpSetR::fromExpression`)
and write the figure to `output/peak_intersect_upset.pdf`. Use ordered sample sets
(alphabetical, reversed) and cap the plot at 70 intersections, ordered by frequency.

## Deliverables

- At least `output/peak_intersect_upset.pdf` must exist when you submit.
- Full output set expected: peak_intersect_upset.pdf under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
