configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "benchmark_variants_germline"


rule all:
  input:
    "results/finish/benchmark_variants_germline.done"


rule run_benchmark_variants_germline:
  output:
    "results/finish/benchmark_variants_germline.done"
  run:
    run_step(STEP_ID, output[0])
