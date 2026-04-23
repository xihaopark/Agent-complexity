# Evaluation V2 · batch `sweep_v2_pipeline_20260416T173242Z`

evaluator_version: `v2` · ts: `2026-04-16T18:46:29Z` · n_tasks: 6 · rtol=0.001 atol=1e-05

**Mean overall score:** 0.562

**Verdict counts (V2):** pass=3, partial_pass=0, partial_fail=0, fail=3, error=0

**Verdict counts (legacy V1):** pass=3, partial=0, fail=3

| task | verdict | verdict (V1) | overall | process_mean | files_mean | n_expected | strategies |
|------|---------|--------------|---------|--------------|------------|------------|------------|
| `akinyi_deseq2` | **pass** | pass | 1.000 | 1.00 | 1.000 | 2 | byte_identical |
| `star_deseq2_init` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | byte_identical |
| `star_deseq2_contrast` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | byte_identical |
| `methylkit_load` | **fail** | fail | 0.075 | 0.25 | 0.000 | 1 | missing |
| `methylkit_unite` | **fail** | fail | 0.075 | 0.25 | 0.000 | 1 | missing |
| `methylkit_to_tibble` | **fail** | fail | 0.225 | 0.75 | 0.000 | 1 | missing |

## Per-file detail

### `akinyi_deseq2`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `deseq2_up.txt` | byte_identical | 1.000 | True | 2481 | 2481 |
| `deseq2_down.txt` | byte_identical | 1.000 | True | 1524 | 1524 |

### `star_deseq2_init`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `normalized_counts.tsv` | byte_identical | 1.000 | True | 58217 | 58217 |

### `star_deseq2_contrast`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `contrast_results.tsv` | byte_identical | 1.000 | True | 53764 | 53764 |

### `methylkit_load`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `mk_raw.rds` | missing | 0.000 | False | None | 3529 |

### `methylkit_unite`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `unite_stats.tsv` | missing | 0.000 | False | None | 83 |

### `methylkit_to_tibble`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `mean_mcpg.tsv` | missing | 0.000 | False | None | 406 |
