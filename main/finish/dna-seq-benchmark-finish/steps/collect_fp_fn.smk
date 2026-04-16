configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "collect_fp_fn"


rule all:
  input:
    "results/finish/collect_fp_fn.done"


rule run_collect_fp_fn:
  output:
    "results/finish/collect_fp_fn.done"
  run:
    run_step(STEP_ID, output[0])
