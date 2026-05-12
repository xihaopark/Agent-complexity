# Paper-Derived Skill: MethPat Methylation Analysis

> **Source**: 10.1186_s12859-016-0950-8 (MethPat paper)
> **Note**: This skill is for METHPAT analysis, which may NOT match simple data processing tasks

## Key Finding from Paper

MethPat is a software tool designed to analyze and visualize complex methylation patterns from bisulfite sequencing data. The tool processes data aligned using Bismark, extracting and summarizing methylation states of CpG sites across multiple epialleles.

## Method from Paper

> "MethPat provides a visual representation of methylation patterns, allowing for the identification of methylation heterogeneity within samples. The tool is particularly useful for visualizing the diversity of epiallelic DNA methylation patterns."

## When This Skill Applies

✅ **Use for**: Complex methylation pattern analysis, DMR detection, epiallele visualization  
❌ **NOT for**: Simple data conversion, file merging, basic filtering

## Recommended Implementation

```r
# MethPat-style analysis workflow
library(methylKit)

# 1. Read methylation data
obj <- readMethylKit(...)

# 2. Filter by coverage (MethPat recommendation)
filtered <- filterByCoverage(obj, lo.count=10, lo.perc=NULL, hi.perc=99.9)

# 3. Normalize
normalized <- normalizeCoverage(filtered, method="median")

# 4. Analyze patterns (complex statistical analysis)
# ... pattern detection code
```

## Parameters from Paper

- **lo.count=10**: Minimum coverage threshold
- **hi.perc=99.9**: Maximum coverage percentile (remove PCR duplicates)
- **method="median"**: Normalization approach

## Mismatch Warning

⚠️ **This skill may NOT be suitable for tasks involving**:
- Simple data format conversion (tibble, data.frame)
- File concatenation or merging
- Basic filtering without statistical analysis
- Any task not involving complex methylation pattern analysis

In case of mismatch, consider using baseline R knowledge instead.
