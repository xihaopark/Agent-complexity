const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export interface AnalysisCreatePayload {
  repo_url: string;
  git_ref: string;
  run_profile: string;
  repeats?: number;
  timeout_sec?: number;
  auth_token?: string;
  run_spec?: {
    setup_commands: string[];
    entry_command?: string;
    task_inputs: Record<string, unknown>[];
    env_allowlist: string[];
    repeats?: number;
    timeout_sec?: number;
  };
}

export async function createAnalysis(payload: AnalysisCreatePayload) {
  const res = await fetch(`${API_BASE}/api/v1/analyses`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error(`Create failed: ${await res.text()}`);
  }
  return await res.json();
}

export async function getAnalysis(id: string) {
  const res = await fetch(`${API_BASE}/api/v1/analyses/${id}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Status fetch failed: ${await res.text()}`);
  }
  return await res.json();
}

export async function getReport(id: string) {
  const res = await fetch(`${API_BASE}/api/v1/analyses/${id}/report`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Report fetch failed: ${await res.text()}`);
  }
  return await res.json();
}

export async function getMetrics(id: string) {
  const res = await fetch(`${API_BASE}/api/v1/analyses/${id}/metrics`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Metrics fetch failed: ${await res.text()}`);
  }
  return await res.json();
}
