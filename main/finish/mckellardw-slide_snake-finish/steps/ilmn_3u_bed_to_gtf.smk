configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3u_bed_to_gtf"


rule all:
  input:
    "results/finish/ilmn_3u_bed_to_gtf.done"


rule run_ilmn_3u_bed_to_gtf:
  output:
    "results/finish/ilmn_3u_bed_to_gtf.done"
  run:
    run_step(STEP_ID, output[0])
