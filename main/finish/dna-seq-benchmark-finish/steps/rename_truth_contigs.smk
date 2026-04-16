configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "rename_truth_contigs"


rule all:
  input:
    "results/finish/rename_truth_contigs.done"


rule run_rename_truth_contigs:
  output:
    "results/finish/rename_truth_contigs.done"
  run:
    run_step(STEP_ID, output[0])
