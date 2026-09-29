import {
  communityIndex,
  getProfile,
  listProfiles,
  validateCritique,
  validateFork,
  validateRevision,
  validateSubmission,
} from "./community";
import { SCHEMA_VERSION } from "./constants";
import { researchGraph } from "./graph";
import { compareStudies, findCounterarguments, modelSpec, reproducibilityPackage, traceClaim } from "./inquiry";
import { manuscriptResponse } from "./manuscripts";
import {
  getSeriesRecord,
  getClaim,
  getStudy,
  getTopicRecord,
  listSeriesRecords,
  listTopicRecords,
  searchResearch,
  studyCollection,
  studyRelated,
  studySources,
} from "./registry";

const PROTOCOL = "2025-03-26";

const READ_ONLY_TOOL_ANNOTATIONS = Object.freeze({
  readOnlyHint: true,
  openWorldHint: false,
  destructiveHint: false,
});

const tools = [
  {
    name: "search_research",
    description:
      "Search GreyScienx exploratory research, mathematical models, simulations, counterfactual studies, socioeconomic analyses, demographic models, and public-policy scenarios. Matches questions, claims, assumptions, results, and limitations, including related wording such as houses for housing. Use when the user asks whether a question has been modelled or wants the assumptions behind a modelled claim. Returns the study, its evidence status, the matching claim, and the key assumptions. It does not return a naked conclusion.",
    inputSchema: objectSchema({
      query: { type: "string", description: "Natural-language question or keywords." },
    }, ["query"]),
  },
  {
    name: "get_study",
    description:
      "Get one GreyScienx study by stable id (for example GSX:POP-009) or paper slug. Returns the question, catalog summary, epistemic status, manuscript link, and related studies. The summary is the catalog description, not a conditional finding.",
    inputSchema: objectSchema({
      study_id: { type: "string", description: "GSX id or paper slug." },
    }, ["study_id"]),
  },
  {
    name: "get_manuscript",
    description:
      "Get the complete Markdown manuscript for a GreyScienx study, or one named section. This is the full source text behind the PDF, not a generated summary. Omit section for the whole manuscript; use a heading title or heading slug for a section.",
    inputSchema: objectSchema({
      study_id: { type: "string", description: "GSX id or paper slug." },
      section: { type: "string", description: "Optional heading title or slug from the manuscript heading index." },
    }, ["study_id"]),
  },
  {
    name: "get_claim",
    description:
      "Get one claim from a GreyScienx study, including evidence status, dependencies, and limitations when that claim has been extracted. Until extraction, this returns an explicit pending state and no conclusion.",
    inputSchema: objectSchema({
      study_id: { type: "string", description: "GSX id or paper slug." },
      claim_id: { type: "string", description: "Optional claim id such as C19." },
    }, ["study_id"]),
  },
  {
    name: "get_assumptions",
    description:
      "Get the assumption objects for a GreyScienx study. Use when an answer depends on what the model assumed. Until extraction, this returns a pending state rather than invented parameters.",
    inputSchema: objectSchema({
      study_id: { type: "string", description: "GSX id or paper slug." },
    }, ["study_id"]),
  },
  {
    name: "get_results",
    description:
      "Get modelled results for a GreyScienx study, with evidence status. Until extraction, this returns a pending state and does not paraphrase the summary as a result.",
    inputSchema: objectSchema({
      study_id: { type: "string", description: "GSX id or paper slug." },
    }, ["study_id"]),
  },
  {
    name: "get_sources",
    description:
      "Get the manuscript and any extracted sources for a GreyScienx study. The manuscript PDF is available now.",
    inputSchema: objectSchema({
      study_id: { type: "string", description: "GSX id or paper slug." },
    }, ["study_id"]),
  },
  {
    name: "get_related_research",
    description:
      "Get other GreyScienx studies in the same series. Use when a question sits next to a study the user has already found.",
    inputSchema: objectSchema({
      study_id: { type: "string", description: "GSX id or paper slug." },
    }, ["study_id"]),
  },
  {
    name: "get_series",
    description:
      "Get a GreyScienx series, its question, and the studies in it. Omit series_slug to list every series.",
    inputSchema: objectSchema({
      series_slug: { type: "string", description: "Series slug, such as population-futures." },
    }, []),
  },
  {
    name: "get_topic",
    description:
      "Get a GreyScienx topic hub: definition, connected topics, and the studies filed under it. Omit topic_slug to list topics.",
    inputSchema: objectSchema({
      topic_slug: { type: "string", description: "Topic slug, such as housing or population-decline." },
    }, []),
  },
  {
    name: "get_research_graph",
    description:
      "Get the GreyScienx claim graph: claims depend on assumptions, cite modelled results, and are generated by a model. Pass a study id to limit the graph to one study. Omit it for the whole corpus. Edges are relationships, not extra findings.",
    inputSchema: objectSchema({
      study_id: { type: "string", description: "Optional GSX id or paper slug." },
    }, []),
  },
  {
    name: "compare_studies",
    description:
      "Compare two published GreyScienx studies. Returns each question, shared topics and geographies, assumption names used by both, and any published contradiction or qualification between them. The comparison does not create a new finding.",
    inputSchema: objectSchema({
      study_a: { type: "string", description: "GSX id or paper slug." },
      study_b: { type: "string", description: "GSX id or paper slug." },
    }, ["study_a", "study_b"]),
  },
  {
    name: "trace_claim",
    description:
      "Trace one GreyScienx claim to the assumptions it depends on, the modelled results it cites, the model that generated it, and its main limitation. Use this instead of quoting a conclusion alone.",
    inputSchema: objectSchema({
      study_id: { type: "string", description: "GSX id or paper slug." },
      claim_id: { type: "string", description: "Claim id such as C01." },
    }, ["study_id", "claim_id"]),
  },
  {
    name: "find_counterarguments",
    description:
      "Find published contradictions, qualifications, and the study's own limitations for a GreyScienx study or one of its claims. External critiques are included only when a person has published one.",
    inputSchema: objectSchema({
      study_id: { type: "string", description: "GSX id or paper slug." },
      claim_id: { type: "string", description: "Optional claim id such as C01." },
    }, ["study_id"]),
  },
  {
    name: "get_model_spec",
    description:
      "Get the registered model statements for a GreyScienx study. Statements come from the manuscript. An empty list means no model object is registered.",
    inputSchema: objectSchema({
      study_id: { type: "string", description: "GSX id or paper slug." },
    }, ["study_id"]),
  },
  {
    name: "get_reproducibility_package",
    description:
      "Get the reproducibility record for a GreyScienx study: whether code and data are recorded, the published files, and the reproduce page. A null repository URL means no separate public code repository is published.",
    inputSchema: objectSchema({
      study_id: { type: "string", description: "GSX id or paper slug." },
    }, ["study_id"]),
  },
  {
    name: "get_profile",
    description:
      "Get a GreyScienx author profile: name, affiliation, full biography, statements, absences, and the published studies attributed to that person. Omit profile_id to list profiles. Use when a citation needs the author record. Do not fill fields the profile marks as not published.",
    inputSchema: objectSchema({
      profile_id: { type: "string", description: "Profile slug or GSX:PROFILE id." },
    }, []),
  },
  {
    name: "get_community",
    description:
      "Get the GreyScienx community record: published profiles, the unpublished review queue, and the counts of published critiques, forks, and revisions. Published counts stay zero until a person publishes one. Use before claiming that a study has an external critique.",
    inputSchema: objectSchema({}, []),
  },
  {
    name: "validate_submission",
    description:
      "Check a proposed GreyScienx research object. Requires a question, research type, evidence status, and an explicit AI-assistance disclosure. The tool does not store or publish the object. A valid result still waits for human review.",
    inputSchema: objectSchema({
      object: { type: "object", description: "The proposed research object.", additionalProperties: true },
    }, ["object"]),
  },
  {
    name: "validate_critique",
    description:
      "Check a critique of a published GreyScienx study or claim. The critique names its target, type, argument, evidence, and proposed change. The tool does not store or publish the critique.",
    inputSchema: objectSchema({
      object: { type: "object", description: "The proposed critique.", additionalProperties: true },
    }, ["object"]),
  },
  {
    name: "validate_fork",
    description:
      "Check a fork of a published GreyScienx study. A fork records the parent study, what changed, the new results, and a conclusion with its evidence status and limitation. The tool does not store or publish the fork.",
    inputSchema: objectSchema({
      object: { type: "object", description: "The proposed fork.", additionalProperties: true },
    }, ["object"]),
  },
  {
    name: "validate_revision",
    description:
      "Check a proposed revision of a published GreyScienx study. It names the study, the version it starts from, and the change. The tool does not store or publish the revision.",
    inputSchema: objectSchema({
      object: { type: "object", description: "The proposed revision.", additionalProperties: true },
    }, ["object"]),
  },
].map((tool) => ({
  ...tool,
  annotations: READ_ONLY_TOOL_ANNOTATIONS,
}));

