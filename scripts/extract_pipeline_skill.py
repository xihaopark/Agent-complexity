#!/usr/bin/env python3
"""Extract pipeline skills from workflow R scripts."""

import re
import argparse
from pathlib import Path

def extract_deseq2_patterns(content: str) -> str:
    """Extract DESeq2 code patterns."""
    patterns = []
    
    # Library loading
    if "library(DESeq2)" in content:
        patterns.append("```r\nlibrary(DESeq2)\n```")
    
    # DESeqDataSet creation
    match = re.search(r'dds\s*<-\s*DESeqDataSetFromMatrix\([^)]+\)', content, re.DOTALL)
    if match:
        patterns.append(f"```r\n# Create DESeqDataSet\n{match.group(0)}\n```")
    
    # DESeq run
    if "DESeq(dds" in content:
        patterns.append("```r\n# Run DESeq2\ndds <- DESeq(dds)\n```")
    
    # Results extraction
    match = re.search(r'results\([^)]+\)', content)
    if match:
        patterns.append(f"```r\n# Get results\nres <- {match.group(0)}\n```")
    
    # LFC shrinkage
    match = re.search(r'lfcShrink\([^)]+\)', content, re.DOTALL)
    if match:
        patterns.append(f"```r\n# Shrink log fold changes\nres <- {match.group(0)}\n```")
    
    return "\n\n".join(patterns) if patterns else ""

def extract_limma_patterns(content: str) -> str:
    """Extract limma code patterns."""
    patterns = []
    
    if "library(limma)" in content:
        patterns.append("```r\nlibrary(limma)\nlibrary(edgeR)\n```")
    
    # DGEList
    match = re.search(r'DGEList\([^)]+\)', content)
    if match:
        patterns.append(f"```r\n# Create DGEList\ndge <- {match.group(0)}\n```")
    
    # calcNormFactors
    if "calcNormFactors" in content:
        patterns.append("```r\n# Normalize\ndge <- calcNormFactors(dge)\n```")
    
    # voom
    match = re.search(r'voom\([^)]+\)', content)
    if match:
        patterns.append(f"```r\n# Voom transform\nv <- {match.group(0)}\n```")
    
    # lmFit
    match = re.search(r'lmFit\([^)]+\)', content)
    if match:
        patterns.append(f"```r\n# Fit linear model\nfit <- {match.group(0)}\n```")
    
    # eBayes
    if "eBayes" in content:
        patterns.append("```r\n# Empirical Bayes\nfit <- eBayes(fit)\n```")
    
    # duplicateCorrelation
    if "duplicateCorrelation" in content:
        match = re.search(r'duplicateCorrelation\([^)]+\)', content, re.DOTALL)
        if match:
            patterns.append(f"```r\n# Estimate correlation\ncorfit <- {match.group(0)}\n```")
    
    # topTable
    if "topTable" in content:
        patterns.append("```r\n# Get top results\nres <- topTable(fit, coef=2, number=Inf)\n```")
    
    return "\n\n".join(patterns) if patterns else ""

def create_skill_md(task_id: str, patterns: str, source_file: str) -> str:
    """Create skill markdown content."""
    family = task_id.split("_")[0]  # deseq2, limma, etc.
    
    return f"""# Pipeline Skill: {task_id}

> Extracted from: `{source_file}`
> Generated: Auto-extracted code patterns

## Code Template

{patterns}

## Common Parameters

- Input: `counts.tsv` (gene × sample matrix)
- Metadata: `coldata.tsv` (sample annotations)
- Output: CSV with DE statistics

## Notes

This template follows standard {family} workflow patterns.
Adapt variable names and contrast specifications to your specific task.
"""

def main():
    parser = argparse.ArgumentParser(description="Extract pipeline skills from R scripts")
    parser.add_argument("--source", required=True, help="Source R script path")
    parser.add_argument("--task", required=True, help="Task ID")
    parser.add_argument("--output", required=True, help="Output SKILL.md path")
    args = parser.parse_args()
    
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: Source file not found: {source_path}")
        return 1
    
    content = source_path.read_text()
    
    # Determine which patterns to extract
    if "DESeq2" in content or "dds <-" in content:
        patterns = extract_deseq2_patterns(content)
    elif "limma" in content or "DGEList" in content:
        patterns = extract_limma_patterns(content)
    else:
        print(f"Warning: No known patterns found in {source_path}")
        patterns = "# No code patterns auto-extracted\n\nPlease review source file manually."
    
    # Create skill markdown
    skill_md = create_skill_md(args.task, patterns, str(source_path))
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(skill_md)
    
    print(f"✓ Pipeline skill written to: {output_path}")
    return 0

if __name__ == "__main__":
    exit(main())
