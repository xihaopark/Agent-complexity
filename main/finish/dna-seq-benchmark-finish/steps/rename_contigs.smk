configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "rename_contigs"


rule all:
  input:
    "results/finish/rename_contigs.done"


rule run_rename_contigs:
  output:
    "results/finish/rename_contigs.done"
  run:
    run_step(STEP_ID, output[0])
