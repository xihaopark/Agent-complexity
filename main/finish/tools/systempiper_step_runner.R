args <- commandArgs(trailingOnly = TRUE)

parse_args <- function(x) {
  out <- list()
  i <- 1
  while (i <= length(x)) {
    key <- x[[i]]
    if (!startsWith(key, "--")) {
      stop(paste("Unexpected argument:", key))
    }
    if (i == length(x)) {
      stop(paste("Missing value for", key))
    }
    out[[substring(key, 3)]] <- x[[i + 1]]
    i <- i + 2
  }
  out
}

opts <- parse_args(args)
required <- c("workflow-name", "workdir", "rmd-file", "step")
missing <- required[!required %in% names(opts)]
if (length(missing) > 0) {
  stop(paste("Missing required args:", paste(missing, collapse = ", ")))
}

workflow_name <- opts[["workflow-name"]]
workdir <- normalizePath(opts[["workdir"]], mustWork = FALSE)
rmd_file <- normalizePath(opts[["rmd-file"]], mustWork = FALSE)
step_name <- opts[["step"]]

if (!dir.exists(workdir)) {
  dir.create(workdir, recursive = TRUE, showWarnings = FALSE)
}

ensure_cran_package <- function(pkg) {
  if (requireNamespace(pkg, quietly = TRUE)) {
    return(invisible(TRUE))
  }
  install.packages(pkg, repos = "https://cloud.r-project.org", lib = libdir, quiet = TRUE)
  if (!requireNamespace(pkg, quietly = TRUE)) {
    stop(sprintf("Failed to install required CRAN package: %s", pkg))
  }
  invisible(TRUE)
}

ensure_bioc_package <- function(pkg) {
  if (requireNamespace(pkg, quietly = TRUE)) {
    return(invisible(TRUE))
  }
  ensure_cran_package("BiocManager")
  suppressMessages(
    BiocManager::install(
      pkg,
      ask = FALSE,
      update = FALSE,
      dependencies = TRUE,
      lib = libdir,
      quiet = TRUE
    )
  )
  if (!requireNamespace(pkg, quietly = TRUE)) {
    stop(sprintf("Failed to install required Bioconductor package: %s", pkg))
  }
  invisible(TRUE)
}

ensure_bioc_package("systemPipeR")
ensure_bioc_package("systemPipeRdata")

workflow_parent <- dirname(workdir)
workflow_dirname <- basename(workdir)
targets_candidates <- c(
  file.path(workdir, "targetsPE.txt"),
  file.path(workdir, "targets.txt")
)
has_workenv <- any(file.exists(targets_candidates))
if (!has_workenv) {
  if (!dir.exists(workflow_parent)) {
    dir.create(workflow_parent, recursive = TRUE, showWarnings = FALSE)
  }
  if (dir.exists(workdir)) {
    unlink(workdir, recursive = TRUE, force = TRUE)
  }
  oldwd <- getwd()
  on.exit(setwd(oldwd), add = TRUE)
  setwd(workflow_parent)
  suppressPackageStartupMessages(library(systemPipeRdata))
  systemPipeRdata::genWorkenvir(workflow = workflow_name, mydirname = workflow_dirname)
}

if (!dir.exists(workdir)) {
  dir.create(workdir, recursive = TRUE, showWarnings = FALSE)
}

setwd(workdir)

libdir <- file.path(workdir, "_r_libs")
if (!dir.exists(libdir)) {
  dir.create(libdir, recursive = TRUE, showWarnings = FALSE)
}
.libPaths(c(normalizePath(libdir, mustWork = FALSE), .libPaths()))

if (!file.exists(rmd_file)) {
  stop(paste("Rmd file not found:", rmd_file))
}

suppressPackageStartupMessages(library(systemPipeR))

project_dir <- file.path(workdir, ".SPRproject")
had_project <- dir.exists(project_dir)
project_args <- if (had_project) {
  list(resume = TRUE)
} else {
  list()
}
sal <- do.call(SPRproject, project_args)
if (!had_project) {
  sal <- importWF(
    sal,
    file_path = rmd_file,
    verbose = FALSE,
    check_tool = FALSE,
    check_module = FALSE
  )
}

runwf_fun <- get("runWF", envir = asNamespace("systemPipeR"))
param_names <- names(formals(runwf_fun))

attempts <- list(
  list(run_step = step_name),
  list(step_name = step_name),
  list(steps = step_name),
  list(step = step_name),
  list(until_step = step_name),
  list(to_step = step_name)
)

executed <- FALSE
last_error <- NULL
sal_run <- sal
for (trial in attempts) {
  usable <- trial[names(trial) %in% param_names]
  if (length(usable) == 0) {
    next
  }
  call_expr <- as.call(c(list(as.name("runWF"), quote(sal_run)), usable))
  result <- try(eval(call_expr), silent = TRUE)
  if (!inherits(result, "try-error")) {
    executed <- TRUE
    break
  }
  last_error <- result
}

if (!executed) {
  result <- try(runWF(sal_run), silent = TRUE)
  if (inherits(result, "try-error")) {
    stop(
      paste(
        "systemPipeR runWF invocation failed for workflow", workflow_name,
        "target step", step_name,
        "\nLast partial-run error:", as.character(last_error),
        "\nFallback error:", as.character(result)
      )
    )
  }
}

cat(sprintf("Completed systemPipeR workflow '%s' through step '%s'\n", workflow_name, step_name))
