configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "scatter_candidates"


rule all:
  input:
    "results/finish/scatter_candidates.done"


rule run_scatter_candidates:
  output:
    "results/finish/scatter_candidates.done"
  run:
    run_step(STEP_ID, output[0])
