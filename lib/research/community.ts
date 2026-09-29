import { researchers } from "../catalog";
import { publicUrl } from "../urls";
import { listReviewQueue } from "./review-queue";
import { profileForm } from "./profiles";
import { getStudy, researchObjects } from "./registry";
import published from "../../research/community/published.json" with { type: "json" };

export const COMMUNITY_VERSION = "GreyCommunity 1.0";

export const critiqueTypes = [
  "assumption",
  "method",
  "data",
  "interpretation",
  "mathematics",
  "source",
  "reproducibility",
  "scope",
] as const;

const evidenceValues = new Set(["modelled", "exploratory", "observational", "qualitative"]);
const researchTypes = new Set(["exploratory_simulation", "counterfactual"]);

export type CommunityObjectType = "submission" | "critique" | "fork" | "revision";

export type ReviewPacket = {
  schema_version: typeof COMMUNITY_VERSION;
  object_type: CommunityObjectType;
  status: "not_stored" | "queued";
  accepted: false;
  review: "human_review_required";
  valid: boolean;
  errors: string[];
  warnings: string[];
  id?: string;
  received_at?: string;
};

const publicObjects = {
  critiques: published.critiques as Array<Record<string, unknown>>,
  forks: published.forks as Array<Record<string, unknown>>,
  revisions: published.revisions as Array<Record<string, unknown>>,
};

export function listProfiles() {
  return researchers.map((researcher) => {
    const studies = researchObjects.filter((study) =>
      study.authors.some((author) => author.slug === researcher.slug),
    );
    const form = profileForm(researcher.slug);
    return {
      schema_version: COMMUNITY_VERSION,
      profile_schema: form?.target_object_schema ?? null,
      id: `GSX:PROFILE:${researcher.slug}`,
      slug: researcher.slug,
      name: researcher.name,
      role: researcher.role,
      affiliation: researcher.affiliation,
      location: researcher.location,
      bio: researcher.bio,
      email: researcher.email,
      study_count: studies.length,
      studies: studies.map((study) => ({
        id: study.id,
        slug: study.slug,
        title: study.title,
        series_slug: study.series_slug,
        series_title: study.series_title,
        summary: study.summary,
        href: study.links.html,
      })),
      external_links: researcher.links,
      biography: form?.biography ?? null,
      roles: form?.roles ?? [],
      education: form?.education ?? [],
      places: form?.locations ?? [],
      external_profiles: form?.external_profiles ?? [],
      external_writing: form?.external_writing ?? [],
      experience: form?.experience ?? [],
      certifications: form?.certifications ?? [],
      portfolio_work: form?.portfolio_work ?? [],
      unreviewed_public_code: form?.unreviewed_public_code ?? [],
      statements: form?.statements ?? [],
      epistemic_positions: form?.epistemic_positions ?? [],
      absences: form?.absences ?? [],
      corpus: form?.corpus ?? null,
      links: {
        html: publicUrl(`/about/${researcher.slug}`),
        index: publicUrl("/researchers"),
        json: publicUrl(`/api/v1/profiles/${researcher.slug}`),
      },
    };
  });
}

export function getProfile(idOrSlug: string) {
  const key = decodeURIComponent(idOrSlug).trim().toLowerCase();
  return (
    listProfiles().find((profile) => profile.slug.toLowerCase() === key || profile.id.toLowerCase() === key) ??
    null
  );
}

export function communityContract() {
  return {
    schema_version: COMMUNITY_VERSION,
    publication_rule:
      "A valid POST is kept in the review queue and stays unpublished. The public record changes when a person publishes it.",
    objects: {
      profile: [
        "id",
        "name",
        "affiliation",
        "bio",
        "biography",
        "roles",
        "education",
        "statements",
        "absences",
        "experience",
        "portfolio_work",
        "studies",
      ],
      critique: [
        "target_study",
        "target_claim",
        "author",
        "critique_type",
        "argument",
        "evidence",
        "proposed_change",
        "status",
        "response",
      ],
      fork: [
        "parent_study",
        "changed_assumptions",
        "changed_data",
        "changed_methods",
        "new_results",
        "new_conclusion",
        "evidence_status",
        "main_limitation",
      ],
      revision: ["target_study", "version_from", "change", "status"],
      submission: ["title", "primary_question", "research_type", "evidence_status", "ai_assistance"],
    },
    critique_types: critiqueTypes,
  };
}

