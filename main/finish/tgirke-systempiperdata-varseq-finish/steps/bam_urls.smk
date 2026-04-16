configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bam_urls"


rule all:
  input:
    "results/finish/bam_urls.done"


rule run_bam_urls:
  output:
    "results/finish/bam_urls.done"
  run:
    run_step(STEP_ID, output[0])
