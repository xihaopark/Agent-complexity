configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "md5sum"


rule all:
  input:
    "results/finish/md5sum.done"


rule run_md5sum:
  output:
    "results/finish/md5sum.done"
  run:
    run_step(STEP_ID, output[0])
