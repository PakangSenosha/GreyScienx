import dns from "node:dns/promises";
import fs from "node:fs";
import https from "node:https";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "research", "templates", "semantic-twin", "live-deployment-validation-report.json");
const origin = (process.env.GREYSCIENCX_LIVE_ORIGIN ?? "https://greyscienx.com").replace(/\/$/, "");
const host = new URL(origin).hostname;
const checks = [];
const warnings = [];

function record(name, passed, details = {}) {
  checks.push({ name, passed, ...details });
  return passed;
}

async function request(url, init = {}) {
  const started = performance.now();
  const response = await fetch(url, {
    redirect: "follow",
    signal: AbortSignal.timeout(30_000),
    headers: { "User-Agent": "GreyScienx-Live-Validator/1.0", ...(init.headers ?? {}) },
    ...init,
  });
  const body = await response.text();
  return {
    url: response.url,
    status: response.status,
    elapsed_ms: Math.round(performance.now() - started),
    headers: Object.fromEntries(response.headers.entries()),
    body,
  };
}

async function headerOnly(url) {
  const started = performance.now();
  const response = await fetch(url, {
    redirect: "follow",
    signal: AbortSignal.timeout(30_000),
    headers: { "User-Agent": "GreyScienx-Live-Validator/1.0" },
  });
  await response.body?.cancel();
  return {
    url: response.url,
    status: response.status,
    elapsed_ms: Math.round(performance.now() - started),
    cache_status: response.headers.get("cf-cache-status"),
    cache_control: response.headers.get("cache-control"),
    etag: response.headers.get("etag"),
    cf_ray: response.headers.get("cf-ray"),
  };
}

async function rpc(method, params, id, accept = "application/json") {
  const response = await request(`${origin}/mcp`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: accept, "MCP-Protocol-Version": "2025-03-26" },
    body: JSON.stringify({ jsonrpc: "2.0", id, method, params }),
  });
  return response;
}

async function manualHttpsRequest(url, address = null) {
  return new Promise((resolve, reject) => {
    const request = https.request(url, {
      method: "GET",
      ...(address ? {
        lookup: (_hostname, options, callback) => options?.all
          ? callback(null, [{ address, family: 4 }])
          : callback(null, address, 4),
      } : {}),
      headers: { "User-Agent": "GreyScienx-Live-Validator/1.0" },
    }, (response) => {
      response.resume();
      resolve({ status: response.statusCode ?? 0, location: response.headers.location ?? null });
    });
    request.setTimeout(30_000, () => request.destroy(new Error("HTTPS request timed out")));
    request.on("error", reject);
    request.end();
  });
}

async function runPool(items, concurrency, worker) {
  const results = new Array(items.length);
  let cursor = 0;
  async function consume() {
    while (cursor < items.length) {
      const index = cursor++;
      try {
        results[index] = await worker(items[index], index);
      } catch (error) {
        results[index] = { url: items[index], status: 0, error: error instanceof Error ? error.message : String(error) };
      }
    }
  }
  await Promise.all(Array.from({ length: Math.min(concurrency, items.length) }, consume));
  return results;
}

const dnsResult = { a: [], aaaa: [], ns: [], www: [] };
const publicResolver = new dns.Resolver();
publicResolver.setServers(["1.1.1.1", "8.8.8.8"]);
try { dnsResult.a = await dns.resolve4(host, { ttl: true }); } catch (error) { dnsResult.a_error = error.code ?? String(error); }
try { dnsResult.aaaa = await dns.resolve6(host, { ttl: true }); } catch (error) { dnsResult.aaaa_error = error.code ?? String(error); }
try { dnsResult.ns = await dns.resolveNs(host); } catch (error) { dnsResult.ns_error = error.code ?? String(error); }
try { dnsResult.www = await publicResolver.resolve4(`www.${host}`, { ttl: true }); } catch (error) { dnsResult.www_error = error.code ?? String(error); }
record("dns_apex_resolves", dnsResult.a.length + dnsResult.aaaa.length > 0, dnsResult);
record("dns_uses_cloudflare_nameservers", dnsResult.ns.length > 0 && dnsResult.ns.every((item) => item.endsWith(".ns.cloudflare.com")), { nameservers: dnsResult.ns });
if (dnsResult.www.length === 0) warnings.push(`www.${host} is not configured.`);

