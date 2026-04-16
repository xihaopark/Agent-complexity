configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_only_main_transcript_reads_closest_to_3_prime"


rule all:
  input:
    "results/finish/get_only_main_transcript_reads_closest_to_3_prime.done"


rule run_get_only_main_transcript_reads_closest_to_3_prime:
  output:
    "results/finish/get_only_main_transcript_reads_closest_to_3_prime.done"
  run:
    run_step(STEP_ID, output[0])
