---
name: pipeline-maxplanck-ie-snakepipes-finish
source_type: pipeline
workflow_id: maxplanck-ie-snakepipes-finish
workflow_dir: /Users/park/code/Paper2Skills-main/main/finish/workflow_candidates/maxplanck-ie__snakePipes
generated_at: 2026-04-16T19:32:04Z
model: openrouter/openai/gpt-4o
files_used: 18
chars_used: 80000
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method
The pipeline is designed for ATAC-seq and ChIP-seq data analysis, focusing on peak calling and differential binding analysis. It uses a combination of tools such as Bowtie2 for alignment, MACS2 for peak calling, and CSAW for differential binding analysis. The pipeline supports both single-end and paired-end data and includes quality control steps using tools like FastQC and Qualimap. It also incorporates additional peak callers like Genrich and HMMRATAC for specific analyses. The pipeline is flexible, allowing for the inclusion of spike-in controls and handling of allelic data.

## Parameters
- `maxFragmentSize`: Maximum fragment size for filtering BAM files.
- `minFragmentSize`: Minimum fragment size for filtering BAM files.
- `genome_size`: Genome size used by MACS2 for peak calling.
- `qval`: Q-value cutoff for peak calling with MACS2.
- `blacklist_bed`: BED file for blacklisting regions in peak calling.
- `fragmentCountThreshold`: Threshold for fragment count filtering.
- `pairedEnd`: Boolean indicating if the data is paired-end.
- `aligner`: Aligner to use (e.g., Bowtie2, HISAT2, STAR).
- `bowtie2_index`: Index for Bowtie2 alignment.
- `hisat2_index`: Index for HISAT2 alignment.
- `star_index`: Index for STAR alignment.
- `sampleSheet`: Path to the sample sheet for CSAW and DESeq2 analyses.
- `fdr`: False discovery rate for differential analysis.
- `absBestLFC`: Absolute best log fold change for differential analysis.
- `windowSize`: Window size for CSAW analysis.
- `useSpikeInForNorm`: Boolean indicating if spike-in normalization is used.
- `externalBed`: External BED file for peak analysis.

## Commands / Code Snippets
```r
# CSAW differential binding analysis
rule CSAW:
    input:
        peaks = getInputPeaks(peakCaller, chip_samples, genrichDict),
        sampleSheet = sampleSheet,
        insert_size_metrics = getSizeMetrics(),
        scale_factors = getScaleFactors() if useSpikeInForNorm else []
    output:
        "CSAW_{}_{}/CSAW.session_info.txt".format(peakCaller, sample_name),
        "CSAW_{}_{}/DiffBinding_analysis.Rdata".format(peakCaller, sample_name),
        expand("CSAW_{}_{}".format(peakCaller, sample_name) + "/Filtered.results.{change_dir}.bed", change_dir=change_direction),
        "CSAW_{}_{}".format(peakCaller, sample_name) + "/Full.results.bed"
    script: "../rscripts/CSAW.R"

# DESeq2 differential expression analysis
rule DESeq2:
    input:
        counts_table = lambda wildcards : "featureCounts/counts_allelic.tsv" if 'allelic-mapping' in mode or 'allelic-counting' in mode or 'allelic-whatshap' in mode else "featureCounts/counts.tsv",
        sampleSheet = sampleSheet,
        symbol_file = "Annotation/genes.filtered.symbol"
    output:
        "{}/DESeq2.session_info.txt".format(get_outdir("DESeq2",sampleSheet,LRT))
    script: "{params.script}"
```

## Notes for R-analysis agent
- The pipeline uses MACS2 for peak calling, which requires specifying the genome size and q-value cutoff.
- CSAW is used for differential binding analysis, and it requires a sample sheet and peak files as input. Ensure the sample sheet is correctly formatted.
- DESeq2 is used for differential expression analysis, with inputs from featureCounts or Salmon. Check that the counts table and sample sheet are correctly specified.
- The pipeline supports spike-in normalization; verify if this is needed for your analysis.
- Ensure that the appropriate aligner index is available for the chosen aligner (Bowtie2, HISAT2, or STAR).
- The pipeline can handle allelic data; ensure the correct mode is set if this analysis is required.
