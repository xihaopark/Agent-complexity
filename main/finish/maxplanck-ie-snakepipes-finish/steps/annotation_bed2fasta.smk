configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotation_bed2fasta"


rule all:
  input:
    "results/finish/annotation_bed2fasta.done"


rule run_annotation_bed2fasta:
  output:
    "results/finish/annotation_bed2fasta.done"
  run:
    run_step(STEP_ID, output[0])
