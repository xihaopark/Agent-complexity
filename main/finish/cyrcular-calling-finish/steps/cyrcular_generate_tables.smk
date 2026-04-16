configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cyrcular_generate_tables"


rule all:
  input:
    "results/finish/cyrcular_generate_tables.done"


rule run_cyrcular_generate_tables:
  output:
    "results/finish/cyrcular_generate_tables.done"
  run:
    run_step(STEP_ID, output[0])
