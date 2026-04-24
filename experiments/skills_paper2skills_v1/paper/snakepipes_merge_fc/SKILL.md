# Paper-Derived Skill: snakePipes Feature Count Integration

> **Source**: 10.1093_bioinformatics_btz436 (snakePipes paper)
> **Note**: This skill describes WORKFLOW-BASED feature count handling, which may NOT match simple file operations

## Key Finding from Paper

snakePipes integrates feature counts from tools like featureCounts or HTSeq into comprehensive analysis workflows, with support for normalization, QC, and differential analysis preparation.

## Method from Paper

> "Feature counts are processed through standardized workflow steps, ensuring consistent handling across different samples and experiments."

## When This Skill Applies

✅ **Use for**: Workflow-integrated feature count processing, automated QC, pipeline-based normalization  
❌ **NOT for**: Simple file merging, direct R data manipulation

## Recommended Implementation (Workflow Context)

```yaml
# snakePipes configuration
quantification_tool: featureCounts  # or HTSeq
normalization: DESeq2_size_factors  # or others
qc_metrics: [coverage, complexity, strand_correlation]
```

```r
# Direct R alternative (when not using workflow):
# fc_list <- lapply(fc_files, read.table, header=TRUE, row.names=1)
# merged_fc <- do.call(cbind, fc_list)
```

## Workflow Features

1. **Automated QC**: Built-in quality metrics
2. **Normalization**: Integrated normalization methods
3. **Batch Handling**: Automatic batch effect detection
4. **Consistency**: Ensures uniform processing

## Mismatch Warning

⚠️ **This skill may NOT be suitable for tasks involving**:
- Simple feature count file concatenation
- Direct R I/O without workflow context
- Basic data frame operations

For simple feature count merging, use standard R I/O functions.
