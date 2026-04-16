
rule store_config:
    output:
        report(
            RESULTS_DIR / "report" / "run-config.yaml", caption="../report/config.rst"
        ),
    log:
        "logs/store_config.log",
    run:
        with open(output[0], "w") as f:
            yaml.dump(config, f, default_flow_style=False)
