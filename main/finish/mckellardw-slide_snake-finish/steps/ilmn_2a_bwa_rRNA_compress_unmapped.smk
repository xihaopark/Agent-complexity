configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_2a_bwa_rRNA_compress_unmapped"


rule all:
  input:
    "results/finish/ilmn_2a_bwa_rRNA_compress_unmapped.done"


rule run_ilmn_2a_bwa_rRNA_compress_unmapped:
  output:
    "results/finish/ilmn_2a_bwa_rRNA_compress_unmapped.done"
  run:
    run_step(STEP_ID, output[0])
