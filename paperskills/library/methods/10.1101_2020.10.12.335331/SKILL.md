---
name: paper-10-1101-2020-10-12-335331
description: >-
  Vision-adapter skill extracted from 10.1101_2020.10.12.335331.pdf via openai/gpt-4o
source_pdf: 10.1101_2020.10.12.335331.pdf
pages_processed: 8
generator: paper2skills_ab_test/vision_adapter.py
---

```markdown
## Method
The paper introduces a "weighted-nearest neighbor" (WNN) analysis for integrating multimodal single-cell data. This unsupervised framework assigns weights to different data types measured within each cell, reflecting their relative utility in defining cellular states. The method involves calculating modality weights using a softmax transformation, ensuring they are non-negative and sum to one for each cell. The WNN graph is constructed by calculating a new set of k-nearest cells based on a metric that averages normalized RNA and protein similarities. This approach enhances the ability to resolve cellular states and supports downstream analyses like clustering and trajectory inference.

## Parameters
- **k**: Default set to 20. Number of nearest neighbors considered for each modality.
- **Modality weights**: Calculated using a softmax transformation, unique to each cell.

## Commands / Code Snippets
(No code snippets visible on provided pages.)

## Notes for R-analysis agent
- The method is implemented in the Seurat package, version 4.
- Ensure input data includes multiple modalities (e.g., RNA and protein measurements).
- Verify the calculation of modality weights using softmax transformation.
- Check compatibility with UMAP visualization and clustering functions in Seurat.
- Confirm robustness to changes in parameter k and data quality differences across modalities.
```
