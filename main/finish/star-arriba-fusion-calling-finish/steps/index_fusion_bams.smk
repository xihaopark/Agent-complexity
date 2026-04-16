configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "index_fusion_bams"


rule all:
  input:
    "results/finish/index_fusion_bams.done"


rule run_index_fusion_bams:
  output:
    "results/finish/index_fusion_bams.done"
  run:
    run_step(STEP_ID, output[0])
