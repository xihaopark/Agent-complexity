configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "pe_or_se_chip_dispatch"


rule all:
  input:
    "results/finish/pe_or_se_chip_dispatch.done"


rule run_pe_or_se_chip_dispatch:
  output:
    "results/finish/pe_or_se_chip_dispatch.done"
  run:
    run_step(STEP_ID, output[0])
