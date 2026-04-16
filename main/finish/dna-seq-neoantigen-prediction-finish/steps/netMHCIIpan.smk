configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "netMHCIIpan"


rule all:
  input:
    "results/finish/netMHCIIpan.done"


rule run_netMHCIIpan:
  output:
    "results/finish/netMHCIIpan.done"
  run:
    run_step(STEP_ID, output[0])
