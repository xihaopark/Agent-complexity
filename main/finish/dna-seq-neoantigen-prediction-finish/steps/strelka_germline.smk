configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "strelka_germline"


rule all:
  input:
    "results/finish/strelka_germline.done"


rule run_strelka_germline:
  output:
    "results/finish/strelka_germline.done"
  run:
    run_step(STEP_ID, output[0])
