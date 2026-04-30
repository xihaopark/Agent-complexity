---
name: paper-10-1038-s41467-024-48981-z
description: >-
  Vision-adapter skill extracted from 10.1038_s41467-024-48981-z.pdf via openai/gpt-4o
source_pdf: 10.1038_s41467-024-48981-z.pdf
pages_processed: 8
generator: paper2skills_ab_test/vision_adapter.py
---

```markdown
## Method
Sopa is a computational framework designed to enhance the accessibility, efficiency, and interpretability of image-based spatial omics data. It operates across various spatial omics technologies, transforming input data into a unified format called a SpatialData object. The pipeline involves several key steps: segmentation, annotation, and spatial statistics. Segmentation is performed using models like Cellpose and Baysor, which handle both transcript-based and staining-based data. The framework supports interactive region of interest (ROI) selection and resolves conflicts in overlapping patches by merging or keeping distinct cell boundaries based on intersection-over-min-area (IOMA) metrics. Sopa also includes geometric and spatial analysis capabilities, allowing for comprehensive data visualization and integration with community tools.

## Parameters
- **Segmentation Model**: Choice between Cellpose, Baysor, or custom models.
- **IOMA Threshold**: Determines conflict resolution in overlapping patches.
- **Channel Averaging Method**: Options for transcript or staining intensity aggregation.

## Commands / Code Snippets
(No code snippets visible on provided pages.)

## Notes for R-analysis agent
- Sopa is implemented as a Python package; integration with R may require reticulate or similar interfaces.
- Ensure compatibility with input data formats (e.g., SpatialData objects).
- Verify segmentation model selection and parameter settings (e.g., IOMA threshold) for accurate conflict resolution.
- Check for dependencies on external tools like Cellpose or Baysor for segmentation tasks.
```
