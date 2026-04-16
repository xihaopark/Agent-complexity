configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3u_sort_index_tagged_bam"


rule all:
  input:
    "results/finish/ilmn_3u_sort_index_tagged_bam.done"


rule run_ilmn_3u_sort_index_tagged_bam:
  output:
    "results/finish/ilmn_3u_sort_index_tagged_bam.done"
  run:
    run_step(STEP_ID, output[0])
