configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "generate_sdf"


rule all:
  input:
    "results/finish/generate_sdf.done"


rule run_generate_sdf:
  output:
    "results/finish/generate_sdf.done"
  run:
    run_step(STEP_ID, output[0])
