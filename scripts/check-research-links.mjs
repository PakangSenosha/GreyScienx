import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { researchObjects } from "../lib/research/registry.ts";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sources = new Map();
for (const study of researchObjects) {
  for (const source of study.sources) {
    if (!source.href || source.type === "manuscript") continue;
    const key = source.href.split("#")[0];
    const current = sources.get(key) ?? { url: key, studies: [], source_ids: [] };
    if (!current.studies.includes(study.id)) current.studies.push(study.id);
    if (!current.source_ids.includes(source.id)) current.source_ids.push(source.id);
    sources.set(key, current);
  }
}

const queue = [...sources.values()];
const results = [];
const workers = Array.from({ length: Math.min(16, queue.length) }, async () => {
  while (queue.length) {
    const source = queue.shift();
    if (!source) break;
    results.push({ ...source, ...(await check(source.url)) });
  }
});
await Promise.all(workers);
results.sort((a, b) => a.url.localeCompare(b.url));

const counts = { ok: 0, restricted: 0, unverified: 0, failed: 0 };
for (const result of results) counts[result.outcome] += 1;
const sourceSet = results.map((item) => item.url).join("\n");
const report = {
  schema_version: "GreyScienxLinkCheck 1.1",
  generated_at: new Date().toISOString(),
  scope: "Automated HTTP reachability check. Outcomes distinguish reachable, access-restricted, transient or network-unverified, and confirmed 404/410 links. Reachability is not proof that a source supports a claim.",
  source_set_sha256: crypto.createHash("sha256").update(sourceSet).digest("hex"),
  checked: results.length,
  ...counts,
  results,
};
const reportFile = path.join(root, "research", "templates", "semantic-twin", "link-check-report.json");
fs.writeFileSync(reportFile, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ ...report, results: undefined }, null, 2));
if (counts.failed) process.exitCode = 2;

async function check(url) {
  const started = Date.now();
  try {
    let response = await request(url, "HEAD");
    if (response.status >= 400) response = await request(url, "GET");
    const status = response.status;
    const final_url = response.url;
    await response.body?.cancel();
    const outcome = status < 400
      ? "ok"
      : [404, 410].includes(status)
        ? "failed"
        : status >= 500
          ? "unverified"
          : "restricted";
    return { outcome, status, final_url, elapsed_ms: Date.now() - started, error: null };
  } catch (error) {
    return {
      outcome: "unverified",
      status: null,
      final_url: null,
      elapsed_ms: Date.now() - started,
      error: error instanceof Error ? error.message : "Request failed",
    };
  }
}

async function request(url, method) {
  return fetch(url, {
    method,
    redirect: "follow",
    signal: AbortSignal.timeout(10_000),
    headers: { "User-Agent": "GreyScienx-Link-Checker/1.1" },
  });
}
