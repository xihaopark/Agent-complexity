configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "split_bam_species"


rule all:
  input:
    "results/finish/split_bam_species.done"


rule run_split_bam_species:
  output:
    "results/finish/split_bam_species.done"
  run:
    run_step(STEP_ID, output[0])
