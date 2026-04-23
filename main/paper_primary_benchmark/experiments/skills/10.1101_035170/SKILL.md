---
name: paper-10-1101-035170
description: >-
  Vision-adapter skill extracted from 10.1101_035170.pdf via openai/gpt-4o
source_pdf: 10.1101_035170.pdf
pages_processed: 8
generator: paper2skills_ab_test/vision_adapter.py
---

```markdown
## Method
The paper describes the creation of a reference panel of 64,976 haplotypes at 39,235,157 SNPs using whole genome sequence data from 20 studies. The method involves combining genotype calls from each study to form a union set of SNP sites with a minor allele count (MAC) of at least 2. Genotype likelihoods were calculated using the 'samtools mpileup' command, and the resulting BCF files were merged. The panel was refined by re-phasing genotypes using the SHAPEIT3 method to improve imputation accuracy. Site filtering was applied to ensure quality, using criteria such as Hardy-Weinberg Equilibrium and inbreeding coefficients.

## Parameters
- **MAC threshold**: Minimum minor allele count for inclusion.
- **MAF threshold**: Minimum minor allele frequency for site inclusion.
- **Ts/Tv ratio**: Transition-to-transversion ratio used for filtering.
- **HWE p-value**: Hardy-Weinberg Equilibrium p-value threshold for filtering.
- **Inbreeding coefficient**: Threshold for filtering sites based on inbreeding.

## Commands / Code Snippets
```bash
# Genotype likelihood calculation
samtools mpileup -g -f reference.fa sample.bam > sample.bcf

# Merging BCF files
bcftools merge file1.bcf file2.bcf -o merged.bcf

# Genotype calling
bcftools call -m -v -o calls.vcf merged.bcf

# Checking for duplicates
bcftools gtcheck -g calls.vcf
```

## Notes for R-analysis agent
- Consider using the `impute` package in R for genotype imputation.
- Ensure input VCF files are pre-processed to match the reference panel's requirements.
- Verify that the input data meets the MAC and MAF thresholds specified.
- Double-check the filtering criteria, especially the Ts/Tv ratio and HWE p-value, to ensure quality control.
- The SHAPEIT3 method is crucial for re-phasing; ensure compatibility with R tools.
```