type RpcMessage = {
  jsonrpc?: string;
  id?: string | number | null;
  method?: string;
  params?: { name?: string; arguments?: Record<string, unknown> };
};

export async function handleMcpRequest(request: Request) {
  if (request.method === "GET") {
    return Response.json(discovery(), { headers: mcpHeaders() });
  }
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: mcpHeaders() });
  }
  if (request.method !== "POST") {
    return Response.json({ error: "method_not_allowed" }, { status: 405, headers: mcpHeaders() });
  }

  let payload: unknown;
  try {
    payload = await request.json();
  } catch {
    return rpcResponse(null, errorBody(-32700, "Parse error"), request, 400);
  }

  if (Array.isArray(payload)) {
    const responses = (await Promise.all(payload.map((message) => dispatch(message as RpcMessage)))).filter(
      (message) => message !== null,
    );
    if (responses.length === 0) return new Response(null, { status: 202, headers: mcpHeaders() });
    return deliver(responses, request);
  }

  const response = await dispatch(payload as RpcMessage);
  if (response === null) return new Response(null, { status: 202, headers: mcpHeaders() });
  return deliver(response, request);
}

export function discovery() {
  return {
    name: "GreyScienx",
    schema_version: SCHEMA_VERSION,
    protocol: "mcp",
    protocolVersion: PROTOCOL,
    transport: "stateless-json-rpc",
    version: "1.2.0",
    description:
      "Read-only research tools for GreyScienx studies, plus community validators that check an object and do not publish it. POST JSON-RPC messages to this URL. There is no hosted model.",
    tools: tools.map((tool) => ({
      name: tool.name,
      description: tool.description,
      annotations: tool.annotations,
    })),
  };
}

