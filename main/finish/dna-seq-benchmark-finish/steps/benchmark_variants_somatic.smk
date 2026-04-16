configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "benchmark_variants_somatic"


rule all:
  input:
    "results/finish/benchmark_variants_somatic.done"


rule run_benchmark_variants_somatic:
  output:
    "results/finish/benchmark_variants_somatic.done"
  run:
    run_step(STEP_ID, output[0])
