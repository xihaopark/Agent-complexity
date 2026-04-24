# Paper-Derived Skill: snakePipes Count Table Management

> **Source**: 10.1093_bioinformatics_btz436 (snakePipes paper)
> **Note**: This skill describes WORKFLOW-BASED merging, which may NOT match simple file operations

## Key Finding from Paper

snakePipes provides structured approaches for managing count tables in complex workflows, including merging samples, quality control, and batch effect handling.

## Method from Paper

> "snakePipes manages count tables through the workflow configuration, ensuring consistent processing across multiple samples and batches."

## When This Skill Applies

✅ **Use for**: Complex workflow-based table management, batch correction, multi-sample integration  
❌ **NOT for**: Simple file concatenation, direct R data.frame merging

## Recommended Implementation (Workflow Context)

```yaml
# snakePipes configuration for count table management
samplesheet: samplesheet.tsv  # Sample metadata
merge_strategy: merge  # How to combine samples
batch_correction: true  # Whether to correct for batch effects
```

```r
# Note: In workflow context, merging is handled by snakemake rules
# Direct R merging would be:
# counts <- do.call(cbind, lapply(files, read.table))
```

## Workflow vs Direct R

| Aspect | Workflow Approach | Direct R Approach |
|--------|------------------|-------------------|
| Configuration | YAML files | Function parameters |
| Execution | snakemake | Direct R code |
| Flexibility | High for pipelines | High for one-off tasks |
| Overhead | Higher (setup) | Lower (direct) |

## Mismatch Warning

⚠️ **This skill may NOT be suitable for tasks involving**:
- Simple count table concatenation
- Direct file I/O operations
- Single-step merging without workflow context

For simple merging, use standard R functions (rbind, cbind, dplyr::bind_rows).
