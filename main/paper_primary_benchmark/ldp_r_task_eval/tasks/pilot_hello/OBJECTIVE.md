# Pilot: sum small integers

You are in a self-contained workspace (no Snakemake).

1. Read `input/numbers.txt` (one integer per line).
2. Use **R** (`run_rscript`) or **shell** to compute the sum of those integers.
3. Write the decimal sum as a single line of text to **`output/result.txt`** (create `output/` if needed).
4. Call **`submit_done(success=true)`** only after `output/result.txt` exists.

The expected sum for the bundled file is **6** (1+2+3).
