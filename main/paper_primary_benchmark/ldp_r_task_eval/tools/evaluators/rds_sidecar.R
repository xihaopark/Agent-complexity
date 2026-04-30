#!/usr/bin/env Rscript
# Usage: rds_sidecar.R <input.rds> <output.tsv>
# Always exits 0, even on failure. Writes a one-line diagnostic to stderr.
#
# V2.1: broader S4 coverage (methylKit sub-slots, DESeq/SummarizedExperiment
# assay matrices, GRanges, limma/DGEList) so evaluator can see cell-level
# content rather than falling back to process_credit.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2L) { message("rds_sidecar: need <in.rds> <out.tsv>"); quit(status = 0) }
inp <- args[[1]]; outp <- args[[2]]

dump_df <- function(df, outp) {
  df <- as.data.frame(df, stringsAsFactors = FALSE)
  # Normalise numeric precision so tiny float drift doesn't spuriously diverge
  # between identical S4 objects serialised on different R builds.
  num_cols <- vapply(df, is.numeric, logical(1))
  for (j in which(num_cols)) df[[j]] <- signif(df[[j]], 8)
  utils::write.table(df, outp, sep = "\t", quote = FALSE,
                     row.names = FALSE, col.names = TRUE, na = "NA")
}
dump_txt <- function(txt, outp) {
  writeLines(as.character(txt), outp, useBytes = TRUE)
}

# Merge a list of per-sample data.frames into a single long-format frame with
# a leading `__item__` column so downstream tabular ladder compares cells.
merge_list_df <- function(lst, outp) {
  parts <- list()
  for (i in seq_along(lst)) {
    d <- tryCatch(as.data.frame(lst[[i]], stringsAsFactors = FALSE),
                  error = function(e) NULL)
    if (is.null(d) || nrow(d) == 0) next
    tag <- names(lst)[i]
    if (is.null(tag) || !nzchar(tag)) tag <- sprintf("[%d]", i)
    d <- cbind(`__item__` = tag, d)
    parts[[length(parts) + 1L]] <- d
  }
  if (length(parts) == 0) return(FALSE)
  cols <- unique(unlist(lapply(parts, names)))
  parts2 <- lapply(parts, function(d) {
    miss <- setdiff(cols, names(d)); for (m in miss) d[[m]] <- NA
    d[, cols, drop = FALSE]
  })
  dump_df(do.call(rbind, parts2), outp); TRUE
}

try_methylkit <- function(obj, outp) {
  if (!inherits(obj, c("methylRawList", "methylBase", "methylBaseDB",
                       "methylRaw", "methylRawDB", "methylDiff"))) return(NULL)
  if (!requireNamespace("methylKit", quietly = TRUE)) return(NULL)
  if (inherits(obj, c("methylRawList"))) {
    # Merge all samples so evaluator sees all cells.
    lst <- tryCatch(lapply(seq_along(obj), function(i) {
      d <- methylKit::getData(obj[[i]])
      d$sample_id <- tryCatch(obj[[i]]@sample.id, error = function(e) sprintf("s%d", i))
      d
    }), error = function(e) NULL)
    if (is.null(lst)) return(NULL)
    if (merge_list_df(lst, outp)) return("methylRawList")
    return(NULL)
  }
  d <- tryCatch(methylKit::getData(obj), error = function(e) NULL)
  if (!is.null(d)) { dump_df(d, outp); return("methylKit") }
  NULL
}

try_bioc <- function(obj, outp) {
  # DESeqResults / DESeqDataSet / SummarizedExperiment / DataFrame
  if (inherits(obj, c("DESeqResults", "DataFrame"))) {
    d <- tryCatch(as.data.frame(obj), error = function(e) NULL)
    if (!is.null(d)) { dump_df(d, outp); return("bioc_df") }
  }
  if (inherits(obj, c("DESeqDataSet", "SummarizedExperiment"))) {
    # Pull the primary assay and coerce to data.frame so cells are comparable.
    asy <- tryCatch(SummarizedExperiment::assay(obj), error = function(e) NULL)
    if (!is.null(asy)) {
      df <- as.data.frame(asy, stringsAsFactors = FALSE)
      df <- cbind(`__rowname__` = rownames(asy) %||% rownames(df), df)
      dump_df(df, outp); return("se_assay")
    }
  }
  if (inherits(obj, "GRanges")) {
    if (requireNamespace("GenomicRanges", quietly = TRUE)) {
      df <- tryCatch(as.data.frame(obj), error = function(e) NULL)
      if (!is.null(df)) { dump_df(df, outp); return("granges") }
    }
  }
  if (inherits(obj, "DGEList")) {
    # edgeR DGEList: dump counts matrix with rownames.
    m <- tryCatch(obj$counts, error = function(e) NULL)
    if (!is.null(m)) {
      df <- cbind(gene_id = rownames(m), as.data.frame(m, stringsAsFactors = FALSE))
      dump_df(df, outp); return("dgelist") }
  }
  NULL
}

`%||%` <- function(a, b) if (is.null(a) || length(a) == 0) b else a

try_dump <- function(obj, outp) {
  if (is.data.frame(obj) || inherits(obj, "tbl_df")) {
    dump_df(as.data.frame(obj, stringsAsFactors = FALSE), outp); return("data.frame")
  }
  k <- try_methylkit(obj, outp); if (!is.null(k)) return(k)
  k <- try_bioc(obj, outp);      if (!is.null(k)) return(k)
  if (is.matrix(obj)) {
    df <- as.data.frame(obj, stringsAsFactors = FALSE)
    if (!is.null(rownames(obj)) && any(nzchar(rownames(obj)))) {
      df <- cbind(`__rowname__` = rownames(obj), df)
    }
    dump_df(df, outp); return("matrix")
  }
  if (is.list(obj) && length(obj) > 0L) {
    all_df <- all(vapply(obj, function(x) is.data.frame(x) || inherits(x, "tbl_df"),
                         logical(1L)))
    if (all_df) {
      if (merge_list_df(obj, outp)) return("list_of_df")
    }
    # Fallback: try list of matrices
    all_m <- all(vapply(obj, is.matrix, logical(1L)))
    if (all_m) {
      mats <- lapply(seq_along(obj), function(i) {
        m <- obj[[i]]
        df <- as.data.frame(m, stringsAsFactors = FALSE)
        if (!is.null(rownames(m))) df <- cbind(`__rowname__` = rownames(m), df)
        df$`__item__` <- names(obj)[i] %||% sprintf("[%d]", i)
        df
      })
      if (merge_list_df(mats, outp)) return("list_of_matrix")
    }
  }
  # Final fallback: a deterministic str() dump so the two runs at least
  # compare structure even if no cells are extractable.
  dump_txt(utils::capture.output(utils::str(obj, max.level = 3L)), outp)
  "str_fallback"
}

ok <- tryCatch({
  obj <- readRDS(inp)
  kind <- try_dump(obj, outp)
  message(sprintf("rds_sidecar ok kind=%s", kind)); TRUE
}, error = function(e) {
  writeLines(character(0), outp)
  message(sprintf("rds_sidecar fail err=%s", conditionMessage(e))); FALSE
})
quit(status = 0)
