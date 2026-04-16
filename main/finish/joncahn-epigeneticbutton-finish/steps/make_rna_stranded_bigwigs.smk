configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_rna_stranded_bigwigs"


rule all:
  input:
    "results/finish/make_rna_stranded_bigwigs.done"


rule run_make_rna_stranded_bigwigs:
  output:
    "results/finish/make_rna_stranded_bigwigs.done"
  run:
    run_step(STEP_ID, output[0])
