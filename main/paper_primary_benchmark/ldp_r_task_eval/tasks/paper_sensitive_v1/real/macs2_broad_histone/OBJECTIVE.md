# Paper-sensitive R-task: macs2_broad_histone

**Design intent:** for **broad** histone marks, narrow peak calling **over-fragments** peaks. The MACS paper and manual discuss **broad** peak mode vs default narrow peak mode.

> This task uses a **pre-computed** narrowPeak / bedGraph-style input in `input/` to keep the run lightweight; the agent is expected to run **macs2** in **broad** mode or otherwise produce **broad region calls** that match the scoring spec.

**Conceptual source:** `epigen-atacseq_pipeline-finish` / ChIP-like peak calling.

## Your goal

You are given a small BED6 file of ChIP fragments / pileup (`input/fragments.bed`) and a control (`input/control.bed`) — see `input/README.md` for the exact format.

Call peaks using **MACS2** in a configuration appropriate for **broad histone** enrichment:

- The deliverable is **`output/broad_peaks.bed`**, BED3 or BED6, sorted, **non-overlapping merged broad regions** as you choose, but the file must be valid BED and non-empty.
- In your `submit_done` message, you **must** state the exact `macs2` subcommand and key flags (e.g. broad mode, q-value, ext size if used).

If `macs2` is not installed in the environment, document the failure in stderr and still produce a best-effort BED; the benchmark expects the reference environment to have MACS2 available.

## Deliverables

- `output/broad_peaks.bed`

Then `submit_done(success=true)`.
