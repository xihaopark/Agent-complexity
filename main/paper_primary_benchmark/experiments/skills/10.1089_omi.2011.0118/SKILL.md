---
name: paper-10-1089-omi-2011-0118
description: >-
  Vision-adapter skill extracted from 10.1089_omi.2011.0118.pdf via openai/gpt-4o
source_pdf: 10.1089_omi.2011.0118.pdf
pages_processed: 4
generator: paper2skills_ab_test/vision_adapter.py
---

```markdown
## Method
The `clusterProfiler` package is designed for comparing biological themes among gene clusters. It implements a gene classification method using the functions `groupGO`, `enrichGO`, and `enrichKEGG` to classify genes based on their projection at a specific level of the Gene Ontology (GO) corpus. The package calculates enrichment tests for GO terms and KEGG pathways using a hypergeometric distribution. To control for false discovery rates, the package applies the Benjamini-Hochberg method for multiple testing corrections. Additionally, `clusterProfiler` provides a function, `compareCluster`, to automatically calculate enriched functional categories for each gene cluster and visualize the results.

## Parameters
- `pvalueCutoff`: Default not specified; threshold for p-value significance.
- `qvalueCutoff`: Default not specified; threshold for q-value significance.
- `ontology`: Specifies the ontology to use (e.g., "BP" for Biological Process).
- `organism`: Specifies the organism database to use (e.g., "hsa" for Homo sapiens).

## Commands / Code Snippets
(No code snippets visible on provided pages.)

## Notes for R-analysis agent
- The `clusterProfiler` package is available on Bioconductor and should be installed from there.
- Ensure the input data is formatted correctly with gene identifiers compatible with the selected organism database.
- Double-check the p-value and q-value cutoffs to ensure they align with the study's significance thresholds.
- Visualization functions are available and should be used to interpret the results effectively.
```
