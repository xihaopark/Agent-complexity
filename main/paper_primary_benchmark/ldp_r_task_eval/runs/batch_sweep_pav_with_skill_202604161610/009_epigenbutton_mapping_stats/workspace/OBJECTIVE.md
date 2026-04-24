# Real R-task: epigenbutton_mapping_stats

**Pipeline provenance:** `joncahn-epigeneticbutton` (family: `chipseq`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/mapping_stats.tsv`, a tab-separated mapping summary with
columns `Line, Tissue, Sample, Rep, Reference_genome, Total_reads,
Passing_filtering, All_mapped_reads, Uniquely_mapped_reads`. The read-count columns
are formatted as `<count> (<pct>%)`; only the numeric prefix matters.

Render a two-panel PDF at `output/mapping_stats.pdf` (landscape, 10x12 in) with
stacked fill/stack bars per (Line/Tissue/Sample/Rep) showing the breakdown into
Uniquely mapped / Multi-mapping / Unmapped / Filtered reads, faceted by `Line`,
with the title `Mapping statistics for ChIP_demo samples`.

## Deliverables

- At least `output/mapping_stats.pdf` must exist when you submit.
- Full output set expected: mapping_stats.pdf under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
