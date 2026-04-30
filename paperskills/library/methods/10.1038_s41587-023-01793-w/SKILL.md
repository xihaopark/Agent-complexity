---
name: paper-10-1038-s41587-023-01793-w
description: >-
  Vision-adapter skill extracted from 10.1038_s41587-023-01793-w.pdf via openai/gpt-4o
source_pdf: 10.1038_s41587-023-01793-w.pdf
pages_processed: 8
generator: paper2skills_ab_test/vision_adapter.py
---

```markdown
## Method
The Minigraph-Cactus pipeline constructs pangenome graphs by combining Minigraph's fast assembly-to-graph mapping with Cactus's base alignment. The process begins with the construction of an SV-only graph using Minigraph, which includes variants affecting sequences of 50bp or more. Minigraph uses a minimizer-based seeding and chaining strategy for base-level alignment, which is efficient for similar input genomes. The pipeline then employs Cactus to refine these alignments, creating a base-resolution graph. Cactus aligns sequences by "pinching" matching bases together, forming a sequence graph that is transformed into a Cactus graph. This method allows for the representation of genetic variation consistently across multiple genomes, improving mapping and variant detection.

## Parameters
- **SV size threshold**: 50bp (default) - Minimum size of structural variants included in the graph.
- **Sequence filter threshold**: 10kb - Threshold for clipping out stretches of sequences not aligning to the Minigraph.

## Commands / Code Snippets
(No code snippets visible on provided pages.)

## Notes for R-analysis agent
- The method is implemented in the Cactus software suite, utilizing Toil for distributed computation.
- Ensure input genome assemblies are in FASTA format.
- The pipeline outputs graphs in GFA and VCF formats, with indexes for vg giraffe.
- Check for compatibility with the `vg` toolkit for mapping and variant calling.
- Be aware of potential issues with highly repetitive sequences, which may require additional filtering.
```