async function dispatch(message: RpcMessage) {
  if (!message || message.jsonrpc !== "2.0" || typeof message.method !== "string") {
    return rpc(message?.id ?? null, errorBody(-32600, "Invalid Request"));
  }
  const id = message.id ?? null;
  if (id === null && message.method.startsWith("notifications/")) return null;

  if (message.method === "initialize") {
    const requested = (message.params as { protocolVersion?: string } | undefined)?.protocolVersion;
    return rpc(id, {
      protocolVersion: typeof requested === "string" ? requested : PROTOCOL,
      capabilities: { tools: { listChanged: false } },
      serverInfo: { name: "GreyScienx", version: "1.2.0" },
      instructions:
        "GreyScienx tools return modelled research records with their evidence status. Read a claim with its assumptions and limitation. Community validators check an object and do not publish it.",
    });
  }
  if (message.method === "ping") return rpc(id, {});
  if (message.method === "tools/list") return rpc(id, { tools });
  if (message.method === "tools/call") return rpc(id, await callTool(message.params));
  return rpc(id, errorBody(-32601, "Method not found"));
}

async function callTool(params: RpcMessage["params"]) {
  const name = params?.name;
  const args = params?.arguments ?? {};
  const tool = tools.find((entry) => entry.name === name);
  if (!tool) {
    return { content: [{ type: "text", text: `Unknown tool ${name ?? ""}` }], isError: true };
  }
  try {
    const payload = await runTool(tool.name, args);
    return { content: [{ type: "text", text: JSON.stringify(payload, null, 2) }], isError: false };
  } catch (error) {
    const message = error instanceof Error ? error.message : "Tool failed";
    return { content: [{ type: "text", text: message }], isError: true };
  }
}

