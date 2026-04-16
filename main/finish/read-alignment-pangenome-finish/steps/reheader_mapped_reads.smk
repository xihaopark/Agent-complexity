configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "reheader_mapped_reads"


rule all:
  input:
    "results/finish/reheader_mapped_reads.done"


rule run_reheader_mapped_reads:
  output:
    "results/finish/reheader_mapped_reads.done"
  run:
    run_step(STEP_ID, output[0])
