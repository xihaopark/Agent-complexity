configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prep_files_for_differential_srna_clusters"


rule all:
  input:
    "results/finish/prep_files_for_differential_srna_clusters.done"


rule run_prep_files_for_differential_srna_clusters:
  output:
    "results/finish/prep_files_for_differential_srna_clusters.done"
  run:
    run_step(STEP_ID, output[0])
