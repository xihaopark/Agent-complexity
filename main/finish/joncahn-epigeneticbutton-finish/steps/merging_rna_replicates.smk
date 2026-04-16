configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merging_rna_replicates"


rule all:
  input:
    "results/finish/merging_rna_replicates.done"


rule run_merging_rna_replicates:
  output:
    "results/finish/merging_rna_replicates.done"
  run:
    run_step(STEP_ID, output[0])
