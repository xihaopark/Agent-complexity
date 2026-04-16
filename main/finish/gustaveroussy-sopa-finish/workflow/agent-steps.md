# gustaveroussy-sopa-finish LLM Execution Spec

## Purpose

- Source repository: `gustaveroussy__sopa`
- Source snakefile: `../workflow_candidates/gustaveroussy__sopa/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `to_spatialdata`
2. `tissue_segmentation`
3. `patchify_image`
4. `patchify_transcripts`
5. `aggregate`
6. `annotate`
7. `scanpy_preprocess`
8. `explorer_raw`
9. `explorer`
10. `report`
11. `patch_segmentation_cellpose`
12. `resolve_cellpose`
13. `patch_segmentation_comseg`
14. `resolve_comseg`
15. `patch_segmentation_baysor`
16. `resolve_baysor`
17. `patch_segmentation_proseg`
18. `patch_segmentation_stardist`
19. `resolve_stardist`
20. `all`
