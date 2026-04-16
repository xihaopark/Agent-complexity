configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prepare_modbam_for_pileup"


rule all:
  input:
    "results/finish/prepare_modbam_for_pileup.done"


rule run_prepare_modbam_for_pileup:
  output:
    "results/finish/prepare_modbam_for_pileup.done"
  run:
    run_step(STEP_ID, output[0])
