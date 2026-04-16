configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "is_stranded"


rule all:
  input:
    "results/finish/is_stranded.done"


rule run_is_stranded:
  output:
    "results/finish/is_stranded.done"
  run:
    run_step(STEP_ID, output[0])
