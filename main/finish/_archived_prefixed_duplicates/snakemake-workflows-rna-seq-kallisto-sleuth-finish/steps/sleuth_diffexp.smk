configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sleuth_diffexp"


rule all:
  input:
    "results/finish/sleuth_diffexp.done"


rule run_sleuth_diffexp:
  output:
    "results/finish/sleuth_diffexp.done"
  run:
    run_step(STEP_ID, output[0])
