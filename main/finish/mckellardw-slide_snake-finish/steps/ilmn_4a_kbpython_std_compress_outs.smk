configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_4a_kbpython_std_compress_outs"


rule all:
  input:
    "results/finish/ilmn_4a_kbpython_std_compress_outs.done"


rule run_ilmn_4a_kbpython_std_compress_outs:
  output:
    "results/finish/ilmn_4a_kbpython_std_compress_outs.done"
  run:
    run_step(STEP_ID, output[0])
