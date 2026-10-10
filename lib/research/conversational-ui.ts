import type { Claim, ResearchObject } from "./schema";

export const ANALYSIS_SUMMARY_RESOURCE_URI = "ui://greyscienx/analysis-summary-v1.html";
export const MCP_APP_MIME_TYPE = "text/html;profile=mcp-app";

export const conversationalTokens = Object.freeze({
  color: {
    brand: { primary: "#f26157", secondary: "#131200" },
    semantic: {
      success: "#238665",
      warning: "#a06400",
      danger: "#c84a42",
      information: "#456d94",
    },
    surface: { default: "#fbfffe", subtle: "#f0f1f2" },
    text: { primary: "#131200", secondary: "#5f5d56" },
    border: { subtle: "rgba(19,18,0,.18)" },
  },
  type: {
    family: {
      display: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
      interface: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
    },
  },
  radius: { control: "10px", panel: "16px" },
});

export type AnalysisSummaryPayload = ReturnType<typeof buildAnalysisSummaryPayload>;

export function buildAnalysisSummaryPayload(study: ResearchObject, claimId?: string | null) {
  const claim = selectClaim(study, claimId);
  if (claimId && !claim) throw new Error(`No published claim ${claimId} exists for ${study.id}.`);

  const finding = claim?.claim ?? study.answer?.conditional_answer ?? study.summary;
  const limitation =
    claim?.main_limitation ??
    study.answer?.main_limitation ??
    "This is a modelled research record. Read the manuscript and assumptions before treating the result as general evidence.";

  return {
    widget: "analysis_summary" as const,
    widget_version: "1.0.0" as const,
    status: "complete" as const,
    study: {
      id: study.id,
      title: study.title,
      question: study.primary_question,
      series: study.series_title,
      research_type: study.research_type,
      evidence_status: study.evidence_status,
      date_modified: study.date_modified,
      extraction_status: study.extraction_status,
    },
    finding: {
      label: claim ? "Modelled conditional finding" : "Research summary",
      text: finding,
      claim_id: claim?.id ?? null,
      claim_type: claim?.claim_type ?? null,
      evidence_status: claim?.evidence_status ?? study.evidence_status,
      sensitivity: claim?.sensitivity ?? study.answer?.sensitivity ?? null,
      confidence: {
        value: null,
        label: "Not numerically rated",
        explanation: "GreyScienx does not publish a numeric confidence score for this finding.",
      },
      limitation,
    },
    evidence: {
      assumption_count: study.assumptions.length,
      result_count: study.results.length,
      source_count: study.sources.length,
      assumptions: study.assumptions.slice(0, 3).map((assumption) => ({
        id: assumption.id,
        name: assumption.name,
        sensitivity: assumption.sensitivity,
        href: assumption.href,
      })),
      results: study.results.slice(0, 3).map((result) => ({
        id: result.id,
        statement: result.statement,
        value: result.value,
        unit: result.unit,
        scenario: result.scenario,
        href: result.href,
      })),
      sources: study.sources.slice(0, 3).map((source) => ({
        id: source.id,
        title: source.title,
        author_or_publisher: source.author_or_publisher ?? null,
        date: source.date ?? null,
        href: source.href,
      })),
    },
    freshness: {
      date: study.date_modified,
      label: `Research record updated ${study.date_modified}`,
      stale: false,
    },
    links: {
      study: study.links.html,
      manuscript: study.links.markdown,
      claim: claim?.href ?? null,
    },
    citation: study.citation.text,
  };
}

export function analysisSummaryResource(previewPayload?: AnalysisSummaryPayload) {
  return {
    uri: ANALYSIS_SUMMARY_RESOURCE_URI,
    name: "greyscienx-analysis-summary",
    title: "GreyScienx analysis summary",
    description:
      "A compact, accessible summary of one GreyScienx finding, its evidence status, sensitivity, provenance and main limitation.",
    mimeType: MCP_APP_MIME_TYPE,
    text: analysisSummaryHtml(previewPayload),
    _meta: {
      ui: {
        prefersBorder: true,
        domain: "https://greyscienx.com",
        csp: {
          connectDomains: [] as string[],
          resourceDomains: [] as string[],
        },
      },
      "openai/widgetDescription":
        "Shows one GreyScienx modelled finding with its evidence boundary, assumptions, source counts and a link to the full study.",
      "openai/widgetPrefersBorder": true,
    },
  };
}

