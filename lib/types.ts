export type SiteLink = {
  label: string;
  href: string;
};

export type Researcher = {
  slug: string;
  subdomain: string;
  name: string;
  givenName: string;
  affiliation: string;
  role: string;
  bio: string;
  location: string;
  email: string;
  links: SiteLink[];
};

export type ArchivePaper = {
  number: string;
  slug: string;
  title: string;
  description: string;
  href: string;
  pages: number;
  size: string;
};

export type ResearchSeries = {
  number: string;
  slug: string;
  title: string;
  description: string;
  papers: ArchivePaper[];
};

export type Stat = {
  value: string;
  label: string;
};

export type Metric = {
  value: string;
  label: string;
  note: string;
};

export type EvidenceCard = {
  value: string;
  title: string;
  body: string;
};

export type MethodStep = {
  title: string;
  body: string;
};

export type Figure = {
  src: string;
  alt: string;
  caption: string;
  width: number;
  height: number;
};

export type ResearchPaper = {
  slug: string;
  researcherSlug: string;
  protocol: string;
  field: string;
  title: string;
  titleAccent: string;
  dek: string;
  date: string;
  pdf: {
    href: string;
    pages: number;
    size: string;
    filename: string;
  };
  previewImage?: string;
  stats: Stat[];
  finding: {
    kicker: string;
    headline: string;
    body: string;
  };
  results: {
    eyebrow: string;
    headline: string;
    intro: string;
    metrics: Metric[];
    figure?: Figure;
    qualification?: {
      title: string;
      body: string;
    };
  };
  evidence: {
    cards: EvidenceCard[];
    figure?: Figure;
  };
  method: {
    eyebrow: string;
    headline: string;
    steps: MethodStep[];
  };
  inside: {
    eyebrow: string;
    headline: string;
    items: string[];
    integrity?: string;
  };
  downloadNote: string;
  footerNote: string;
};
