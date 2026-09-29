import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";
import { papers } from "../catalog.ts";
import { getProfile, listProfiles, validateCritique, validateSubmission } from "./community.ts";
import { profileMarkdown } from "./profiles.ts";
import { holdForReview, listReviewQueue } from "./review-queue.ts";
import { discoveryMethods, matchesDiscovery, packageFor, seriesContext } from "./packages.ts";
import { handleMcpRequest } from "./mcp.ts";
import { studyMarkdown } from "./markdown.ts";
import { manuscriptFor, manuscriptResponse } from "./manuscripts.ts";
import { researchGraph } from "./graph.ts";
import { getClaim, getStudy, listTopicRecords, researchObjects, searchResearch } from "./registry.ts";

test("publishes one object per catalog paper", () => {
  assert.equal(researchObjects.length, 29);
  assert.equal(papers.length, 29);
  const slugs = new Set(researchObjects.map((study) => study.slug));
  for (const paper of papers) assert.equal(slugs.has(paper.slug), true);
  assert.equal(new Set(researchObjects.map((study) => study.id)).size, 29);
});

test("keeps published identifiers", () => {
  assert.equal(getStudy("the-first-three-years-advantage")?.id, "GSX:HH-002");
  assert.equal(getStudy("GSX:POP-004")?.title, "The Politics of an Ageing Electorate");
  assert.equal(getStudy("GSX:POP-009")?.slug, "how-to-shrink-a-country-without-breaking-it");
  assert.equal(getStudy("GSX:WPL-001")?.slug, "inherited-geography");
});

test("does not invent claim-level findings", () => {
  for (const study of researchObjects) {
    assert.equal("short_answer" in study, false);
    assert.equal(study.evidence_status, "modelled");
    assert.equal(study.peer_review_status, "none");
    assert.ok(study.sources.length >= 1);
    assert.ok(study.sources.some((source) => source.id === `${study.id}:PDF`));
    if (study.extraction_status === "full_text_claim_led") continue;
    assert.equal(study.extraction_status, "pending");
    assert.deepEqual(study.claims, []);
    assert.deepEqual(study.assumptions, []);
    assert.deepEqual(study.results, []);
    assert.deepEqual(study.models, []);
    assert.match(study.retrieval_note, /catalog description/);
  }
});

test("extracts a conditional claim for every published study", () => {
  assert.equal(researchObjects.length, 29);
  assert.equal(researchObjects.filter((study) => study.extraction_status === "full_text_claim_led").length, 29);
  const expected = [
    ["GSX:HH-001", /R3\.972 million/],
    ["GSX:HH-002", /R602,000/],
    ["GSX:POP-009", /54,000/],
    ["GSX:POP-012", /R1\.23 trillion/],
    ["GSX:SRD-001", /R253\.5 billion/],
    ["GSX:SRD-002", /R426\.9 billion/],
    ["GSX:IND-004", /sixteen hours/],
    ["GSX:WPL-001", /R1\.57 million/],
  ];
  for (const study of researchObjects) {
    assert.ok(study.claims.length >= 1);
    assert.ok(study.assumptions.length >= 1);
    assert.ok(study.results.length >= 1);
    assert.ok(study.claims.every((claim) => claim.main_limitation.length > 40));
    assert.ok(study.claims.every((claim) => claim.evidence_status === "modelled"));
    assert.ok(study.claims.every((claim) => claim.confidence === null));
    assert.ok(study.answer);
    assert.equal(study.answer.evidence_status, "modelled");
    assert.ok(study.answer.assumption_ids.length > 0);
    assert.ok(study.answer.result_ids.length > 0);
    assert.ok(study.assumptions.every((item) => item.href.includes(`/assumptions/${item.local_id}`)));
    assert.ok(study.results.every((item) => item.href.includes(`/results/${item.local_id}`)));
    assert.ok(study.models.every((item) => item.href.includes(`/models/${item.local_id}`)));
  }
  for (const [id, pattern] of expected) {
    assert.match(getStudy(id).claims[0].claim, pattern);
  }
});

test("extracts conditional claims for the first three years", () => {
  const study = getStudy("GSX:HH-002");
  assert.equal(study.extraction_status, "full_text_claim_led");
  assert.equal(study.claims.length, 4);
  const central = study.claims.find((claim) => claim.local_id === "C01");
  assert.match(central.claim, /R602,000/);
  assert.match(central.claim, /R3\.32 million/);
  assert.equal(central.evidence_status, "modelled");
  assert.equal(central.confidence, null);
  assert.ok(central.depends_on.includes("GSX:HH-002:A04"));
  assert.match(central.main_limitation, /not a forecast/);
});

