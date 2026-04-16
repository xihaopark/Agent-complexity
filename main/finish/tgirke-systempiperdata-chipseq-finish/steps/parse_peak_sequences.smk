configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "parse_peak_sequences"


rule all:
  input:
    "results/finish/parse_peak_sequences.done"


rule run_parse_peak_sequences:
  output:
    "results/finish/parse_peak_sequences.done"
  run:
    run_step(STEP_ID, output[0])
