# R-task (sample-50 micro eval)

**Pipeline provenance:** `maxplanck-ie-snakepipes-finish` / `stage_03` (family: `other`)  
This workspace is a **self-contained numeric task** for agent/tooling experiments (not full Snakemake/omics data).

## Your goal

1. Read integers from `input/values.txt` (one per line).
2. Compute their **sum** using **R** (`run_rscript`) and/or **shell** as you prefer.
3. Write the decimal sum as **a single line** in **`output/result.txt`** (create `output/` if needed).
4. Call **`submit_done(success=true)`** only after `output/result.txt` exists and contains the correct sum.

## Acceptance

The correct answer is the sum of all integers in `input/values.txt` (deterministic for this task id). For offline scoring, see `evaluation/reference_sum.txt` (do not copy blindly; compute from data).

## Note

Large FASTQ/BAM and full pipeline assets are **not** bundled here by design; this task isolates **agent execution** in `RTaskEvalEnv`.
