configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "modkit_pileup_dmc"


rule all:
  input:
    "results/finish/modkit_pileup_dmc.done"


rule run_modkit_pileup_dmc:
  output:
    "results/finish/modkit_pileup_dmc.done"
  run:
    run_step(STEP_ID, output[0])
