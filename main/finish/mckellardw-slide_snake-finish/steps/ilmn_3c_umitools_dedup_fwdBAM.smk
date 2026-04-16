configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3c_umitools_dedup_fwdBAM"


rule all:
  input:
    "results/finish/ilmn_3c_umitools_dedup_fwdBAM.done"


rule run_ilmn_3c_umitools_dedup_fwdBAM:
  output:
    "results/finish/ilmn_3c_umitools_dedup_fwdBAM.done"
  run:
    run_step(STEP_ID, output[0])
