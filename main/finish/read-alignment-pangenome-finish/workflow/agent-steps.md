# read-alignment-pangenome-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__read-alignment-pangenome`
- Source snakefile: `../workflow_candidates/snakemake-workflows__read-alignment-pangenome/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `bam_index`
2. `tabix_known_variants`
3. `get_genome`
4. `genome_faidx`
5. `genome_dict`
6. `get_known_variants`
7. `remove_iupac_codes`
8. `bwa_index`
9. `get_pangenome`
10. `get_sra`
11. `fastp_pipe`
12. `fastp_se`
13. `fastp_pe`
14. `merge_trimmed_fastqs`
15. `map_reads_bwa`
16. `count_sample_kmers`
17. `create_reference_paths`
18. `map_reads_vg`
19. `reheader_mapped_reads`
20. `fix_mate`
21. `add_read_group`
22. `sort_alignments`
23. `annotate_umis`
24. `mark_duplicates`
25. `calc_consensus_reads`
26. `map_consensus_reads`
27. `merge_consensus_reads`
28. `sort_consensus_reads`
29. `recalibrate_base_qualities`
30. `apply_bqsr`
31. `assign_primers`
32. `filter_primerless_reads`
33. `trim_primers`
34. `map_primers`
35. `filter_unmapped_primers`
36. `primer_to_bed`
37. `build_primer_regions`
38. `all`
