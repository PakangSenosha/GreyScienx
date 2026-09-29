import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const origin = "https://greyscienx.com";
const keyFile = path.join(root, "public", "indexnow-key.txt");
const key = fs.readFileSync(keyFile, "utf8").trim();
const keyLocation = `${origin}/indexnow-key.txt`;
const sitemapPaths = ["/sitemap.xml", "/sitemap-research.xml", "/sitemap-series.xml", "/sitemap-datasets.xml", "/sitemap-standards.xml"];
const urls = new Set([origin]);
const sitemapResults = [];

for (const sitemapPath of sitemapPaths) {
  const response = await fetch(`${origin}${sitemapPath}`, {
    headers: { "User-Agent": "GreyScienx-IndexNow-Submitter/1.0" },
    signal: AbortSignal.timeout(30_000),
  });
  const body = await response.text();
  if (!response.ok) throw new Error(`${sitemapPath} returned ${response.status}`);
  for (const match of body.matchAll(/<loc>([^<]+)<\/loc>/g)) urls.add(match[1].replaceAll("&amp;", "&"));
  sitemapResults.push({ path: sitemapPath, status: response.status, urls: [...body.matchAll(/<loc>/g)].length });
}

const keyResponse = await fetch(keyLocation, { signal: AbortSignal.timeout(30_000) });
const publishedKey = (await keyResponse.text()).trim();
if (!keyResponse.ok || publishedKey !== key) throw new Error(`Published IndexNow key validation failed with ${keyResponse.status}`);

const response = await fetch("https://api.indexnow.org/indexnow", {
  method: "POST",
  headers: { "Content-Type": "application/json; charset=utf-8", "User-Agent": "GreyScienx-IndexNow-Submitter/1.0" },
  body: JSON.stringify({
    host: "greyscienx.com",
    key,
    keyLocation,
    urlList: [...urls],
  }),
  signal: AbortSignal.timeout(60_000),
});
const responseBody = await response.text();
const accepted = response.status === 200 || response.status === 202;
const report = {
  schema_version: "GreyScienxIndexNowSubmission 1.0",
  submitted_at: new Date().toISOString(),
  endpoint: "https://api.indexnow.org/indexnow",
  host: "greyscienx.com",
  key_location: keyLocation,
  sitemap_results: sitemapResults,
  unique_urls_submitted: urls.size,
  status: response.status,
  accepted,
  response_body: responseBody || null,
};
const output = path.join(root, "research", "templates", "semantic-twin", "indexnow-submission-report.json");
fs.writeFileSync(output, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ accepted, status: response.status, unique_urls_submitted: urls.size, output: path.relative(root, output).replaceAll("\\", "/") }, null, 2));
if (!accepted) process.exitCode = 1;
