configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3c_merge_dedup_bam"


rule all:
  input:
    "results/finish/ilmn_3c_merge_dedup_bam.done"


rule run_ilmn_3c_merge_dedup_bam:
  output:
    "results/finish/ilmn_3c_merge_dedup_bam.done"
  run:
    run_step(STEP_ID, output[0])
