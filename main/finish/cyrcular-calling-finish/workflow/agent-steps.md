# cyrcular-calling-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__cyrcular-calling`
- Source snakefile: `../workflow_candidates/snakemake-workflows__cyrcular-calling/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `get_genome`
2. `genome_faidx`
3. `minimap2_index`
4. `download_regulatory_annotation`
5. `download_repeatmasker_annotation`
6. `download_gene_annotation`
7. `minimap2_bam`
8. `merge_fastqs`
9. `samtools_index`
10. `samtools_faidx`
11. `bcf_index`
12. `bcftools_concat`
13. `bcftools_sort`
14. `varlociraptor_call`
15. `varlociraptor_alignment_properties`
16. `varlociraptor_preprocess`
17. `scatter_candidates`
18. `sort_bnd_bcfs`
19. `circle_bnds`
20. `cyrcular_generate_tables`
21. `cyrcular_annotate_graph`
22. `reheader_filtered_bcf`
23. `sort_bcf_header`
24. `get_bcf_header`
25. `extract_vcf_header_lines_for_bcftools_annotate`
26. `filter_overview_table`
27. `filter_varlociraptor`
28. `circle_coverage_plot`
29. `circle_graph_plots`
30. `render_datavzrd_config`
31. `copy_qc_plots_for_datavzrd`
32. `copy_graph_plots_for_datavzrd`
33. `datavzrd_circle_calls`
34. `all`