function selectClaim(study: ResearchObject, claimId?: string | null): Claim | null {
  if (!study.claims.length) return null;
  if (!claimId) return study.claims[0];
  const normalized = claimId.trim().toLowerCase();
  return (
    study.claims.find(
      (claim) => claim.id.toLowerCase() === normalized || claim.local_id.toLowerCase() === normalized,
    ) ?? null
  );
}

function safeJson(value: unknown) {
  return JSON.stringify(value ?? null)
    .replaceAll("<", "\\u003c")
    .replaceAll(">", "\\u003e")
    .replaceAll("&", "\\u0026")
    .replaceAll("\u2028", "\\u2028")
    .replaceAll("\u2029", "\\u2029");
}

function analysisSummaryHtml(previewPayload?: AnalysisSummaryPayload) {
  return ANALYSIS_SUMMARY_HTML.replace("__GREYSCIENCX_PREVIEW_DATA__", safeJson(previewPayload));
}

const ANALYSIS_SUMMARY_HTML = String.raw`<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />
  <meta name="color-scheme" content="light dark" />
  <title>GreyScienx analysis summary</title>
  <style>
    :root {
      color-scheme: light dark;
      --brand: #f26157;
      --ink: #131200;
      --paper: #fbfffe;
      --subtle: #f0f1f2;
      --muted: #5f5d56;
      --line: rgba(19,18,0,.18);
      --success: #238665;
      --warning: #a06400;
      --focus: #456d94;
      --shadow: 0 10px 30px rgba(19,18,0,.08);
      --radius-control: 10px;
      --radius-panel: 16px;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-synthesis: none;
    }
    :root[data-theme="dark"] {
      --ink: #fbfffe;
      --paper: #171714;
      --subtle: #23231f;
      --muted: #bbb9b0;
      --line: rgba(251,255,254,.2);
      --success: #72d2b3;
      --warning: #f2ba65;
      --focus: #91b7d9;
      --shadow: none;
    }
    @media (prefers-color-scheme: dark) {
      :root:not([data-theme="light"]) {
        --ink: #fbfffe;
        --paper: #171714;
        --subtle: #23231f;
        --muted: #bbb9b0;
        --line: rgba(251,255,254,.2);
        --success: #72d2b3;
        --warning: #f2ba65;
        --focus: #91b7d9;
        --shadow: none;
      }
    }
    * { box-sizing: border-box; }
    html, body { margin: 0; min-width: 0; background: transparent; }
    body { padding: 8px; color: var(--ink); }
    button, a { font: inherit; }
    button:focus-visible, a:focus-visible, summary:focus-visible {
      outline: 3px solid var(--focus);
      outline-offset: 3px;
    }
    .card {
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: var(--radius-panel);
      background: var(--paper);
      box-shadow: var(--shadow);
    }
    .brand-line { height: 7px; background: var(--brand); }
    .content { padding: clamp(18px, 4vw, 28px); }
    .identity { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
    .brand { font-size: 12px; font-weight: 900; letter-spacing: .13em; text-transform: uppercase; }
    .status {
      display: inline-flex; align-items: center; gap: 7px; padding: 6px 9px;
      border: 1px solid var(--line); border-radius: 999px; color: var(--muted);
      font-size: 12px; font-weight: 750;
    }
    .status::before { width: 8px; height: 8px; border-radius: 50%; background: var(--success); content: ""; }
    .eyebrow { margin: 24px 0 8px; color: var(--brand); font-size: 12px; font-weight: 850; letter-spacing: .08em; text-transform: uppercase; }
    h1 { margin: 0; font-size: clamp(24px, 6vw, 36px); letter-spacing: -.045em; line-height: 1.02; }
    .question { margin: 10px 0 0; color: var(--muted); font-size: 14px; line-height: 1.5; }
    .finding { margin: 22px 0 0; padding: 18px 0; border-block: 1px solid var(--line); }
    .finding-label, .meta-label { color: var(--muted); font-size: 11px; font-weight: 850; letter-spacing: .08em; text-transform: uppercase; }
    .finding blockquote { margin: 9px 0 0; font-size: clamp(17px, 4.2vw, 22px); font-weight: 720; letter-spacing: -.02em; line-height: 1.38; }
    .meta-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); margin-top: 18px; border: 1px solid var(--line); border-radius: 12px; }
    .meta-item { min-width: 0; padding: 13px; border-right: 1px solid var(--line); }
    .meta-item:last-child { border-right: 0; }
    .meta-value { display: block; margin-top: 5px; font-size: 13px; font-weight: 760; overflow-wrap: anywhere; }
    .limitation { margin-top: 18px; padding: 14px 16px; border-left: 4px solid var(--warning); background: var(--subtle); }
    .limitation strong { display: block; margin-bottom: 5px; font-size: 12px; }
    .limitation p { margin: 0; color: var(--muted); font-size: 13px; line-height: 1.48; }
    .evidence-panel { margin-top: 18px; padding-top: 18px; border-top: 1px solid var(--line); }
    .evidence-panel[hidden] { display: none; }
    .evidence-heading { margin: 0 0 12px; font-size: 16px; }
    .evidence-group + .evidence-group { margin-top: 15px; }
    .evidence-list { margin: 7px 0 0; padding: 0; list-style: none; }
    .evidence-list li { padding: 10px 0; border-top: 1px solid var(--line); }
    .evidence-list a { color: inherit; font-size: 13px; font-weight: 700; line-height: 1.4; text-decoration-color: var(--brand); text-underline-offset: 3px; }
    .evidence-list span { display: block; margin-top: 3px; color: var(--muted); font-size: 12px; line-height: 1.4; }
    .empty-evidence { margin: 7px 0 0; color: var(--muted); font-size: 13px; }
    .freshness { margin: 17px 0 0; color: var(--muted); font-size: 12px; }
    .actions { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 20px; }
    .action {
      min-height: 44px; display: inline-flex; align-items: center; justify-content: center;
      padding: 10px 14px; border: 1px solid var(--ink); border-radius: var(--radius-control);
      background: transparent; color: var(--ink); font-size: 13px; font-weight: 800; text-decoration: none; cursor: pointer;
    }
    .action-primary { border-color: var(--brand); background: var(--brand); color: #131200; }
    .state { padding: 30px; }
    .state h1 { font-size: 24px; }
    .state p { margin: 10px 0 0; color: var(--muted); line-height: 1.5; }
    .skeleton { min-height: 340px; padding: 24px; }
    .skeleton-line { height: 14px; margin-bottom: 13px; border-radius: 7px; background: var(--subtle); }
    .skeleton-line:nth-child(2) { width: 72%; height: 34px; }
    .skeleton-line:nth-child(3) { width: 92%; }
    .skeleton-line:nth-child(4) { width: 85%; }
    .skeleton-line:nth-child(5) { width: 64%; }
    @media (max-width: 480px) {
      body { padding: 4px; }
      .content { padding: 18px; }
      .meta-grid { grid-template-columns: 1fr; }
      .meta-item { border-right: 0; border-bottom: 1px solid var(--line); }
      .meta-item:last-child { border-bottom: 0; }
      .actions { grid-template-columns: 1fr; }
    }
    @media (prefers-reduced-motion: no-preference) {
      .evidence-panel { animation: reveal .16s ease-out; }
      @keyframes reveal { from { opacity: 0; transform: translateY(-4px); } }
    }
  </style>
</head>
<body>
  <main aria-live="polite">
    <article class="card" id="card">
      <div class="brand-line" aria-hidden="true"></div>
      <div class="skeleton" id="loading-state" aria-label="Loading GreyScienx analysis summary">
        <div class="skeleton-line"></div><div class="skeleton-line"></div><div class="skeleton-line"></div>
        <div class="skeleton-line"></div><div class="skeleton-line"></div>
      </div>
      <section class="content" id="complete-state" hidden>
        <header class="identity">
          <span class="brand">GreyScienx</span>
          <span class="status" id="evidence-status">Modelled</span>
        </header>
        <p class="eyebrow" id="series"></p>
        <h1 id="title"></h1>
        <p class="question" id="question"></p>
        <section class="finding" aria-labelledby="finding-label">
          <span class="finding-label" id="finding-label"></span>
          <blockquote id="finding-text"></blockquote>
        </section>
        <section class="meta-grid" aria-label="Finding context">
          <div class="meta-item"><span class="meta-label">Confidence</span><span class="meta-value" id="confidence"></span></div>
          <div class="meta-item"><span class="meta-label">Sensitivity</span><span class="meta-value" id="sensitivity"></span></div>
          <div class="meta-item"><span class="meta-label">Evidence</span><span class="meta-value" id="evidence-counts"></span></div>
        </section>
        <aside class="limitation" aria-labelledby="limitation-title">
          <strong id="limitation-title">Main limitation</strong><p id="limitation"></p>
        </aside>
        <section class="evidence-panel" id="evidence-panel" hidden aria-labelledby="evidence-heading">
          <h2 class="evidence-heading" id="evidence-heading">Evidence snapshot</h2>
          <div class="evidence-group"><span class="meta-label">Key assumptions</span><ul class="evidence-list" id="assumptions"></ul></div>
          <div class="evidence-group"><span class="meta-label">Modelled results</span><ul class="evidence-list" id="results"></ul></div>
          <div class="evidence-group"><span class="meta-label">Sources</span><ul class="evidence-list" id="sources"></ul></div>
        </section>
        <p class="freshness" id="freshness"></p>
        <footer class="actions">
          <button class="action action-primary" id="evidence-toggle" type="button" aria-controls="evidence-panel" aria-expanded="false">Explore evidence</button>
          <a class="action" id="open-study" href="#" target="_blank" rel="noopener noreferrer">Open in GreyScienx</a>
        </footer>
      </section>
      <section class="state" id="message-state" hidden><p class="eyebrow" id="state-eyebrow">GreyScienx</p><h1 id="state-title"></h1><p id="state-message"></p></section>
    </article>
  </main>
  <script>
    (function () {
      "use strict";
      var previewData = __GREYSCIENCX_PREVIEW_DATA__;
      var latestData = null;
      function isAllowedHost(hostname) {
        var host = String(hostname || "").toLowerCase();
        return host === "greyscienx.com" || host.endsWith(".greyscienx.com");
      }

      function byId(id) { return document.getElementById(id); }
      function text(id, value) { byId(id).textContent = value == null ? "—" : String(value); }
      function safeUrl(value) {
        try {
          var url = new URL(String(value));
          return url.protocol === "https:" && isAllowedHost(url.hostname) ? url.toString() : null;
        } catch (_) { return null; }
      }
      function clearList(id) { var list = byId(id); while (list.firstChild) list.removeChild(list.firstChild); return list; }
      function addLinkItem(list, title, detail, href) {
        var item = document.createElement("li");
        var validHref = safeUrl(href);
        var heading = validHref ? document.createElement("a") : document.createElement("strong");
        heading.textContent = title || "Untitled record";
        if (validHref) { heading.href = validHref; heading.target = "_blank"; heading.rel = "noopener noreferrer"; }
        item.appendChild(heading);
        if (detail) { var supporting = document.createElement("span"); supporting.textContent = detail; item.appendChild(supporting); }
        list.appendChild(item);
      }
      function renderList(id, items, mapper) {
        var list = clearList(id);
        if (!Array.isArray(items) || !items.length) {
          var empty = document.createElement("li"); empty.className = "empty-evidence"; empty.textContent = "No extracted records are published for this category."; list.appendChild(empty); return;
        }
        items.slice(0, 3).forEach(function (item) { mapper(list, item || {}); });
      }
      function notifyHeight() {
        if (window.openai && typeof window.openai.notifyIntrinsicHeight === "function") {
          window.openai.notifyIntrinsicHeight(document.documentElement.scrollHeight);
        }
      }
      function renderState(kind, title, message) {
        byId("loading-state").hidden = true;
        byId("complete-state").hidden = true;
        byId("message-state").hidden = false;
        text("state-eyebrow", kind === "permission_required" ? "Permission required" : "GreyScienx");
        text("state-title", title);
        text("state-message", message);
        notifyHeight();
      }
      function render(data) {
        latestData = data;
        if (!data || typeof data !== "object") { renderState("empty", "No analysis to display", "Ask ChatGPT to select a GreyScienx study and render its analysis summary."); return; }
        if (data.status && data.status !== "complete") {
          var states = {
            partial: ["Analysis is still arriving", "The available fields are incomplete. Wait for the remaining evidence."],
            empty: ["No matching finding", "Try a broader research question or open the GreyScienx research index."],
            error: ["The analysis could not be displayed", "Retry the tool call. If the problem continues, open the study on GreyScienx."],
            permission_required: ["Permission is required", "Reconnect the plugin or complete the requested authorization step."],
            stale: ["This record may be stale", "Open the study to check the latest published version."],
            cancelled: ["Analysis cancelled", "Ask ChatGPT to run the analysis again when you are ready."],
            loading: ["Loading analysis", "GreyScienx is preparing the evidence summary."],
          };
          var state = states[data.status] || states.error;
          renderState(data.status, state[0], state[1]); return;
        }
        var study = data.study || {};
        var finding = data.finding || {};
        var evidence = data.evidence || {};
        byId("loading-state").hidden = true;
        byId("message-state").hidden = true;
        byId("complete-state").hidden = false;
        text("evidence-status", finding.evidence_status || study.evidence_status || "Status unavailable");
        text("series", study.series || "GreyScienx research");
        text("title", study.title || "Analysis summary");
        text("question", study.question || "");
        text("finding-label", finding.label || "Finding");
        text("finding-text", finding.text || "No finding text was returned.");
        text("confidence", finding.confidence && finding.confidence.label ? finding.confidence.label : "Not numerically rated");
        text("sensitivity", finding.sensitivity ? String(finding.sensitivity) : "Not stated");
        text("evidence-counts", String(evidence.assumption_count || 0) + " assumptions · " + String(evidence.result_count || 0) + " results · " + String(evidence.source_count || 0) + " sources");
        text("limitation", finding.limitation || "No limitation was returned with this record.");
        text("freshness", data.freshness && data.freshness.label ? data.freshness.label : "Freshness unavailable");
        renderList("assumptions", evidence.assumptions, function (list, item) { addLinkItem(list, item.name, item.sensitivity ? "Sensitivity: " + item.sensitivity : "", item.href); });
        renderList("results", evidence.results, function (list, item) {
          var metric = item.value && item.unit ? item.value + " " + item.unit : item.scenario || "Modelled result";
          addLinkItem(list, item.statement, metric, item.href);
        });
        renderList("sources", evidence.sources, function (list, item) {
          var detail = [item.author_or_publisher, item.date].filter(Boolean).join(" · ");
          addLinkItem(list, item.title, detail, item.href);
        });
        var studyUrl = safeUrl(data.links && data.links.study);
        byId("open-study").href = studyUrl || "https://greyscienx.com/research";
        notifyHeight();
      }

      byId("evidence-toggle").addEventListener("click", function () {
        var panel = byId("evidence-panel");
        var opening = panel.hidden;
        panel.hidden = !opening;
        this.setAttribute("aria-expanded", String(opening));
        this.textContent = opening ? "Hide evidence" : "Explore evidence";
        notifyHeight();
      });
      byId("open-study").addEventListener("click", function (event) {
        var href = safeUrl(this.href);
        if (!href) { event.preventDefault(); return; }
        if (window.openai && typeof window.openai.openExternal === "function") {
          event.preventDefault(); window.openai.openExternal({ href: href });
        }
      });
      window.addEventListener("message", function (event) {
        if (event.source !== window.parent) return;
        var message = event.data;
        if (!message || message.jsonrpc !== "2.0") return;
        if (message.method === "ui/notifications/tool-result") render(message.params && message.params.structuredContent);
      }, { passive: true });
      window.addEventListener("openai:set_globals", function (event) {
        var globals = event.detail && event.detail.globals;
        if (globals && (globals.theme === "light" || globals.theme === "dark")) document.documentElement.dataset.theme = globals.theme;
        notifyHeight();
      }, { passive: true });
      var requestedTheme = new URLSearchParams(window.location.search).get("theme");
      if (requestedTheme === "light" || requestedTheme === "dark") document.documentElement.dataset.theme = requestedTheme;
      var initial = previewData || (window.openai && window.openai.toolOutput);
      if (initial) render(initial);
    })();
  </script>
</body>
</html>`;
