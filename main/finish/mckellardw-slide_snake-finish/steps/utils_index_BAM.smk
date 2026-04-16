configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "utils_index_BAM"


rule all:
  input:
    "results/finish/utils_index_BAM.done"


rule run_utils_index_BAM:
  output:
    "results/finish/utils_index_BAM.done"
  run:
    run_step(STEP_ID, output[0])
