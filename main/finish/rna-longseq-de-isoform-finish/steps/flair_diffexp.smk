configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "flair_diffexp"


rule all:
  input:
    "results/finish/flair_diffexp.done"


rule run_flair_diffexp:
  output:
    "results/finish/flair_diffexp.done"
  run:
    run_step(STEP_ID, output[0])
