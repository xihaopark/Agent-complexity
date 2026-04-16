configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "collect_fp_fn_benchmark"


rule all:
  input:
    "results/finish/collect_fp_fn_benchmark.done"


rule run_collect_fp_fn_benchmark:
  output:
    "results/finish/collect_fp_fn_benchmark.done"
  run:
    run_step(STEP_ID, output[0])
