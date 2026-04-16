configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "diff_loading"


rule all:
  input:
    "results/finish/diff_loading.done"


rule run_diff_loading:
  output:
    "results/finish/diff_loading.done"
  run:
    run_step(STEP_ID, output[0])
