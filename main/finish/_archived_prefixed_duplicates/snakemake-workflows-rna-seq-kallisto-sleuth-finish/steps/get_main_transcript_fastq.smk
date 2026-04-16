configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_main_transcript_fastq"


rule all:
  input:
    "results/finish/get_main_transcript_fastq.done"


rule run_get_main_transcript_fastq:
  output:
    "results/finish/get_main_transcript_fastq.done"
  run:
    run_step(STEP_ID, output[0])
