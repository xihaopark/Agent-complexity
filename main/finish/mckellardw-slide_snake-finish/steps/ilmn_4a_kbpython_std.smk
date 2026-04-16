configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_4a_kbpython_std"


rule all:
  input:
    "results/finish/ilmn_4a_kbpython_std.done"


rule run_ilmn_4a_kbpython_std:
  output:
    "results/finish/ilmn_4a_kbpython_std.done"
  run:
    run_step(STEP_ID, output[0])
