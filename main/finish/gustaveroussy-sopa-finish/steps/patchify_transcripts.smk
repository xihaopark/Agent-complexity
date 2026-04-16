configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "patchify_transcripts"


rule all:
  input:
    "results/finish/patchify_transcripts.done"


rule run_patchify_transcripts:
  output:
    "results/finish/patchify_transcripts.done"
  run:
    run_step(STEP_ID, output[0])
