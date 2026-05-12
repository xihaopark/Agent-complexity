# Evaluation summary for batch `sweep_v2_pipeline_20260416T173242Z`

**Tasks:** 6 | pass: 3 | partial: 0 | fail: 3 | pass_rate: 50.0%

| task | verdict | byte-identical | table-full-match | expected | exists |
|------|---------|----------------|------------------|----------|--------|
| `akinyi_deseq2` | **pass** | 2 | 0 | 2 | 2 |
| `star_deseq2_init` | **pass** | 1 | 1 | 1 | 1 |
| `star_deseq2_contrast` | **pass** | 1 | 1 | 1 | 1 |
| `methylkit_load` | **fail** | 0 | 0 | 1 | 0 |
| `methylkit_unite` | **fail** | 0 | 0 | 1 | 0 |
| `methylkit_to_tibble` | **fail** | 0 | 0 | 1 | 0 |
