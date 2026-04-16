def get_mem_mb_by_attempt(
    wildcards, attempt: int, threads: int, default_mem: int
) -> int:

    MAX_MEM = 128000

    print(
        f"Calculating memory for attempt {attempt} with {threads} threads with default memory {default_mem} MB"
    )
    mem_mb = attempt * int(default_mem)

    print(f"Calculated memory: {mem_mb} MB")

    if mem_mb * threads < MAX_MEM:
        return mem_mb
    else:
        print("Warning: calculated memory exceeds MAX_MEM")
        return MAX_MEM


def get_mem_mb(wildcards, default_mem):

    configured_fractions = list(map(float, config["SUBSAMPLING_FRACTIONS"]))

    frac = float(wildcards.subsampling_fraction)

    assert frac in configured_fractions

    min_frac = min(configured_fractions)  # get baseline

    return default_mem * (frac / min_frac)


def get_input_reads(wildcards, fieldname):
    sample = wildcards.sample
    return (
        samples[samples["samplename"] == sample][fieldname].astype("string").to_list()
    )


def generate_file_paths(config, base_dir, **kwargs):
    paths = []

    def parse_paths(base, subpaths):
        if isinstance(subpaths, list):
            for path in subpaths:
                paths.append(f"{base}/{path}")
        elif isinstance(subpaths, dict):
            for key, value in subpaths.items():
                parse_paths(f"{base}/{key}", value)

    for base, subpaths in config["target_files"].items():
        parse_paths(base, subpaths)

    # add base_dir to all paths
    paths = [f"{base_dir}/{path}" for path in paths]

    # raise warning if any of the keyword-arguments are None
    empty_keywords = []
    for key, value in kwargs.items():
        if value is None:
            print(f"Warning: {key} is None")
            empty_keywords.append(key)

    # apply expand function when {} occurrs in path
    paths = [
        expand(path, **kwargs)
        for path in paths
        if not any(keyword in path for keyword in empty_keywords)
    ]

    return paths
