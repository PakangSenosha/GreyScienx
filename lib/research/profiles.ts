import { profileForms } from "./extractions/from-profiles";

export type ProfileForm = (typeof profileForms)[keyof typeof profileForms];

export type PublicProfile = {
  id: string;
  slug: string;
  name: string;
  role: string;
  affiliation: string;
  location: string;
  bio: string;
  email: string;
  study_count: number;
  studies: Array<{
    id: string;
    slug: string;
    title: string;
    series_slug: string;
    series_title: string;
    summary: string;
    href: string;
  }>;
  profile_schema: string | null;
  biography: ProfileForm["biography"] | null;
  roles: ProfileForm["roles"];
  education: ProfileForm["education"];
  places: ProfileForm["locations"];
  external_profiles: ProfileForm["external_profiles"];
  external_writing: ProfileForm["external_writing"];
  experience: ProfileForm["experience"];
  certifications: ProfileForm["certifications"];
  portfolio_work: ProfileForm["portfolio_work"];
  unreviewed_public_code: ProfileForm["unreviewed_public_code"];
  statements: ProfileForm["statements"];
  epistemic_positions: ProfileForm["epistemic_positions"];
  absences: ProfileForm["absences"];
  corpus: ProfileForm["corpus"] | null;
  links: {
    html: string;
    index: string;
    json: string;
  };
};

export function profileForm(slug: string): ProfileForm | null {
  return profileForms[slug as keyof typeof profileForms] ?? null;
}

export function profileMarkdown(profile: PublicProfile) {
  const form = profileForm(profile.slug);
  const sections = profile.biography?.sections ?? [];
  const body = sections
    .map((section) => `## ${section.heading}\n\n${section.paragraphs.join("\n\n")}`)
    .join("\n\n");
  const series = (form?.corpus.series ?? [])
    .map((series) => {
      const studies = series.studies
        .map((study) => `- ${study.id}: ${study.title}. ${study.description}`)
        .join("\n");
      return `### ${series.id} ${series.title}\n\n${series.question}\n\n${studies}`;
    })
    .join("\n\n");
  const sentence = (text: string) => `${text.trim().replace(/\.+$/, "")}.`;
  const statements = (profile.statements ?? [])
    .map((item) => `- ${item.id}. ${sentence(item.statement)} Source: ${sentence(item.source)}`)
    .join("\n");
  const absences = (profile.absences ?? []).map((item) => `- ${item.statement}`).join("\n");
  const experience = (profile.experience ?? [])
    .map((item) => `- ${item.title}, ${item.organisation}, ${item.start} to ${item.end}. ${item.location}.`)
    .join("\n");
  const work = (profile.portfolio_work ?? [])
    .map((item) => `- ${item.title} (${item.years}). ${item.summary} ${item.url}.`)
    .join("\n");
  return `# ${profile.name}

${profile.id}

${profile.biography?.summary ?? profile.bio}

${body}

## Study register

${series}

## Statements

${statements}

## Practice

${experience}

## Other work

${work}

## Not published

${absences}

Canonical page: ${profile.links.html}
`;
}

export function profileJsonLd(profile: PublicProfile) {
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Person",
        "@id": profile.links.html,
        name: profile.name,
        givenName: "Pakang",
        familyName: "Senosha",
        description: profile.biography?.summary ?? profile.bio,
        email: profile.email,
        url: profile.links.html,
        homeLocation: {
          "@type": "Place",
          name: profile.location,
        },
        affiliation: {
          "@type": "CollegeOrUniversity",
          name: profile.affiliation,
        },
        sameAs: (profile.external_profiles ?? []).map((item) => item.url),
      },
      {
        "@type": "Organization",
        name: "GreyScienx",
        url: "https://greyscienx.com",
        founder: { "@id": profile.links.html },
      },
    ],
  };
}
