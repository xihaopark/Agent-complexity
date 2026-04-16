configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "postprocess_diffexp"


rule all:
  input:
    "results/finish/postprocess_diffexp.done"


rule run_postprocess_diffexp:
  output:
    "results/finish/postprocess_diffexp.done"
  run:
    run_step(STEP_ID, output[0])
