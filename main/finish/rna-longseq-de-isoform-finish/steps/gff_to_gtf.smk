configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gff_to_gtf"


rule all:
  input:
    "results/finish/gff_to_gtf.done"


rule run_gff_to_gtf:
  output:
    "results/finish/gff_to_gtf.done"
  run:
    run_step(STEP_ID, output[0])
