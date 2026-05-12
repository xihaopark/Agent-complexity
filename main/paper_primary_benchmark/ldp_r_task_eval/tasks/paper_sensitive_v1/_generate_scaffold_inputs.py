#!/usr/bin/env python3
"""Generate minimal synthetic inputs for paper_sensitive_v1 tasks (scaffold)."""
from __future__ import annotations

import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def write_tsv(path: Path, header: list[str], rows: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(header)
        w.writerows(rows)


def tiny_counts_4v4() -> tuple[list, list]:
    """30 genes x 4 samples, 2x2 (A vs B)."""
    random.seed(42)
    samples = ["S1", "S2", "S3", "S4"]
    cond = ["A", "A", "B", "B"]
    header = ["gene_id"] + samples
    rows = []
    for i in range(30):
        g = f"G{i+1:04d}"
        base = random.randint(20, 200)
        row = [g]
        for j, c in enumerate(cond):
            # tiny fold change for B
            u = 1.4 if c == "B" and i < 5 else 1.0
            row.append(max(0, int(base * u + random.randint(-5, 5))))
        rows.append(row)
    coldata = [["sample", "condition"]]
    for s, c in zip(samples, cond):
        coldata.append([s, c])
    return header, rows, coldata


def main() -> None:
    # 1) deseq2_apeglm_small_n
    h, rows, coldata = tiny_counts_4v4()
    p = ROOT / "real" / "deseq2_apeglm_small_n" / "input"
    write_tsv(p / "counts.tsv", h, rows)
    write_tsv(p / "coldata.tsv", [coldata[0], *coldata[1:]])

    # 2) deseq2_lrt_interaction — 8 samples: 2x2 factorial, 2 reps
    random.seed(43)
    samples = [f"SX{i}" for i in range(1, 9)]
    header = ["gene_id"] + samples
    tmap = {  # treatment x time
        "SX1": ("ctrl", "t0"), "SX2": ("ctrl", "t0"),
        "SX3": ("trt", "t0"), "SX4": ("trt", "t0"),
        "SX5": ("ctrl", "t1"), "SX6": ("ctrl", "t1"),
        "SX7": ("trt", "t1"), "SX8": ("trt", "t1"),
    }
    g_rows = []
    for i in range(40):
        g = f"IG{i+1:04d}"
        b = random.randint(30, 300)
        row = [g]
        for s in samples:
            tr, ti = tmap[s]
            eff = 1.0
            if tr == "trt" and ti == "t1" and i < 4:
                eff = 1.5
            row.append(max(0, int(b * eff + random.randint(-8, 8))))
        g_rows.append(row)
    write_tsv(ROOT / "real/deseq2_lrt_interaction/input/counts.tsv", header, g_rows)
    cd = [["sample", "treatment", "time"]]
    for s in samples:
        tr, ti = tmap[s]
        cd.append([s, tr, ti])
    write_tsv(ROOT / "real/deseq2_lrt_interaction/input/coldata.tsv", [cd[0], *cd[1:]])

    # 3) limma_voom_weights — S1..S5, one "bad" (low total count scale)
    random.seed(44)
    samps = [f"SQ{i}" for i in range(1, 6)]
    h2 = ["gene_id"] + samps
    depth = [50, 50, 50, 5, 50]  # SQ4 is bad
    g2 = []
    for i in range(35):
        g = f"VG{i+1:04d}"
        row = [g]
        for j, s in enumerate(samps):
            b = 100 + 10 * i
            m = 0.6 if s in ("SQ1", "SQ2", "SQ3") else (0.45 if s == "SQ4" else 0.5)
            row.append(max(5, int(b * m * (depth[j] / 50.0))))
        g2.append(row)
    write_tsv(ROOT / "real/limma_voom_weights/input/counts.tsv", h2, g2)
    c2 = [
        ["sample", "group", "seq_depth"],
        ["SQ1", "A", "50M"],
        ["SQ2", "A", "48M"],
        ["SQ3", "A", "49M"],
        ["SQ4", "B", "0.1M"],
        ["SQ5", "B", "47M"],
    ]
    write_tsv(ROOT / "real/limma_voom_weights/input/coldata.tsv", c2[0:1] + c2[1:])

    # 4) macs2 — tiny bed6
    bed = """chr1\\t1000\\t1500\\t.\\t1000\\t.\\nchr1\\t1600\\t2000\\t.\\t800\\t.\\n""".encode()
    p4 = ROOT / "real/macs2_broad_histone/input"
    p4.mkdir(parents=True, exist_ok=True)
    (p4 / "fragments.bed").write_bytes(bed)
    (p4 / "control.bed").write_text("chr1\\t0\\t5000\\n")
    (p4 / "README.md").write_text("Synthetic BED6; invoke macs2 in broad mode.\\n")

    # 5) combat
    random.seed(45)
    s8 = [f"C{i}" for i in range(1, 9)]
    h5 = ["gene_id"] + s8
    rows5 = []
    for i in range(25):
        g = f"CG{i+1:04d}"
        row = [g]
        for j, s in enumerate(s8):
            batch = 0 if j < 4 else 1
            bshift = 1.0 + 0.35 * batch
            cond = 0.15 * (1 if j % 2 == 0 else -1)
            v = int((80 + i) * bshift * (1 + cond) + random.randint(-3, 3))
            row.append(max(5, v))
        rows5.append(row)
    write_tsv(ROOT / "real/combat_seq_batch/input/counts.tsv", h5, rows5)
    bmeta = [
        ["sample", "condition", "batch"],
        ["C1", "A", "B1"],
        ["C2", "A", "B1"],
        ["C3", "B", "B1"],
        ["C4", "B", "B1"],
        ["C5", "A", "B2"],
        ["C6", "A", "B2"],
        ["C7", "B", "B2"],
        ["C8", "B", "B2"],
    ]
    write_tsv(ROOT / "real/combat_seq_batch/input/coldata.tsv", bmeta[0:1] + bmeta[1:])

    # 6) seurat — gene x cell count matrix (small)
    p6 = ROOT / "real/seurat_sctransform_scaling/input"
    p6.mkdir(parents=True, exist_ok=True)
    genes = [f"GENE_{i:03d}" for i in range(1, 51)]
    cells = [f"CELL_{i:02d}" for i in range(1, 21)]
    h6 = ["gene_id"] + cells
    random.seed(46)
    m6 = []
    for g in genes:
        row = [g]
        for c in range(20):
            u = 1.2 if c >= 10 else 1.0
            row.append(max(0, int(random.negative_binomial(5, 0.3) * u)))
        m6.append(row)
    write_tsv(p6 / "counts_matrix.tsv", h6, m6)
    (p6 / "README.md").write_text("Load `counts_matrix.tsv` as features x cells (Seurat: transpose to cells x features). 20 cells, 50 genes.\\n")

    # 7) clusterProfiler
    p7 = ROOT / "real/clusterprofiler_gsea_vs_ora/input"
    p7.mkdir(parents=True, exist_ok=True)
    with (p7 / "de_table.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["gene_id", "log2FoldChange", "padj"])
        random.seed(47)
        for i in range(120):
            w.writerow([f"G{i+1:05d}", round(random.uniform(-2, 2), 3), 10 ** random.uniform(-4, 0)])
    (p7 / "org_db.txt").write_text("org.Mm.eg.db\\n")

    # 8) edgeR
    random.seed(48)
    s6 = [f"E{i}" for i in range(1, 7)]
    h8 = ["gene_id"] + s6
    rows8 = []
    for i in range(40):
        g = f"EG{i+1:04d}"
        row = [g]
        for j, s in enumerate(s6):
            base = 120 + 3 * i
            o = 0.4 if s == "E3" else 0
            row.append(max(0, int(base * (0.2 if o else 1) + random.randint(-6, 6))))
        rows8.append(row)
    write_tsv(ROOT / "real/edger_robust_filtering/input/counts.tsv", h8, rows8)
    e2 = [
        ["sample", "group", "is_outlier"],
        ["E1", "A", "0"],
        ["E2", "A", "0"],
        ["E3", "A", "1"],
        ["E4", "B", "0"],
        ["E5", "B", "0"],
        ["E6", "B", "0"],
    ]
    write_tsv(ROOT / "real/edger_robust_filtering/input/coldata.tsv", e2[0:1] + e2[1:])

    # 9) methylkit regions
    p9 = ROOT / "real/methylkit_diffmeth_params/input"
    p9.mkdir(parents=True, exist_ok=True)
    rlines = [
        ["chr", "start", "end", "sample_id", "meth", "unmeth", "coverage"],
    ]
    for s in ("S1", "S2", "S3", "S4"):
        for r in range(1, 11):
            ch = "chr1"
            st = 1000 * r
            en = st + 200
            cov = 20 + r
            meths = 8 if s in ("S1", "S2") else 3
            rlines.append(
                [str(ch), str(st), str(en), s, str(meths), str(cov - meths), str(cov)]
            )
    write_tsv(p9 / "regions.tsv", rlines[0], rlines[1:])

    # 10) limma duplicate
    h10, rows10, _ = tiny_counts_4v4()  # reuse 4 sample structure -> expand to 6 (3 patients)
    # overwrite with 6 samples, paired
    samps = ["P1_T", "P1_C", "P2_T", "P2_C", "P3_T", "P3_C"]
    random.seed(49)
    h10 = ["gene_id"] + samps
    rows10 = []
    for i in range(32):
        g = f"PG{i+1:04d}"
        base = 90 + 2 * i
        row = [g]
        for j, s in enumerate(samps):
            is_trt = "_T" in s
            row.append(
                max(
                    0,
                    int(
                        base * (1.25 if is_trt and i < 3 else 1.0) + random.randint(-4, 4)
                    ),
                )
            )
        rows10.append(row)
    write_tsv(ROOT / "real/limma_duplicatecorrelation/input/counts.tsv", h10, rows10)
    c10 = [
        ["sample", "patient", "treatment"],
        ["P1_T", "P1", "trt"],
        ["P1_C", "P1", "ctrl"],
        ["P2_T", "P2", "trt"],
        ["P2_C", "P2", "ctrl"],
        ["P3_T", "P3", "trt"],
        ["P3_C", "P3", "ctrl"],
    ]
    write_tsv(ROOT / "real/limma_duplicatecorrelation/input/coldata.tsv", c10[0:1] + c10[1:])

    # 11) integration — two 10-cell batches
    p11 = ROOT / "real/seurat_integration_method/input"
    p11.mkdir(parents=True, exist_ok=True)
    genes2 = [f"IG_{i:03d}" for i in range(1, 31)]
    b1 = [f"B1_{i:02d}" for i in range(1, 11)]
    b2 = [f"B2_{i:02d}" for i in range(1, 11)]
    random.seed(50)
    h_b1 = ["gene_id"] + b1
    h_b2 = ["gene_id"] + b2
    mat1, mat2 = [], []
    for g in genes2:
        m1, m2 = [g], [g]
        for _ in b1:
            m1.append(max(0, int(random.negative_binomial(4, 0.25) * 0.7)))
        for _ in b2:
            m2.append(max(0, int(random.negative_binomial(4, 0.25) * 1.3)))
        mat1.append(m1)
        mat2.append(m2)
    write_tsv(p11 / "batch1_counts.tsv", h_b1, mat1)
    write_tsv(p11 / "batch2_counts.tsv", h_b2, mat2)
    (p11 / "README.md").write_text("Two gene x cell count matrices; merge for Seurat with batch labels.\\n")

    # 12) deseq2_shrinkage_comparison
    random.seed(51)
    s12 = [f"N{i}" for i in range(1, 7)]
    h12 = ["gene_id"] + s12
    r12 = []
    for i in range(50):
        g = f"SG{i+1:04d}"
        b = 100 + i
        row = [g]
        for j, _ in enumerate(s12):
            grp = "A" if j < 3 else "B"
            u = 1.35 if grp == "B" and i < 7 else 1.0
            row.append(max(0, int(b * u + random.randint(-4, 4))))
        r12.append(row)
    write_tsv(ROOT / "real/deseq2_shrinkage_comparison/input/counts.tsv", h12, r12)
    c12 = [["sample", "condition"]]
    for s in s12:
        c12.append([s, "A" if s in ("N1", "N2", "N3") else "B"])
    write_tsv(ROOT / "real/deseq2_shrinkage_comparison/input/coldata.tsv", c12[0:1] + c12[1:])

    print("Wrote scaffold inputs to", ROOT)


if __name__ == "__main__":
    main()
