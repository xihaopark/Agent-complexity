---
name: paper-10-1186-s12859-019-2926-y
description: >-
  Vision-adapter skill extracted from 10.1186_s12859-019-2926-y.pdf via openai/gpt-4o
source_pdf: 10.1186_s12859-019-2926-y.pdf
pages_processed: 8
generator: paper2skills_ab_test/vision_adapter.py
---

```markdown
## Method
AutoCryoPicker is an unsupervised learning framework designed for automated particle picking in cryo-EM images. The method comprises three main stages: preprocessing, clustering, and particle picking. 

1. **Preprocessing**: This stage involves converting cryo-EM images from MRC format to PNG using EMAN2, followed by several image enhancement techniques. These include global and local contrast enhancement, intensity adjustment, and particle edge enhancement. The goal is to improve image quality and contrast, making particles more distinguishable from the background.

2. **Clustering**: The enhanced images undergo intensity-based clustering (IBC) to identify potential particle candidates. This method is more accurate than traditional k-means and Fuzzy C-means (FCM) clustering, as it uses an intensity distribution model to better handle the noise and variability in cryo-EM images.

3. **Particle Picking**: A modified Circular Hough Transform (CHT) algorithm is used to detect and encapsulate particles within bounding boxes. This stage involves generating and cleaning binary masks, followed by measuring particle properties to finalize detection.

## Parameters
- **Image Resolution**: Affects preprocessing steps like intensity adjustment.
- **Clustering Method**: Intensity-based clustering (IBC) is used, but parameters for clustering are not specified.
- **Contrast Enhancement**: Parameters for global and local contrast adjustments are applied but not detailed.
- **Edge Enhancement**: Uses guided image filtering, but specific parameters are not mentioned.

## Commands / Code Snippets
(No code snippets visible on provided pages.)

## Notes for R-analysis agent
- Consider using image processing libraries in R, such as `EBImage`, for preprocessing steps.
- Clustering can be implemented using `stats::kmeans` or `cluster::fanny` for Fuzzy C-means, but note that IBC is a custom method.
- The Circular Hough Transform might be implemented using packages like `OpenImageR`.
- Ensure input images are converted to a suitable format (e.g., PNG) before processing.
- Verify the intensity normalization and contrast enhancement steps are correctly applied to match the preprocessing described.
```
