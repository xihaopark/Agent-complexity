configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3u_gzip_counts"


rule all:
  input:
    "results/finish/ilmn_3u_gzip_counts.done"


rule run_ilmn_3u_gzip_counts:
  output:
    "results/finish/ilmn_3u_gzip_counts.done"
  run:
    run_step(STEP_ID, output[0])