test("connects claims to the assumptions they use", () => {
  const graph = researchGraph("GSX:HH-002");
  assert.ok(
    graph.edges.some(
      (edge) => edge.subject_id === "GSX:HH-002:C01" && edge.predicate === "depends_on" && edge.object_id.startsWith("GSX:HH-002:A"),
    ),
  );
  assert.equal(
    graph.edges.some((edge) => edge.object_id === "none" || edge.object_id === "none recorded"),
    false,
  );
  assert.ok(graph.nodes.some((node) => node.id === "GSX:HH-002" && node.type === "study"));
  const complete = researchGraph();
  assert.ok(complete.nodes.some((node) => node.type === "source"));
  assert.ok(complete.nodes.some((node) => node.type === "topic"));
  assert.ok(complete.edges.some((edge) => edge.predicate === "supported_by"));
  assert.ok(complete.edges.some((edge) => edge.predicate === "has_topic"));
});

test("gives every topic at least one study", () => {
  const topics = listTopicRecords();
  assert.ok(topics.length > 0);
  for (const topic of topics) {
    assert.ok(topic.study_count > 0);
    assert.ok(topic.definition.length > 0);
    assert.ok(Array.isArray(topic.related_questions));
    assert.ok(Array.isArray(topic.claims));
    assert.ok(Array.isArray(topic.assumptions));
    assert.ok(Array.isArray(topic.datasets));
  }
  assert.ok(topics.some((topic) => topic.claims.length > 0));
  assert.ok(topics.some((topic) => topic.assumptions.length > 0));
  assert.ok(topics.some((topic) => topic.datasets.length > 0));
  assert.ok(topics.some((topic) => topic.related_questions.length > 0));
});

test("search ranks the study that asks the question", () => {
  const parents = searchResearch("living with parents");
  assert.equal(parents[0]?.slug, "the-first-three-years-advantage");

  const retirement = searchResearch("retirement age");
  assert.equal(retirement[0]?.slug, "does-raising-the-retirement-age-actually-work");

  const housing = searchResearch("population decline housing").slice(0, 3).map((hit) => hit.slug);
  assert.ok(housing.includes("how-to-shrink-a-country-without-breaking-it"));

  assert.equal(searchResearch("   ").length, 0);
  assert.equal(parents[0]?.most_relevant_claim?.id, "GSX:HH-002:C01");
  assert.equal(parents[0]?.most_relevant_claim?.evidence_status, "modelled");
  assert.ok(parents[0]?.key_assumptions.length > 0);
  assert.equal(parents[0]?.evidence_status, "modelled");
  assert.equal(retirement[0]?.most_relevant_claim?.id, "GSX:POP-003:C01");

  const shock = searchResearch("shocked-year GDP");
  assert.equal(shock[0]?.slug, "extreme-fiscal-pressure");
  assert.equal(shock[0]?.key_assumptions[0]?.id, "GSX:POP-012:A01");

  const houses = searchResearch("where will people live if the nation ages").slice(0, 3).map((hit) => hit.slug);
  assert.ok(houses.includes("the-hundred-year-life"));
  const property = searchResearch("what happens to property values when population falls but people live longer")
    .slice(0, 3)
    .map((hit) => hit.slug);
  assert.ok(property.includes("how-to-shrink-a-country-without-breaking-it"));
  assert.ok(property.includes("the-hundred-year-life"));
});

