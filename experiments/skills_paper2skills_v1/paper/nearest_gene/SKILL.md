# Paper-Derived Skill: snakePipes Epigenomic Workflows

> **Source**: 10.1093_bioinformatics_btz436 (snakePipes paper)
> **Note**: This skill is for WORKFLOW ORCHESTRATION, which may NOT match simple annotation tasks

## Key Finding from Paper

snakePipes is a workflow package designed to facilitate the processing and analysis of epigenomic data from various assays (ChIP-seq, RNA-seq, ATAC-seq). It leverages the Snakemake workflow management system.

## Method from Paper

> "snakePipes workflows are modular, enabling users to customize and integrate different tools by altering YAML configuration files. The workflows use conda environments to manage dependencies."

## When This Skill Applies

✅ **Use for**: Complex workflow management, multi-step pipeline orchestration, cluster execution  
❌ **NOT for**: Simple gene annotation, single-step operations, direct R analysis

## Recommended Implementation

```yaml
# snakePipes workflow configuration
# cluster.yaml: Configuration for cluster execution
# <organism>.yaml: Genome, indexes, and annotations
# env.yaml: Conda environment specifications
# defaults.yaml: Workflow default settings
```

```r
# Note: snakePipes is implemented using Snakemake, not directly in R
# Outputs from snakePipes can be analyzed in R
```

## Workflow Steps

1. **Configure**: Set up YAML files for the workflow
2. **Execute**: Run snakemake with proper cluster configuration
3. **Analyze**: Process outputs in R

## Mismatch Warning

⚠️ **This skill may NOT be suitable for tasks involving**:
- Simple nearest gene annotation
- Direct GenomicRanges operations
- Single-step R analysis
- Any task not involving complex workflow orchestration

For simple gene annotation, use standard R packages (GenomicRanges, ChIPseeker) instead.
