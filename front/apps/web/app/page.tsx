"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { createAnalysis } from "../lib/api";

export default function HomePage() {
  const router = useRouter();
  const [repoUrl, setRepoUrl] = useState("");
  const [gitRef, setGitRef] = useState("main");
  const [authToken, setAuthToken] = useState("");
  const [entryCommand, setEntryCommand] = useState("");
  const [setupCommands, setSetupCommands] = useState("pip install -r requirements.txt || true");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const payload: any = {
        repo_url: repoUrl,
        git_ref: gitRef,
        run_profile: "standard",
        repeats: 10,
        timeout_sec: 1800
      };
      if (authToken.trim()) payload.auth_token = authToken.trim();
      if (entryCommand.trim()) {
        payload.run_spec = {
          setup_commands: setupCommands
            .split("\n")
            .map((s) => s.trim())
            .filter(Boolean),
          entry_command: entryCommand.trim(),
          task_inputs: [],
          env_allowlist: []
        };
      }
      const data = await createAnalysis(payload);
      router.push(`/analysis/${data.analysis_id}`);
    } catch (err: any) {
      setError(err.message || "submit failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>Agentic Complexity Analyzer</h1>
      <p className="muted">
        上传 GitHub 链接，自动执行静态+动态复杂度分析，并生成结构化报告。
      </p>
      <form className="card" onSubmit={onSubmit}>
        <label>GitHub Repository URL</label>
        <input
          required
          placeholder="https://github.com/org/repo"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
        />

        <div className="grid">
          <div>
            <label>Git Ref</label>
            <input value={gitRef} onChange={(e) => setGitRef(e.target.value)} />
          </div>
          <div>
            <label>Private Token (Optional)</label>
            <input
              type="password"
              placeholder="GitHub PAT"
              value={authToken}
              onChange={(e) => setAuthToken(e.target.value)}
            />
          </div>
        </div>

        <label>Entry Command (Optional, overrides auto-detect)</label>
        <input
          placeholder="python main.py"
          value={entryCommand}
          onChange={(e) => setEntryCommand(e.target.value)}
        />

        <label>Setup Commands (one per line)</label>
        <textarea value={setupCommands} onChange={(e) => setSetupCommands(e.target.value)} />

        {error ? <p style={{ color: "#b40000" }}>{error}</p> : null}
        <button type="submit" disabled={loading}>
          {loading ? "Submitting..." : "Start Analysis"}
        </button>
      </form>
    </main>
  );
}
