configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_bismark_indices"


rule all:
  input:
    "results/finish/make_bismark_indices.done"


rule run_make_bismark_indices:
  output:
    "results/finish/make_bismark_indices.done"
  run:
    run_step(STEP_ID, output[0])
