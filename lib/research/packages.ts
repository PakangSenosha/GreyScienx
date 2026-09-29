import { formPackages } from "./extractions/from-packages";
import { researchGraph } from "./graph";
import { researchObjects } from "./registry";

export type StudyPackage = {
  manuscript: {
    study_id: string;
    source_path: string;
    source_sha256: string;
    source_bytes: number;
    character_count: number;
    word_count: number;
    headings: Array<{ level: number; title: string; slug: string; line: number }>;
  };
  answer_block: {
    conditional_answer: string;
    evidence_status: string;
    assumption_ids: string[];
    result_ids: string[];
    main_limitation: string;
    sensitivity: string;
  } | null;
  unresolved_questions: string[];
  entities: string[];
  methods: Array<Record<string, unknown>>;
  parameters: Array<Record<string, unknown>>;
  equations: string[];
  scenarios: Array<Record<string, unknown>>;
  datasets: Array<{
    id: string;
    title: string;
    description: string;
    href: string | null;
    geographic_coverage: string;
    licence: string;
  }>;
  sources: Array<{
    id: string;
    type: string;
    title: string;
    author_or_publisher: string;
    date: string;
    href: string | null;
    locator: string;
    supports: string[];
    contradicts: string[];
    note: string;
  }>;
  figures: Array<Record<string, unknown>>;
  tables: Array<Record<string, unknown>>;
  reproducibility: {
    code_available: boolean;
    data_available: boolean;
    environment_available: boolean;
    random_seed: string;
    software: string[];
    repository_url: string | null;
  };
  shared_assumptions: string[];
  shared_datasets: string[];
  shared_models: string[];
  editorial: {
    required_checks: Record<string, unknown>;
    blocking_issues: string[];
    warnings: string[];
    change_log: Array<Record<string, unknown>>;
  };
  files: Array<{
    path: string;
    href: string;
    bytes: number;
    sha256: string;
    media_type: string;
    role: string;
  }>;
};

export function packageFor(studyId: string): StudyPackage | null {
  const record = formPackages[studyId as keyof typeof formPackages];
  return record ?? null;
}

export function discoveryMethods() {
  return [
    ...new Set(
      researchObjects.flatMap((study) => packageFor(study.id)?.reproducibility.software ?? []),
    ),
  ].sort();
}

export function matchesDiscovery(studyId: string, method: string, code: string) {
  const pack = packageFor(studyId);
  const software = pack?.reproducibility.software ?? [];
  const codeAvailable = pack?.reproducibility.code_available ?? false;
  if (method && !software.includes(method)) return false;
  if (code === "recorded" && !codeAvailable) return false;
  if (code === "unrecorded" && codeAvailable) return false;
  return true;
}

export function seriesContext(seriesSlug: string) {
  const studies = researchObjects.filter((study) => study.series_slug === seriesSlug);
  const packs = studies.map((study) => packageFor(study.id)).filter((pack) => pack !== null);
  const names = new Map<string, { name: string; studies: string[] }>();
  for (const study of studies) {
    for (const assumption of study.assumptions) {
      const key = assumption.name.trim().toLowerCase();
      const current = names.get(key) ?? { name: assumption.name, studies: [] };
      if (!current.studies.includes(study.id)) current.studies.push(study.id);
      names.set(key, current);
    }
  }
  const studyIds = new Set(studies.map((study) => study.id));
  const edges = researchGraph().edges.filter(
    (edge) => studyIds.has(edge.subject_id) || studyIds.has(edge.object_id),
  );
  return {
    shared_assumptions: unique(packs.flatMap((pack) => pack.shared_assumptions)),
    shared_datasets: unique(packs.flatMap((pack) => pack.shared_datasets)),
    shared_models: unique(packs.flatMap((pack) => pack.shared_models)),
    unresolved_questions: unique(packs.flatMap((pack) => pack.unresolved_questions)),
    repeated_assumptions: [...names.values()].filter((item) => item.studies.length > 1),
    contradictions: edges.filter((edge) => edge.predicate === "contradicts"),
    qualifications: edges.filter((edge) => edge.predicate === "qualifies"),
  };
}

function unique(values: string[]) {
  return [...new Set(values.filter(Boolean))];
}
