configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_archive"


rule all:
  input:
    "results/finish/get_archive.done"


rule run_get_archive:
  output:
    "results/finish/get_archive.done"
  run:
    run_step(STEP_ID, output[0])
