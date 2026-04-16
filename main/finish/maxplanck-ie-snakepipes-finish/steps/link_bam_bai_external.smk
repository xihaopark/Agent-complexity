configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "link_bam_bai_external"


rule all:
  input:
    "results/finish/link_bam_bai_external.done"


rule run_link_bam_bai_external:
  output:
    "results/finish/link_bam_bai_external.done"
  run:
    run_step(STEP_ID, output[0])
