configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_2a_extract_rRNA_fasta"


rule all:
  input:
    "results/finish/ilmn_2a_extract_rRNA_fasta.done"


rule run_ilmn_2a_extract_rRNA_fasta:
  output:
    "results/finish/ilmn_2a_extract_rRNA_fasta.done"
  run:
    run_step(STEP_ID, output[0])