test("markdown states the question without a conditional conclusion", () => {
  const study = getStudy("GSX:HH-002");
  assert.ok(study);
  const markdown = studyMarkdown(study);
  assert.match(markdown, /GSX:HH-002/);
  assert.match(markdown, /Primary question/);
  assert.match(markdown, /catalog summary/);
  assert.match(markdown, /R602,000/);
  assert.match(markdown, /not a forecast/);
  assert.match(markdown, /## Full manuscript/);
  assert.ok(markdown.length > manuscriptFor(study.id).content_markdown.length);
  assert.doesNotMatch(markdown, /short answer/i);
});

test("publishes a checksum-addressed full manuscript twin for every study", () => {
  for (const study of researchObjects) {
    const manuscript = manuscriptFor(study.id);
    assert.ok(manuscript);
    assert.equal(manuscript.study_id, study.id);
    assert.equal(manuscript.source_sha256, study.manuscript.source_sha256);
    assert.ok(manuscript.word_count > 250);
    assert.ok(manuscript.headings.length > 2);
    assert.ok(study.links.manuscript.endsWith(`/api/v1/research/${study.slug}/manuscript`));
    const section = manuscriptResponse(study.id, manuscript.headings[0].slug);
    assert.equal(section.section.slug, manuscript.headings[0].slug);
    assert.match(section.content_markdown, /^#/);
  }
});

test("mcp lists read-only tools and returns no naked claim", async () => {
  const listed = await post({ jsonrpc: "2.0", id: 1, method: "tools/list" });
  const names = listed.result.tools.map((tool) => tool.name);
  assert.deepEqual(names, [
    "search_research",
    "get_study",
    "get_manuscript",
    "get_claim",
    "get_assumptions",
    "get_results",
    "get_sources",
    "get_related_research",
    "get_series",
    "get_topic",
    "get_research_graph",
    "compare_studies",
    "trace_claim",
    "find_counterarguments",
    "get_model_spec",
    "get_reproducibility_package",
    "get_profile",
    "get_community",
    "validate_submission",
    "validate_critique",
    "validate_fork",
    "validate_revision",
  ]);

  const claim = await post({
    jsonrpc: "2.0",
    id: 2,
    method: "tools/call",
    params: { name: "get_claim", arguments: { study_id: "GSX:WPL-001", claim_id: "C19" } },
  });
  const body = JSON.parse(claim.result.content[0].text);
  assert.equal(body.claim, null);
  assert.equal(body.extraction_status, "not_found");
  assert.equal(claim.result.isError, false);

  const extracted = await post({
    jsonrpc: "2.0",
    id: 4,
    method: "tools/call",
    params: { name: "get_claim", arguments: { study_id: "GSX:HH-002", claim_id: "C01" } },
  });
  const extractedBody = JSON.parse(extracted.result.content[0].text);
  assert.equal(extractedBody.id, "GSX:HH-002:C01");
  assert.equal(extractedBody.evidence_status, "modelled");
  assert.ok(extractedBody.depends_on.length > 0);
  assert.match(extractedBody.main_limitation, /not a forecast/);
  assert.equal(getClaim(getStudy("GSX:HH-002"), "C19").claim, null);

  const found = await post({
    jsonrpc: "2.0",
    id: 3,
    method: "tools/call",
    params: { name: "search_research", arguments: { query: "retirement age" } },
  });
  const results = JSON.parse(found.result.content[0].text);
  assert.equal(results.results[0].slug, "does-raising-the-retirement-age-actually-work");

  const manuscript = await post({
    jsonrpc: "2.0",
    id: 31,
    method: "tools/call",
    params: { name: "get_manuscript", arguments: { study_id: "GSX:HH-001", section: "part-i-the-economic-foundation" } },
  });
  const manuscriptBody = JSON.parse(manuscript.result.content[0].text);
  assert.equal(manuscriptBody.study_id, "GSX:HH-001");
  assert.equal(manuscriptBody.section.slug, "part-i-the-economic-foundation");
  assert.match(manuscriptBody.content_markdown, /cohabitation dividend/i);

  const traced = await post({
    jsonrpc: "2.0",
    id: 5,
    method: "tools/call",
    params: { name: "trace_claim", arguments: { study_id: "GSX:HH-002", claim_id: "C01" } },
  });
  const trace = JSON.parse(traced.result.content[0].text);
  assert.equal(trace.claim.id, "GSX:HH-002:C01");
  assert.equal(trace.evidence_status, "modelled");
  assert.ok(trace.assumptions.length > 0);
  assert.ok(trace.results.length > 0);
  assert.ok(trace.model);
  assert.match(trace.main_limitation, /not a forecast/);

  const missing = await post({
    jsonrpc: "2.0",
    id: 6,
    method: "tools/call",
    params: { name: "trace_claim", arguments: { study_id: "GSX:HH-002", claim_id: "C19" } },
  });
  assert.equal(JSON.parse(missing.result.content[0].text).claim, null);

  const compared = await post({
    jsonrpc: "2.0",
    id: 7,
    method: "tools/call",
    params: { name: "compare_studies", arguments: { study_a: "GSX:HH-001", study_b: "GSX:HH-002" } },
  });
  const comparison = JSON.parse(compared.result.content[0].text);
  assert.equal(comparison.studies.length, 2);
  assert.ok(comparison.shared_topics.includes("cohabitation"));

  const counters = await post({
    jsonrpc: "2.0",
    id: 8,
    method: "tools/call",
    params: { name: "find_counterarguments", arguments: { study_id: "GSX:HH-002", claim_id: "C01" } },
  });
  const counter = JSON.parse(counters.result.content[0].text);
  assert.deepEqual(counter.external_critiques, []);
  assert.equal(counter.limitations.length, 1);
  assert.match(counter.limitations[0].main_limitation, /not a forecast/);

  const model = await post({
    jsonrpc: "2.0",
    id: 9,
    method: "tools/call",
    params: { name: "get_model_spec", arguments: { study_id: "GSX:HH-002" } },
  });
  assert.ok(JSON.parse(model.result.content[0].text).models.length > 0);

  const reproduced = await post({
    jsonrpc: "2.0",
    id: 10,
    method: "tools/call",
    params: { name: "get_reproducibility_package", arguments: { study_id: "GSX:HH-002" } },
  });
  const pack = JSON.parse(reproduced.result.content[0].text);
  assert.equal(pack.reproducibility.code_available, true);
  assert.equal(pack.reproducibility.repository_url, null);
  assert.ok(pack.files.some((file) => file.path.endsWith("model.py")));
});

test("publishes the author profile and keeps community objects empty", async () => {
  const profiles = listProfiles();
  assert.equal(profiles.length, 1);
  assert.equal(profiles[0].id, "GSX:PROFILE:pakang-senosha");
  assert.equal(profiles[0].study_count, 29);
  assert.equal(profiles[0].profile_schema, "GreyProfile 1.0");
  assert.equal(getProfile("GSX:PROFILE:pakang-senosha")?.name, "Pakang Senosha");
  const founder = getProfile("pakang-senosha");
  assert.equal(founder.biography.sections.length, 8);
  assert.equal(founder.education[0].status, "student");
  assert.equal(founder.education[1].institution, "Nelson Mandela University");
  assert.equal(founder.location, "Roodepoort, South Africa");
  assert.equal(founder.corpus.series.length, 6);
  assert.equal(founder.corpus.series.reduce((sum, series) => sum + series.studies.length, 0), 29);
  assert.ok(founder.absences.some((item) => item.field === "msc_completion"));
  assert.equal(founder.external_writing.length, 0);
  assert.equal(JSON.stringify(founder).toLowerCase().includes("medium"), false);
  assert.ok(founder.experience.some((item) => item.organisation === "Lancet Flora"));
  assert.ok(founder.portfolio_work.some((item) => item.title === "Bantuity Ecosystem"));
  assert.match(profileMarkdown(founder), /GSX:PROFILE:pakang-senosha/);
  assert.match(profileMarkdown(founder), /What this biography refuses to invent/);

  const valid = validateSubmission({
    title: "A modelled note on household formation",
    primary_question: "What does a three-year delay change in this scenario?",
    research_type: "counterfactual",
    evidence_status: "modelled",
    ai_assistance: { disclosure: "Drafting assistance is disclosed. No peer review is claimed." },
  });
  assert.equal(valid.valid, true);
  assert.equal(valid.accepted, false);
  assert.equal(valid.status, "not_stored");

  const previousInbox = process.env.GREYSCIENX_REVIEW_INBOX;
  const inboxDir = mkdtempSync(path.join(tmpdir(), "gsx-review-"));
  process.env.GREYSCIENX_REVIEW_INBOX = path.join(inboxDir, "inbox.jsonl");
  try {
    const queued = await holdForReview(valid, {
      title: "A modelled note on household formation",
      primary_question: "What does a three-year delay change in this scenario?",
      research_type: "counterfactual",
      evidence_status: "modelled",
      ai_assistance: { disclosure: "Drafting assistance is disclosed. No peer review is claimed." },
    });
    assert.equal(queued.status, "queued");
    assert.equal(queued.accepted, false);
    assert.match(queued.id ?? "", /^GSX:REVIEW:/);
    assert.equal((await listReviewQueue()).some((item) => item.id === queued.id), true);
    assert.equal((await listReviewQueue()).length, 1);
  } finally {
    if (previousInbox === undefined) delete process.env.GREYSCIENX_REVIEW_INBOX;
    else process.env.GREYSCIENX_REVIEW_INBOX = previousInbox;
    rmSync(inboxDir, { recursive: true, force: true });
  }

  const rejected = validateSubmission({
    title: "Already published",
    primary_question: "Can this replace a published study?",
    research_type: "exploratory_simulation",
    evidence_status: "modelled",
    id: "GSX:HH-002",
    status: "published",
    peer_review_status: "peer_reviewed",
    ai_assistance: "Assistance is disclosed in this sentence.",
  });
  assert.equal(rejected.valid, false);
  assert.equal((await holdForReview(rejected, { title: "no" })).status, "not_stored");
  assert.ok(rejected.errors.some((error) => error.includes("already belongs")));
  assert.ok(rejected.errors.some((error) => error.includes("peer_review_status")));

  const critique = validateCritique({
    target_study: "GSX:HH-002",
    target_claim: "C01",
    author: "Reviewer",
    critique_type: "assumption",
    argument: "The middle-salary path is too narrow to carry the lifetime wealth claim on its own.",
    evidence: "The manuscript states the scenario.",
    proposed_change: "Report the path as one scenario.",
  });
  assert.equal(critique.valid, true);
  assert.equal(critique.accepted, false);

  const missingClaim = validateCritique({
    target_study: "GSX:HH-002",
    target_claim: "C19",
    author: "Reviewer",
    critique_type: "scope",
    argument: "This critique names a claim the study has not published.",
    evidence: "The claim list omits C19.",
    proposed_change: "Leave the claim unpublished.",
  });
  assert.equal(missingClaim.valid, false);

  const profile = await post({
    jsonrpc: "2.0",
    id: 6,
    method: "tools/call",
    params: { name: "get_profile", arguments: { profile_id: "pakang-senosha" } },
  });
  const profileBody = JSON.parse(profile.result.content[0].text);
  assert.equal(profileBody.study_count, 29);
  assert.equal(profile.result.isError, false);
});

test("filters the archive by recorded method and code", () => {
  assert.ok(discoveryMethods().includes("Python 3"));
  assert.equal(matchesDiscovery("GSX:HH-001", "Python 3", ""), true);
  assert.equal(matchesDiscovery("GSX:HH-001", "", "unrecorded"), false);
  assert.equal(matchesDiscovery("GSX:HH-002", "Python 3", "recorded"), true);
  assert.equal(matchesDiscovery("GSX:HH-002", "", "unrecorded"), false);
  const recorded = searchResearch("household").filter((hit) => matchesDiscovery(hit.id, "Python 3", "recorded"));
  assert.ok(recorded.some((hit) => hit.id === "GSX:HH-001"));
  assert.ok(recorded.some((hit) => hit.id === "GSX:HH-002"));
});

test("publishes a dataset and reproducibility record for every study", () => {
  for (const study of researchObjects) {
    const pack = packageFor(study.id);
    assert.ok(pack);
    assert.ok(pack.datasets.length >= 1);
    assert.equal(typeof pack.reproducibility.code_available, "boolean");
  }
  assert.equal(packageFor("GSX:HH-001").reproducibility.code_available, true);
  assert.equal(packageFor("GSX:HH-002").reproducibility.code_available, true);
  assert.equal(packageFor("GSX:HH-002").reproducibility.repository_url, null);
  assert.ok(packageFor("GSX:HH-001").files.some((file) => file.path.endsWith("expanded_lifetime_model.py")));
  assert.ok(packageFor("GSX:HH-001").files.some((file) => file.path.endsWith("model_results.json")));
  assert.ok(packageFor("GSX:HH-002").files.some((file) => file.path.endsWith("model.py")));
  assert.ok(packageFor("GSX:HH-002").files.every((file) => file.sha256.length === 64));
  const series = seriesContext("household-economics");
  assert.ok(series.unresolved_questions.length >= 2);
  assert.equal(series.contradictions.length, 0);
});

async function post(message) {
  const response = await handleMcpRequest(
    new Request("https://greyscienx.com/mcp", {
      method: "POST",
      headers: { "content-type": "application/json", accept: "application/json" },
      body: JSON.stringify(message),
    }),
  );
  assert.equal(response.status, 200);
  return response.json();
}
