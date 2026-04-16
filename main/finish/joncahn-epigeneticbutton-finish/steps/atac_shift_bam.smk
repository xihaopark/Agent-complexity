configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "atac_shift_bam"


rule all:
  input:
    "results/finish/atac_shift_bam.done"


rule run_atac_shift_bam:
  output:
    "results/finish/atac_shift_bam.done"
  run:
    run_step(STEP_ID, output[0])