export async function communityIndex() {
  const profiles = listProfiles();
  const publishedReviewIds = new Set(
    [...publicObjects.critiques, ...publicObjects.forks, ...publicObjects.revisions]
      .map((item) => item.review_id)
      .filter((id): id is string => typeof id === "string"),
  );
  const reviewQueue = (await listReviewQueue()).filter((item) => !publishedReviewIds.has(item.id));
  return {
    ...communityContract(),
    counts: {
      profiles: profiles.length,
      critiques: publicObjects.critiques.length,
      forks: publicObjects.forks.length,
      revisions: publicObjects.revisions.length,
      review_queue: reviewQueue.length,
    },
    review_queue: reviewQueue,
    profiles: profiles.map((profile) => ({
      id: profile.id,
      slug: profile.slug,
      name: profile.name,
      study_count: profile.study_count,
      href: profile.links.html,
    })),
    critiques: publicObjects.critiques,
    forks: publicObjects.forks,
    revisions: publicObjects.revisions,
  };
}

export function studyCommunity(studyId: string, kind: "critiques" | "forks" | "revisions") {
  const field = kind === "forks" ? "parent_study" : "target_study";
  const records = publicObjects[kind].filter((item) => {
    const target = item[field];
    const study = typeof target === "string" ? getStudy(target) : null;
    return study?.id === studyId;
  });
  return {
    schema_version: COMMUNITY_VERSION,
    study_id: studyId,
    count: records.length,
    note: records.length ? `Published ${kind}: ${records.length}.` : `Published ${kind}: none.`,
    [kind]: records,
  };
}

export function invalidJson(objectType: CommunityObjectType): ReviewPacket {
  return packet(objectType, ["Request body must be JSON."], []);
}

export function validateSubmission(body: unknown): ReviewPacket {
  const errors: string[] = [];
  const warnings: string[] = [];
  if (!isRecord(body)) return packet("submission", ["Request body must be a JSON object."], []);
  requireText(body, "title", 8, "title must name the study.", errors);
  requireText(body, "primary_question", 12, "primary_question must state the question the study asks.", errors);
  if (!researchTypes.has(text(body, "research_type"))) {
    errors.push("research_type must be exploratory_simulation or counterfactual.");
  }
  requireEvidence(body, errors);
  requireAssistance(body, errors);
  const id = text(body, "id");
  if (id) {
    if (!/^GSX:[A-Z]{2,5}-\d{3}$/.test(id)) errors.push("id must look like GSX:POP-013.");
    else if (getStudy(id)) errors.push("id already belongs to a published study.");
  } else {
    warnings.push("No stable id was supplied. Review assigns one.");
  }
  if (text(body, "status") === "published") errors.push("status cannot be published. Review publishes a study.");
  const peer = text(body, "peer_review_status");
  if (peer && peer !== "none") {
    errors.push("peer_review_status must be none. A submission does not establish peer review.");
  }
  if ("claims" in body) checkClaims(body.claims, errors);
  return packet("submission", errors, warnings);
}

export function validateCritique(body: unknown): ReviewPacket {
  const errors: string[] = [];
  const warnings: string[] = [];
  if (!isRecord(body)) return packet("critique", ["Request body must be a JSON object."], []);
  const study = publishedStudy(text(body, "target_study"), "target_study", errors);
  const claimId = text(body, "target_claim");
  if (study && claimId) {
    const found = study.claims.some(
      (claim) => claim.local_id.toLowerCase() === claimId.toLowerCase() || claim.id.toLowerCase() === claimId.toLowerCase(),
    );
    if (!found) errors.push("target_claim is not a published claim on that study.");
  } else if (study && !claimId) {
    warnings.push("No target_claim was supplied. The critique addresses the study.");
  }
  requireText(body, "author", 2, "author must name the person or agent responsible for the critique.", errors);
  if (!critiqueTypes.includes(text(body, "critique_type") as (typeof critiqueTypes)[number])) {
    errors.push(`critique_type must be one of: ${critiqueTypes.join(", ")}.`);
  }
  requireText(body, "argument", 40, "argument must state the criticism.", errors);
  requireText(body, "evidence", 8, "evidence must name the support for the criticism, or state that none is supplied.", errors);
  requireText(body, "proposed_change", 8, "proposed_change must say what should change.", errors);
  if (text(body, "status") === "published") errors.push("status cannot be published. Review publishes a critique.");
  return packet("critique", errors, warnings);
}

