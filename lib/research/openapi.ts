import { site } from "../site";
import { SCHEMA_VERSION } from "./constants";

const origin = `https://${site.domain}`;

export function openApiDocument() {
  return {
    openapi: "3.1.0",
    info: {
      title: "GreyScienx Research API",
      version: "1.2.0",
      summary: "Read-only study records, plus validators that do not publish community objects.",
      description:
        `${SCHEMA_VERSION}. Returns published studies, complete Markdown manuscripts, series, topics, claims, assumptions, results, models, sources, datasets, and concept-aware search over the research corpus. Community routes expose profiles, published community objects, and the unpublished review queue. Submission, critique, fork, and revision POST routes validate an object, keep a valid one for review, and do not publish it automatically. This API does not host a model.`,
    },
    servers: [{ url: origin }],
    paths: {
      "/api/v1/research": {
        get: operation("List published studies", "Returns a summary of every published research object.", {
          "200": jsonResponse("Study list"),
        }),
      },
      "/api/v1/research/{id}": {
        get: operation(
          "Get one study",
          "Accepts a paper slug or a stable id such as GSX:POP-009.",
          { "200": jsonResponse("Research object"), "404": jsonResponse("Not found") },
          [idParam()],
        ),
      },
      "/api/v1/research/{id}/manuscript": {
        get: operation(
          "Get the full manuscript",
          "Returns the complete source manuscript as Markdown plus its checksum and heading index. Set Accept to text/markdown for a raw Markdown response. An optional section query accepts a heading title or slug.",
          {
            "200": {
              description: "Full manuscript or selected section",
              content: {
                "application/json": { schema: { type: "object" } },
                "text/markdown": { schema: { type: "string" } },
              },
            },
            "404": jsonResponse("Study or section not found"),
          },
          [
            idParam(),
            {
              name: "section",
              in: "query",
              required: false,
              schema: { type: "string" },
              description: "Heading title or stable heading slug.",
            },
          ],
        ),
      },
      "/api/v1/research/{id}/claims": collectionPath("claims"),
      "/api/v1/research/{id}/claims/{claimId}": {
        get: operation(
          "Get one claim",
          "Returns one extracted claim with its evidence status, dependencies, and main limitation. Unknown or unextracted claim ids return no conclusion.",
          { "200": jsonResponse("Claim"), "404": jsonResponse("Not found") },
          [idParam(), { name: "claimId", in: "path", required: true, schema: { type: "string" }, description: "Local claim id such as C01." }],
        ),
      },
      "/api/v1/research/{id}/assumptions": collectionPath("assumptions"),
      "/api/v1/research/{id}/assumptions/{objectId}": subobjectPath("assumption"),
      "/api/v1/research/{id}/datasets": {
        get: operation(
          "Get datasets",
          "Returns the dataset record and reproducibility flags for one study. The manuscript is the published file.",
          { "200": jsonResponse("Datasets"), "404": jsonResponse("Not found") },
          [idParam()],
        ),
      },
      "/api/v1/research/{id}/results": collectionPath("results"),
      "/api/v1/research/{id}/results/{objectId}": subobjectPath("result"),
      "/api/v1/research/{id}/models": collectionPath("models"),
      "/api/v1/research/{id}/models/{objectId}": subobjectPath("model"),
      "/api/v1/research/{id}/sources": collectionPath("sources"),
      "/api/v1/research/{id}/related": collectionPath("related studies"),
      "/api/v1/research/{id}/versions": collectionPath("version history"),
      "/api/v1/research/{id}/versions/{objectId}": subobjectPath("version"),
      "/api/v1/series": {
        get: operation("List series", "Returns each research series and its question.", {
          "200": jsonResponse("Series list"),
        }),
      },
      "/api/v1/series/{slug}": {
        get: operation("Get one series", "Returns the series question and its studies.", {
          "200": jsonResponse("Series"),
          "404": jsonResponse("Not found"),
        }, [slugParam("Series slug")]),
      },
      "/api/v1/topics": {
        get: operation("List topics", "Returns topic definitions that have at least one study.", {
          "200": jsonResponse("Topic list"),
        }),
      },
      "/api/v1/topics/{slug}": {
        get: operation("Get one topic", "Returns the definition, connected topics, and studies.", {
          "200": jsonResponse("Topic"),
          "404": jsonResponse("Not found"),
        }, [slugParam("Topic slug")]),
      },
      "/api/v1/graph": {
        get: operation(
          "Get the research graph",
          "Claims, assumptions, results, models, and studies, with the predicate that connects each pair.",
          { "200": jsonResponse("Research graph") },
        ),
      },
      "/api/v1/research/{id}/graph": {
        get: operation(
          "Get one study graph",
          "The claim graph for a single study, including its series membership.",
          { "200": jsonResponse("Study graph"), "404": jsonResponse("Not found") },
          [idParam()],
        ),
      },
      "/feed.xml": {
        get: operation("Study feed", "RSS 2.0 list of published studies and their questions.", {
          "200": { description: "RSS feed", content: { "application/rss+xml": { schema: { type: "string" } } } },
        }),
      },
      "/api/v1/community": {
        get: operation(
          "Get the community record",
          "Profiles plus the published critiques, forks, and revisions. Those three lists are empty until review publishes one.",
          { "200": jsonResponse("Community record") },
        ),
      },
      "/api/v1/profiles": {
        get: operation("List author profiles", "Returns each published author, the semantic-twin biography, and the studies attributed to them.", {
          "200": jsonResponse("Profile list"),
        }),
      },
      "/api/v1/profiles/{slug}": {
        get: operation("Get one profile", "Accepts a profile slug or a GSX:PROFILE id. A compiled profile includes the biography, statements, education status, and explicit absences.", {
          "200": jsonResponse("Profile"),
          "404": jsonResponse("Not found"),
        }, [slugParam("Profile slug")]),
      },
      "/api/v1/critiques": reviewPath("critique", "Critiques"),
      "/api/v1/forks": reviewPath("fork", "Forks"),
      "/api/v1/revisions": reviewPath("revision", "Revisions"),
      "/api/v1/submissions": {
        get: operation(
          "Describe submission review",
          "Lists unpublished submissions waiting for review.",
          { "200": jsonResponse("Submission review") },
        ),
        post: operation(
          "Validate a submission",
          "Checks the question, research type, evidence status, and AI-assistance disclosure. A valid object is kept for human review and is not published.",
          { "200": jsonResponse("Valid, unpublished"), "400": jsonResponse("Invalid JSON"), "422": jsonResponse("Validation errors") },
        ),
      },
      "/api/v1/research/{id}/critiques": studyCommunityPath("critiques"),
      "/api/v1/research/{id}/forks": studyCommunityPath("forks"),
      "/api/v1/research/{id}/revisions": studyCommunityPath("revisions"),
      "/api/v1/search": {
        get: operation(
          "Search studies",
          "Hybrid concept-vector search over titles, questions, claims, assumptions, results, limitations, and identifiers. A transparent local concept map and sparse-vector similarity handle related wording without sending the query to an external model. Optional filters limit hits by recorded software or code availability. Results include evidence status, the most relevant extracted claim, and the assumptions that matched or that the claim depends on.",
          { "200": jsonResponse("Search results") },
          [
            {
              name: "q",
              in: "query",
              required: true,
              schema: { type: "string" },
              description: "A question or keywords, such as living with parents or retirement age.",
            },
            {
              name: "method",
              in: "query",
              required: false,
              schema: { type: "string" },
              description: "Recorded software, such as Python 3.",
            },
            {
              name: "code",
              in: "query",
              required: false,
              schema: { type: "string", enum: ["recorded", "unrecorded"] },
              description: "Whether the study records code.",
            },
          ],
        ),
      },
    },
  };
}

