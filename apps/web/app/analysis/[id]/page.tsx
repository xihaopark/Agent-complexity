"use client";

import { useEffect, useMemo, useState } from "react";
import { getAnalysis, getMetrics, getReport } from "../../../lib/api";

const REFRESH_MS = 5000;

export default function AnalysisDetailPage({ params }: { params: { id: string } }) {
  const id = params.id;
  const [statusData, setStatusData] = useState<any>(null);
  const [report, setReport] = useState<any>(null);
  const [metrics, setMetrics] = useState<any[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;
    async function fetchAll() {
      try {
        const [statusRes, reportRes, metricRes] = await Promise.all([
          getAnalysis(id),
          getReport(id),
          getMetrics(id)
        ]);
        if (!mounted) return;
        setStatusData(statusRes);
        setReport(reportRes);
        setMetrics(metricRes);
      } catch (err: any) {
        if (!mounted) return;
        setError(err.message || "load failed");
      }
    }
    fetchAll();
    const timer = setInterval(fetchAll, REFRESH_MS);
    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, [id]);

  const grouped = useMemo(() => {
    const map: Record<string, any[]> = {};
    for (const item of metrics) {
      const key = item.scope || "unknown";
      if (!map[key]) map[key] = [];
      map[key].push(item);
    }
    return map;
  }, [metrics]);

  return (
    <main>
      <h1>Analysis #{id}</h1>
      {error ? <p style={{ color: "#b40000" }}>{error}</p> : null}
      <section className="card">
        <h3>Status</h3>
        <pre>{JSON.stringify(statusData, null, 2)}</pre>
      </section>
      <section className="card" style={{ marginTop: 16 }}>
        <h3>Report</h3>
        <pre>{JSON.stringify(report, null, 2)}</pre>
      </section>
      <section className="card" style={{ marginTop: 16 }}>
        <h3>Metrics</h3>
        {Object.entries(grouped).map(([scope, rows]) => (
          <div key={scope} style={{ marginBottom: 12 }}>
            <h4>{scope}</h4>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th align="left">Code</th>
                  <th align="left">Value</th>
                  <th align="left">CI</th>
                </tr>
              </thead>
              <tbody>
                {rows.slice(0, 120).map((row, idx) => (
                  <tr key={`${scope}-${idx}`}>
                    <td>{row.metric_code}</td>
                    <td>{row.raw_value ?? "-"}</td>
                    <td>
                      {row.ci_low !== null && row.ci_high !== null
                        ? `[${row.ci_low}, ${row.ci_high}]`
                        : "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </section>
    </main>
  );
}