export function validateFork(body: unknown): ReviewPacket {
  const errors: string[] = [];
  const warnings: string[] = [];
  if (!isRecord(body)) return packet("fork", ["Request body must be a JSON object."], []);
  publishedStudy(text(body, "parent_study"), "parent_study", errors);
  if (!Array.isArray(body.changed_assumptions)) errors.push("changed_assumptions must be an array.");
  else if (body.changed_assumptions.length === 0) warnings.push("changed_assumptions is empty.");
  if (!Array.isArray(body.changed_data)) errors.push("changed_data must be an array.");
  requireText(body, "changed_methods", 12, "changed_methods must describe the change in method.", errors);
  requireText(body, "new_results", 12, "new_results must describe the new modelled results.", errors);
  requireText(body, "new_conclusion", 20, "new_conclusion is required.", errors);
  requireEvidence(body, errors);
  requireText(body, "main_limitation", 40, "main_limitation must travel with the new conclusion.", errors);
  if (text(body, "status") === "published") errors.push("status cannot be published. Review publishes a fork.");
  return packet("fork", errors, warnings);
}

export function validateRevision(body: unknown): ReviewPacket {
  const errors: string[] = [];
  const warnings: string[] = [];
  if (!isRecord(body)) return packet("revision", ["Request body must be a JSON object."], []);
  publishedStudy(text(body, "target_study"), "target_study", errors);
  requireText(body, "version_from", 1, "version_from must name the version under revision.", errors);
  requireText(body, "change", 20, "change must describe the revision.", errors);
  if (text(body, "status") === "published") errors.push("status cannot be published. Review publishes a revision.");
  return packet("revision", errors, warnings);
}

function publishedStudy(id: string, field: string, errors: string[]) {
  if (!id) {
    errors.push(`${field} must name a published GreyScienx study.`);
    return null;
  }
  const study = getStudy(id);
  if (!study) errors.push(`${field} does not match a published GreyScienx study.`);
  return study;
}

function checkClaims(value: unknown, errors: string[]) {
  if (!Array.isArray(value)) {
    errors.push("claims must be an array.");
    return;
  }
  value.forEach((claim, index) => {
    if (!isRecord(claim)) {
      errors.push(`claims[${index}] must be an object.`);
      return;
    }
    if (text(claim, "claim").length < 12) errors.push(`claims[${index}].claim is missing.`);
    if (!text(claim, "evidence_status")) errors.push(`claims[${index}] needs evidence_status.`);
    if (text(claim, "main_limitation").length < 40) {
      errors.push(`claims[${index}].main_limitation must travel with the claim.`);
    }
    if (!Array.isArray(claim.depends_on)) errors.push(`claims[${index}].depends_on must name the assumptions it uses.`);
  });
}

function requireAssistance(body: Record<string, unknown>, errors: string[]) {
  const ai = body.ai_assistance;
  if (typeof ai === "string") {
    if (ai.trim().length < 12) errors.push("ai_assistance must state the assistance used, including none.");
    return;
  }
  if (isRecord(ai)) {
    if (text(ai, "disclosure").length < 12) {
      errors.push("ai_assistance.disclosure must state the assistance used, including none.");
    }
    return;
  }
  errors.push("ai_assistance is required.");
}

function requireEvidence(body: Record<string, unknown>, errors: string[]) {
  if (!evidenceValues.has(text(body, "evidence_status"))) {
    errors.push("evidence_status must be modelled, exploratory, observational, or qualitative.");
  }
}

function requireText(body: Record<string, unknown>, key: string, min: number, message: string, errors: string[]) {
  if (text(body, key).length < min) errors.push(message);
}

function packet(objectType: CommunityObjectType, errors: string[], warnings: string[]): ReviewPacket {
  return {
    schema_version: COMMUNITY_VERSION,
    object_type: objectType,
    status: "not_stored",
    accepted: false,
    review: "human_review_required",
    valid: errors.length === 0,
    errors,
    warnings,
  };
}

function text(record: Record<string, unknown>, key: string) {
  const value = record[key];
  return typeof value === "string" ? value.trim() : "";
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