async function runTool(name: string, args: Record<string, unknown>) {
  if (name === "search_research") {
    const query = requiredString(args, "query");
    return { query, method: "hybrid_concept_vector_v1", results: searchResearch(query) };
  }
  if (name === "get_study") return requireStudy(args);
  if (name === "get_manuscript") {
    const study = requireStudy(args);
    const manuscript = manuscriptResponse(study.id, optionalString(args, "section"));
    if (!manuscript) throw new Error(`No manuscript section matches the request for ${study.id}.`);
    return manuscript;
  }
  if (name === "get_claim") return getClaim(requireStudy(args), optionalString(args, "claim_id"));
  if (name === "get_assumptions") return studyCollection(requireStudy(args), "assumptions");
  if (name === "get_results") return studyCollection(requireStudy(args), "results");
  if (name === "get_sources") return studySources(requireStudy(args));
  if (name === "get_related_research") return studyRelated(requireStudy(args));
  if (name === "get_series") {
    const slug = optionalString(args, "series_slug");
    if (!slug) return { series: listSeriesRecords() };
    const series = getSeriesRecord(slug);
    if (!series) throw new Error(`No GreyScienx series for ${slug}`);
    return series;
  }
  if (name === "get_research_graph") {
    const slug = optionalString(args, "study_id");
    if (!slug) return researchGraph();
    const study = getStudy(slug);
    if (!study) throw new Error(`No GreyScienx study for ${slug}`);
    return researchGraph(study.id);
  }
  if (name === "compare_studies") return compareStudies(requireStudyBy(args, "study_a"), requireStudyBy(args, "study_b"));
  if (name === "trace_claim") return traceClaim(requireStudy(args), requiredString(args, "claim_id"));
  if (name === "find_counterarguments") return findCounterarguments(requireStudy(args), optionalString(args, "claim_id"));
  if (name === "get_model_spec") return modelSpec(requireStudy(args));
  if (name === "get_reproducibility_package") return reproducibilityPackage(requireStudy(args));
  if (name === "get_topic") {
    const slug = optionalString(args, "topic_slug");
    if (!slug) return { topics: listTopicRecords() };
    const topic = getTopicRecord(slug);
    if (!topic) throw new Error(`No GreyScienx topic for ${slug}`);
    return topic;
  }
  if (name === "get_profile") {
    const slug = optionalString(args, "profile_id");
    if (!slug) return { profiles: listProfiles() };
    const profile = getProfile(slug);
    if (!profile) throw new Error(`No GreyScienx profile for ${slug}`);
    return profile;
  }
  if (name === "get_community") return communityIndex();
  if (name === "validate_submission") return validateSubmission(args.object);
  if (name === "validate_critique") return validateCritique(args.object);
  if (name === "validate_fork") return validateFork(args.object);
  if (name === "validate_revision") return validateRevision(args.object);
  throw new Error(`Unknown tool ${name}`);
}

function requireStudy(args: Record<string, unknown>) {
  return requireStudyBy(args, "study_id");
}

function requireStudyBy(args: Record<string, unknown>, key: string) {
  const study = getStudy(requiredString(args, key));
  if (!study) throw new Error(`No GreyScienx study matches ${key}.`);
  return study;
}

function requiredString(args: Record<string, unknown>, key: string) {
  const value = args[key];
  if (typeof value !== "string" || value.trim() === "") throw new Error(`Missing ${key}.`);
  return value.trim();
}

function optionalString(args: Record<string, unknown>, key: string) {
  const value = args[key];
  return typeof value === "string" && value.trim() !== "" ? value.trim() : null;
}

function objectSchema(properties: Record<string, unknown>, required: string[]) {
  return { type: "object", properties, required, additionalProperties: false };
}

function rpc(id: string | number | null, resultOrError: Record<string, unknown>) {
  if ("code" in resultOrError && "message" in resultOrError) {
    return { jsonrpc: "2.0", id, error: resultOrError };
  }
  return { jsonrpc: "2.0", id, result: resultOrError };
}

function errorBody(code: number, message: string) {
  return { code, message };
}

function rpcResponse(id: string | number | null, error: { code: number; message: string }, request: Request, status: number) {
  return deliver({ jsonrpc: "2.0", id, error }, request, status);
}

function deliver(body: unknown, request: Request, status = 200) {
  const accept = request.headers.get("accept") ?? "";
  if (accept.includes("text/event-stream") && !accept.includes("application/json")) {
    const events = (Array.isArray(body) ? body : [body])
      .map((message) => `event: message\ndata: ${JSON.stringify(message)}\n\n`)
      .join("");
    return new Response(events, {
      status,
      headers: { ...mcpHeaders(), "Content-Type": "text/event-stream; charset=utf-8" },
    });
  }
  return Response.json(body, { status, headers: mcpHeaders() });
}

function mcpHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Accept, MCP-Protocol-Version",
    "Cache-Control": "no-store",
  };
}
