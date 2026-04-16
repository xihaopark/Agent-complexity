configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bedtools_complement_blacklist"


rule all:
  input:
    "results/finish/bedtools_complement_blacklist.done"


rule run_bedtools_complement_blacklist:
  output:
    "results/finish/bedtools_complement_blacklist.done"
  run:
    run_step(STEP_ID, output[0])
