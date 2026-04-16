configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "mask_reference_fasta"


rule all:
  input:
    "results/finish/mask_reference_fasta.done"


rule run_mask_reference_fasta:
  output:
    "results/finish/mask_reference_fasta.done"
  run:
    run_step(STEP_ID, output[0])