let wwwRedirect;
try {
  wwwRedirect = await manualHttpsRequest(`https://www.${host}/research`, dnsResult.www[0]?.address ?? null);
} catch (error) {
  wwwRedirect = { status: 0, error: error instanceof Error ? error.message : String(error) };
}
record("www_redirects_to_apex", [301, 308].includes(wwwRedirect.status) && wwwRedirect.location === `${origin}/research`, wwwRedirect);

const homepage = await request(origin);
record("https_homepage", homepage.status === 200 && homepage.headers["content-type"]?.includes("text/html"), {
  status: homepage.status,
  final_url: homepage.url,
  elapsed_ms: homepage.elapsed_ms,
  server: homepage.headers.server,
  cf_ray: homepage.headers["cf-ray"],
});
record("homepage_canonical_and_jsonld", homepage.body.includes(`<link rel="canonical" href="${origin}"`) && homepage.body.includes("application/ld+json"));

const robots = await request(`${origin}/robots.txt`);
const sitemapPaths = ["/sitemap.xml", "/sitemap-research.xml", "/sitemap-series.xml", "/sitemap-datasets.xml", "/sitemap-standards.xml"];
record("robots_allows_and_discovers_sitemaps", robots.status === 200 && /Allow:\s*\//i.test(robots.body) && sitemapPaths.every((item) => robots.body.includes(`${origin}${item}`)), {
  status: robots.status,
  content_type: robots.headers["content-type"],
});

const sitemapResults = await Promise.all(sitemapPaths.map((item) => request(`${origin}${item}`)));
const sitemapUrls = [...new Set(sitemapResults.flatMap((item) => [...item.body.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1].replaceAll("&amp;", "&"))))];
record("sitemap_documents", sitemapResults.every((item) => item.status === 200 && item.body.includes("<urlset")), {
  documents: sitemapResults.map((item, index) => ({ path: sitemapPaths[index], status: item.status, content_type: item.headers["content-type"], urls: [...item.body.matchAll(/<loc>/g)].length })),
  unique_urls: sitemapUrls.length,
  duplicate_entries: sitemapResults.reduce((sum, item) => sum + [...item.body.matchAll(/<loc>/g)].length, 0) - sitemapUrls.length,
});
record("sitemap_urls_are_canonical", sitemapUrls.length > 0 && sitemapUrls.every((url) => url.startsWith(`${origin}/`) || url === origin));

const liveUrls = await runPool(sitemapUrls, 10, headerOnly);
const brokenUrls = liveUrls.filter((item) => item.status < 200 || item.status >= 400);
record("all_sitemap_urls_resolve", brokenUrls.length === 0, {
  checked: liveUrls.length,
  successful: liveUrls.length - brokenUrls.length,
  failures: brokenUrls,
});
record("search_indexing_readiness", robots.status === 200 && sitemapUrls.length > 0 && brokenUrls.length === 0, {
  robots_status: robots.status,
  sitemap_documents: sitemapResults.length,
  canonical_urls_checked: liveUrls.length,
  note: "This validates crawlability and discovery surfaces, not third-party crawler ingestion.",
});
warnings.push("Search-engine ingestion is not immediate or controlled by the deployment; crawlability is verified, while public index inclusion requires later observation or Search Console/Bing Webmaster data.");