function collectionPath(label: string) {
  return {
    get: operation(
      `Get ${label}`,
      `Returns the ${label} published for one study.`,
      { "200": jsonResponse(label), "404": jsonResponse("Not found") },
      [idParam()],
    ),
  };
}

function subobjectPath(label: string) {
  return {
    get: operation(
      `Get one ${label}`,
      `Returns one stable ${label} object belonging to the study.`,
      { "200": jsonResponse(label), "404": jsonResponse("Not found") },
      [
        idParam(),
        {
          name: "objectId",
          in: "path",
          required: true,
          schema: { type: "string" },
          description: `Local or canonical ${label} identifier.`,
        },
      ],
    ),
  };
}

function operation(
  summary: string,
  description: string,
  responses: Record<string, unknown>,
  parameters: unknown[] = [],
) {
  return { summary, description, parameters, responses };
}

function jsonResponse(description: string) {
  return {
    description,
    content: { "application/json": { schema: { type: "object" } } },
  };
}

function idParam() {
  return {
    name: "id",
    in: "path",
    required: true,
    schema: { type: "string" },
    description: "Paper slug or GSX study id.",
  };
}

function reviewPath(kind: string, label: string) {
  return {
    get: operation(`List ${label.toLowerCase()}`, `Returns published ${label.toLowerCase()}. The list is empty until review publishes one.`, {
      "200": jsonResponse(label),
    }),
    post: operation(
      `Validate a ${kind}`,
      `Checks a proposed ${kind}. A valid object is not stored and is not published.`,
      { "200": jsonResponse("Valid, unpublished"), "400": jsonResponse("Invalid JSON"), "422": jsonResponse("Validation errors") },
    ),
  };
}

function studyCommunityPath(kind: string) {
  return {
    get: operation(
      `Get ${kind} for one study`,
      `Returns the published ${kind} for one study. The list is empty until review publishes one.`,
      { "200": jsonResponse(kind), "404": jsonResponse("Not found") },
      [idParam()],
    ),
  };
}

function slugParam(description: string) {
  return {
    name: "slug",
    in: "path",
    required: true,
    schema: { type: "string" },
    description,
  };
}
