configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "dispatch_srna_fastq"


rule all:
  input:
    "results/finish/dispatch_srna_fastq.done"


rule run_dispatch_srna_fastq:
  output:
    "results/finish/dispatch_srna_fastq.done"
  run:
    run_step(STEP_ID, output[0])
