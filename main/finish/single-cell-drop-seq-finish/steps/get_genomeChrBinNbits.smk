configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_genomeChrBinNbits"


rule all:
  input:
    "results/finish/get_genomeChrBinNbits.done"


rule run_get_genomeChrBinNbits:
  output:
    "results/finish/get_genomeChrBinNbits.done"
  run:
    run_step(STEP_ID, output[0])
