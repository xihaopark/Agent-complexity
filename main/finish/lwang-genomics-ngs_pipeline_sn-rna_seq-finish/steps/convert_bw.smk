configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "convert_bw"


rule all:
  input:
    "results/finish/convert_bw.done"


rule run_convert_bw:
  output:
    "results/finish/convert_bw.done"
  run:
    run_step(STEP_ID, output[0])
