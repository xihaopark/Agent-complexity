configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_2b_ribodetector_get_no_rRNA_list"


rule all:
  input:
    "results/finish/ilmn_2b_ribodetector_get_no_rRNA_list.done"


rule run_ilmn_2b_ribodetector_get_no_rRNA_list:
  output:
    "results/finish/ilmn_2b_ribodetector_get_no_rRNA_list.done"
  run:
    run_step(STEP_ID, output[0])
