---
name: paper-10-1093-nar-gkaa1052
description: >-
  Vision-adapter skill extracted from 10.1093_nar_gkaa1052.pdf via openai/gpt-4o
source_pdf: 10.1093_nar_gkaa1052.pdf
pages_processed: 8
generator: paper2skills_ab_test/vision_adapter.py
---

```markdown
## Method
The Asymmetron toolkit is designed to identify strand asymmetry patterns in biological sequences. It operates on BED-formatted files and uses the Python-based package `pybedtools`. The toolkit provides four main functions: `consecutive_patterns.py`, `contained_asymmetries.py`, `pairwise_asymmetries.py`, and `orientation.py`. These functions analyze strand asymmetries by calculating the frequency of motifs in specific orientations and comparing them to expected distributions. The toolkit evaluates strand asymmetries in non-palindromic sequences by comparing motif occurrences on complementary DNA strands. Statistical significance is assessed using simulations and empirical P-values.

## Parameters
- **N**: Default 1000, number of simulations for calculating strand asymmetry.
- **dmax**: Maximum distance considered for consecutive occurrences.
- **p**: Default 0.5, probability for same strand orientation in binomial tests.
- **BED file inputs**: Required for specifying genomic features and motifs.

## Commands / Code Snippets
```python
python contained_asymmetries.py gencode.v33.annotation.bed LINES.bed
python orientation.py Bg02es.Rep1strand.bed LINES.bed
python contained_asymmetries.py Bg02es.Rep1strand.bed LINES.bed gnomad.v2.1.sv.sites.LINES.bed --expected.asym = 0.524
```

## Notes for R-analysis agent
- The method is implemented in Python using `pybedtools`; consider using R packages like `GenomicRanges` for similar operations.
- Ensure BED files are correctly formatted and contain necessary strand information.
- Validate the number of simulations (N) and adjust if computational resources are limited.
- Double-check the orientation assignment of motifs before analysis to ensure accurate results.
- Consider using `ggplot2` for visualization of strand asymmetry results in R.
```
