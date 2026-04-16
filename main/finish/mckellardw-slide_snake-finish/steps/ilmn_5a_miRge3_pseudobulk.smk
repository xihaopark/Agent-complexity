configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_5a_miRge3_pseudobulk"


rule all:
  input:
    "results/finish/ilmn_5a_miRge3_pseudobulk.done"


rule run_ilmn_5a_miRge3_pseudobulk:
  output:
    "results/finish/ilmn_5a_miRge3_pseudobulk.done"
  run:
    run_step(STEP_ID, output[0])
