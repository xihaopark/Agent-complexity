configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1a_compress_merged_fq"


rule all:
  input:
    "results/finish/ont_1a_compress_merged_fq.done"


rule run_ont_1a_compress_merged_fq:
  output:
    "results/finish/ont_1a_compress_merged_fq.done"
  run:
    run_step(STEP_ID, output[0])
