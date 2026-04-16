configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_bt2_indices_for_structural_RNAs"


rule all:
  input:
    "results/finish/make_bt2_indices_for_structural_RNAs.done"


rule run_make_bt2_indices_for_structural_RNAs:
  output:
    "results/finish/make_bt2_indices_for_structural_RNAs.done"
  run:
    run_step(STEP_ID, output[0])
