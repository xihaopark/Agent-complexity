configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_4a_kbpython_std_remove_suffix"


rule all:
  input:
    "results/finish/ilmn_4a_kbpython_std_remove_suffix.done"


rule run_ilmn_4a_kbpython_std_remove_suffix:
  output:
    "results/finish/ilmn_4a_kbpython_std_remove_suffix.done"
  run:
    run_step(STEP_ID, output[0])
