configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "rseqc_gtf2bed"


rule all:
  input:
    "results/finish/rseqc_gtf2bed.done"


rule run_rseqc_gtf2bed:
  output:
    "results/finish/rseqc_gtf2bed.done"
  run:
    run_step(STEP_ID, output[0])