const llms = await request(`${origin}/llms.txt`);
record("llms_discovery", llms.status === 200 && llms.headers["content-type"]?.includes("text/plain") && llms.body.includes("GreyScienx"), {
  status: llms.status,
  cache_control: llms.headers["cache-control"],
  bytes: Buffer.byteLength(llms.body),
});
const feed = await request(`${origin}/feed.xml`);
record("rss_feed", feed.status === 200 && /<(rss|feed)\b/i.test(feed.body), { status: feed.status, content_type: feed.headers["content-type"] });
const researchIndex = await request(`${origin}/research/index.md`);
record("machine_readable_research_index", researchIndex.status === 200 && researchIndex.body.includes("GreyScienx"), {
  status: researchIndex.status,
  content_type: researchIndex.headers["content-type"],
  bytes: Buffer.byteLength(researchIndex.body),
});
const indexNowKey = await request(`${origin}/indexnow-key.txt`);
record("indexnow_key_is_published", indexNowKey.status === 200 && /^[a-f0-9]{32,128}$/i.test(indexNowKey.body.trim()), {
  status: indexNowKey.status,
  key_location: `${origin}/indexnow-key.txt`,
});
const googleVerificationFiles = fs.readdirSync(path.join(root, "public"))
  .filter((name) => /^google[a-f0-9]+\.html$/i.test(name));
const googleVerificationResults = await Promise.all(googleVerificationFiles.map(async (name) => {
  const result = await request(`${origin}/${name}`);
  return {
    file: name,
    status: result.status,
    valid: result.status === 200 && result.body.trim() === `google-site-verification: ${name}`,
  };
}));
record("google_search_console_verification_file", googleVerificationResults.length > 0 && googleVerificationResults.every((item) => item.valid), {
  files: googleVerificationResults,
});

const collection = await request(`${origin}/api/v1/research`);
let collectionJson;
try { collectionJson = JSON.parse(collection.body); } catch { collectionJson = null; }
const collectionCount = Array.isArray(collectionJson) ? collectionJson.length : collectionJson?.studies?.length ?? collectionJson?.results?.length ?? null;
record("research_api", collection.status === 200 && collectionJson !== null, {
  status: collection.status,
  content_type: collection.headers["content-type"],
  reported_items: collectionCount,
});

const search = await request(`${origin}/api/v1/search?q=${encodeURIComponent("retirement at 60 worker retiree ratio")}`);
let searchJson;
try { searchJson = JSON.parse(search.body); } catch { searchJson = null; }
record("research_search", search.status === 200 && searchJson?.method === "hybrid_concept_vector_v1" && searchJson?.results?.length > 0, {
  status: search.status,
  cache_control: search.headers["cache-control"],
  result_count: searchJson?.results?.length ?? 0,
  first_result: searchJson?.results?.[0]?.id ?? searchJson?.results?.[0]?.title ?? null,
});

const articlePath = "/research/population-futures/when-retirement-becomes-impossible";
const article = await request(`${origin}${articlePath}`);
record("representative_article", article.status === 200 && article.body.includes("When Retirement Becomes Impossible") && article.body.includes("application/ld+json"), {
  status: article.status,
  elapsed_ms: article.elapsed_ms,
});
const negotiatedJson = await request(`${origin}${articlePath}`, { headers: { Accept: "application/json" } });
record("content_negotiation_json", negotiatedJson.status === 200 && negotiatedJson.headers["content-type"]?.includes("application/json"), {
  status: negotiatedJson.status,
  content_type: negotiatedJson.headers["content-type"],
});
const negotiatedMarkdown = await request(`${origin}${articlePath}`, { headers: { Accept: "text/markdown" } });
record("content_negotiation_markdown", negotiatedMarkdown.status === 200 && negotiatedMarkdown.headers["content-type"]?.includes("text/markdown"), {
  status: negotiatedMarkdown.status,
  content_type: negotiatedMarkdown.headers["content-type"],
});

