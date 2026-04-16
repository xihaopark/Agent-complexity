configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3c_umitools_dedup_revBAM"


rule all:
  input:
    "results/finish/ilmn_3c_umitools_dedup_revBAM.done"


rule run_ilmn_3c_umitools_dedup_revBAM:
  output:
    "results/finish/ilmn_3c_umitools_dedup_revBAM.done"
  run:
    run_step(STEP_ID, output[0])
