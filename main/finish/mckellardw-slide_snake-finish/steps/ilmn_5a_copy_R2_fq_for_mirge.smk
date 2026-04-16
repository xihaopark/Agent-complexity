configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_5a_copy_R2_fq_for_mirge"


rule all:
  input:
    "results/finish/ilmn_5a_copy_R2_fq_for_mirge.done"


rule run_ilmn_5a_copy_R2_fq_for_mirge:
  output:
    "results/finish/ilmn_5a_copy_R2_fq_for_mirge.done"
  run:
    run_step(STEP_ID, output[0])