const discovery = await request(`${origin}/mcp`);
let discoveryJson;
try { discoveryJson = JSON.parse(discovery.body); } catch { discoveryJson = null; }
record("mcp_discovery", discovery.status === 200 && discoveryJson?.protocol === "mcp" && discoveryJson?.transport === "stateless-json-rpc", {
  status: discovery.status,
  protocol_version: discoveryJson?.protocolVersion,
  tool_count: discoveryJson?.tools?.length ?? 0,
  cache_control: discovery.headers["cache-control"],
});
const initialize = await rpc("initialize", { protocolVersion: "2025-03-26", capabilities: {}, clientInfo: { name: "GreyScienx Live Validator", version: "1.0.0" } }, 1);
const initializeJson = JSON.parse(initialize.body);
record("mcp_initialize", initialize.status === 200 && initializeJson?.result?.serverInfo?.name === "GreyScienx", {
  status: initialize.status,
  protocol_version: initializeJson?.result?.protocolVersion,
  server_version: initializeJson?.result?.serverInfo?.version,
});
const toolsList = await rpc("tools/list", {}, 2);
const toolsJson = JSON.parse(toolsList.body);
record("mcp_tools_list", toolsList.status === 200 && toolsJson?.result?.tools?.some((item) => item.name === "search_research"), {
  status: toolsList.status,
  tool_count: toolsJson?.result?.tools?.length ?? 0,
});
const toolCall = await rpc("tools/call", { name: "search_research", arguments: { query: "retirement at 60 worker retiree ratio" } }, 3);
const toolJson = JSON.parse(toolCall.body);
record("mcp_tool_call", toolCall.status === 200 && toolJson?.result?.isError === false && toolJson?.result?.content?.[0]?.text?.includes("GSX:POP-001"), {
  status: toolCall.status,
  is_error: toolJson?.result?.isError,
  returned_expected_study: toolJson?.result?.content?.[0]?.text?.includes("GSX:POP-001") ?? false,
});
const sse = await rpc("tools/list", {}, 4, "text/event-stream");
record("mcp_sse_delivery", sse.status === 200 && sse.headers["content-type"]?.includes("text/event-stream") && sse.body.startsWith("event: message"), {
  status: sse.status,
  content_type: sse.headers["content-type"],
});

const staticAsset = `${origin}/brand/greyscienx-wordmark.svg`;
const assetRequests = [await headerOnly(staticAsset), await headerOnly(staticAsset), await headerOnly(staticAsset)];
record("edge_static_asset_cache", assetRequests[1].status === 200 && assetRequests[2].cache_status === "HIT" && assetRequests.every((item) => item.etag === assetRequests[0].etag), {
  requests: assetRequests,
});
const pdfAsset = `${origin}/research/population-futures/when-retirement-becomes-impossible.pdf`;
const pdfRequests = [await headerOnly(pdfAsset), await headerOnly(pdfAsset)];
record("edge_pdf_cache", pdfRequests[1].status === 200 && pdfRequests[1].cache_status === "HIT" && pdfRequests[0].etag === pdfRequests[1].etag, {
  requests: pdfRequests,
});
record("mcp_cache_is_disabled", discovery.headers["cache-control"]?.includes("no-store"), { cache_control: discovery.headers["cache-control"] });
record("search_cache_policy", search.headers["cache-control"]?.includes("max-age=300"), { cache_control: search.headers["cache-control"] });

const failed = checks.filter((item) => !item.passed);
const report = {
  schema_version: "GreyScienxLiveDeploymentValidation 1.0",
  generated_at: new Date().toISOString(),
  origin,
  worker_version: process.env.GREYSCIENCX_WORKER_VERSION ?? null,
  passed: failed.length === 0,
  summary: {
    checks: checks.length,
    passed: checks.length - failed.length,
    failed: failed.length,
    sitemap_urls_checked: liveUrls.length,
    warnings: warnings.length,
  },
  warnings,
  checks,
};

fs.writeFileSync(output, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ ...report.summary, passed: report.passed, output: path.relative(root, output).replaceAll("\\", "/") }, null, 2));
if (!report.passed) process.exitCode = 1;
