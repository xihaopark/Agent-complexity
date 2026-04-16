configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "pathenrich"


rule all:
  input:
    "results/finish/pathenrich.done"


rule run_pathenrich:
  output:
    "results/finish/pathenrich.done"
  run:
    run_step(STEP_ID, output[0])
