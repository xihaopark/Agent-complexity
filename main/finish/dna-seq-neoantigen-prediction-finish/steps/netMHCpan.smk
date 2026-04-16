configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "netMHCpan"


rule all:
  input:
    "results/finish/netMHCpan.done"


rule run_netMHCpan:
  output:
    "results/finish/netMHCpan.done"
  run:
    run_step(STEP_ID, output[0])
