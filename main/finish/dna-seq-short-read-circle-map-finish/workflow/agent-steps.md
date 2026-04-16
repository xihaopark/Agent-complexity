# dna-seq-short-read-circle-map-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__dna-seq-short-read-circle-map`
- Source snakefile: `../workflow_candidates/snakemake-workflows__dna-seq-short-read-circle-map/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `bam_index`
2. `get_genome`
3. `bwa_index`
4. `genome_faidx`
5. `genome_dict`
6. `get_known_variants`
7. `remove_iupac_codes`
8. `tabix_known_variants`
9. `cutadapt_pe`
10. `bwa_mem`
11. `merge_unit_bams_per_sample`
12. `recalibrate_base_qualities`
13. `apply_bqsr`
14. `samtools_queryname_sort`
15. `circle_map_extract_reads`
16. `samtools_sort_candidates`
17. `circle_map_realign`
18. `clean_circle_map_realign_output`
19. `render_datavzrd_config`
20. `datavzrd`
21. `all`
