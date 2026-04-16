configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "find_motifs_in_file"


rule all:
  input:
    "results/finish/find_motifs_in_file.done"


rule run_find_motifs_in_file:
  output:
    "results/finish/find_motifs_in_file.done"
  run:
    run_step(STEP_ID, output[0])
