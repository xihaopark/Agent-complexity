# Paper-sensitive tasks — quick index

| id | chapter | primary tools | expected outputs (agent) | source workflow (conceptual) |
|----|---------|----------------|---------------------------|------------------------------|
| `deseq2_apeglm_small_n` | I — agent limits | DESeq2, apeglm | `output/de_results.csv` | `rna-seq-star-deseq2-finish` |
| `deseq2_lrt_interaction` | I | DESeq2, LRT | `output/interaction_de.csv` | `rna-seq-star-deseq2-finish` |
| `limma_voom_weights` | I | limma, voomWithQualityWeights | `output/de_results_weighted.csv` | `epigen-dea_limma-finish` |
| `macs2_broad_histone` | I | MACS2 | `output/broad_peaks.bed` | `epigen-atacseq_pipeline-finish` |
| `combat_seq_batch` | II — baselines weak | sva, ComBat-seq, DESeq2 | `output/adjusted_counts.tsv`, `output/de_results.csv` | `epigen-dea_limma-finish` + ComBat-seq lit |
| `seurat_sctransform_scaling` | II | Seurat, SCTransform | `output/hvg_top.tsv` | `epigen-scrnaseq_processing_seurat-finish` |
| `clusterprofiler_gsea_vs_ora` | II | clusterProfiler | `output/gsea_results.tsv` | `epigen-enrichment_analysis-finish` |
| `edger_robust_filtering` | II | edgeR | `output/de_robust.tsv` | `epigen-rnaseq_pipeline-finish` |
| `methylkit_diffmeth_params` | III — paper value | methylKit | `output/diff_meth.tsv` | `fritjoflammers-snakemake-methylanalysis-finish` |
| `limma_duplicatecorrelation` | III | limma | `output/paired_de.csv` | `epigen-dea_limma-finish` |
| `seurat_integration_method` | III | Seurat | `output/integration_metrics.tsv` | `epigen-scrnaseq_processing_seurat-finish` |
| `deseq2_shrinkage_comparison` | III | DESeq2 | `output/shrunk_de.csv` | `rna-seq-star-deseq2-finish` |

All tasks are **scaffold** until `reference_output/` is populated and the evaluator is wired.
