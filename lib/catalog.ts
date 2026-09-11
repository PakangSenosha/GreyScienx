import type { ResearchPaper, Researcher } from "./types";

export const researchers: Researcher[] = [
  {
    slug: "pakang-senosha",
    subdomain: "pakangsenosha",
    name: "Pakang Senosha",
    givenName: "Pakang",
    affiliation: "University of Pretoria",
    role: "MSc Epidemiology and Biostatistics",
    bio: "Pakang Senosha is an MSc student in Epidemiology and Biostatistics at the University of Pretoria and the founder of GreyScienx. The press exists for semi-professional research that deserves a public site, a downloadable manuscript, and a clear statement of what was found.",
    location: "Pretoria, South Africa",
    email: "senoshapakang@gmail.com",
    links: [
      { label: "LinkedIn", href: "https://www.linkedin.com/in/pakang-senosha/" },
      { label: "GitHub", href: "https://github.com/Pakang619" },
    ],
  },
];

export const papers: ResearchPaper[] = [
  {
    slug: "searching-for-trading-edges",
    researcherSlug: "pakang-senosha",
    protocol: "Evidence protocol 01",
    field: "Quantitative finance",
    title: "Searching for",
    titleAccent: "Trading Edges.",
    dek: "A reproducibility audit and frozen cross-asset study spanning synthetic indices, equities, foreign exchange, metal proxies, and cryptocurrency.",
    date: "6 September 2026",
    pdf: {
      href: "/papers/searching-for-trading-edges/manuscript.pdf",
      pages: 43,
      size: "1.12 MB",
      filename: "Searching-for-Trading-Edges.pdf",
    },
    previewImage: "/papers/searching-for-trading-edges/preview.png",
    stats: [
      { value: "60", label: "registered studies" },
      { value: "37", label: "documented equations" },
      { value: "1,560", label: "hashed artifacts" },
      { value: "73/73", label: "engine tests passed" },
    ],
    finding: {
      kicker:
        "After selection, causality, costs, uncertainty, concentration, and drawdown were tested:",
      headline:
        "No tested strategy established a reproducible, implementation-ready edge.",
      body: "At the sampled horizons, next-period direction remained close to a fair coin. Small nonlinear, tail, and regime effects appeared, but none became stable net predictability. This is a finite conclusion about the tested rules and data, not a universal proof.",
    },
    results: {
      eyebrow: "The measured distribution",
      headline: "The dominant fingerprint was random-walk compatible.",
      intro:
        "The principal Volatility 75 forensic sample contained 39,999 M1 returns. Its marginal distribution was nearly Gaussian, its sign sequence was almost maximally uncertain, and ordered out-of-sample models did not predict direction better than chance.",
      metrics: [
        {
          value: "−0.00263",
          label: "Lag-one return autocorrelation",
          note: "Economically negligible linear memory.",
        },
        {
          value: "0.8375",
          label: "Runs-test p-value",
          note: "The ordering of return signs did not reject randomness.",
        },
        {
          value: "0.9999998",
          label: "Direction entropy, bits",
          note: "Almost the one-bit maximum of a fair binary sequence.",
        },
        {
          value: "0.99898",
          label: "Estimated entropy rate",
          note: "Prior directions removed almost none of the uncertainty.",
        },
        {
          value: "49.88%",
          label: "Walk-forward accuracy",
          note: "Approximate 95% interval: 49.10% to 50.67%.",
        },
        {
          value: "p = 0.58",
          label: "Permutation test",
          note: "No statistically credible directional forecast.",
        },
        {
          value: "0.489–0.506",
          label: "DFA Hurst estimates",
          note: "M1, M5, and M15 remained close to Brownian H=0.5.",
        },
        {
          value: "0.00293",
          label: "Mean cross-index |correlation|",
          note: "V10, V25, and V75 exposed no common generator factor.",
        },
      ],
      figure: {
        src: "/papers/searching-for-trading-edges/random-walk-diagnostics.png",
        alt: "Hurst, directional accuracy, and entropy diagnostics supporting a random-walk-compatible interpretation",
        caption:
          "Memory remained near Brownian, predictive accuracy stayed near 50%, and normalized uncertainty remained close to its maximum.",
        width: 2667,
        height: 1992,
      },
      qualification: {
        title: "What “random” means here",
        body: "The data were not perfectly featureless. Mutual-information, jump, volatility, and state diagnostics found small departures from literal Gaussian iid behavior. Those departures did not survive as reproducible, cost-covering directional strategies.",
      },
    },
    evidence: {
      cards: [
        {
          value: "152.31%",
          title: "Trend path, then concentration failure",
          body: "The 60-day cross-asset trend path was positive in development, but Bitcoin supplied 70.12% of positive contribution.",
        },
        {
          value: "−13.14%",
          title: "Direct FX replication",
          body: "The frozen 13-pair trend replication lost money after costs and failed its mean, interval, profit-factor, and stress gates.",
        },
        {
          value: "−5.78 bps",
          title: "Drift Switch after spread",
          body: "A small +0.42 bps gross drift could not cover approximately 6.2 bps of round-trip spread on the frozen DSI30 screen.",
        },
        {
          value: "51.79%",
          title: "Selected Vol90 floating drawdown",
          body: "The reproduced high-return path breached the risk ceiling when open positions were marked to market at M1 closes.",
        },
      ],
      figure: {
        src: "/papers/searching-for-trading-edges/development-gates.png",
        alt: "Matrix showing which frozen cross-asset development gates passed and failed",
        caption:
          "Predeclared development gates. The positive stock diagnostic was ineligible by design.",
        width: 2200,
        height: 960,
      },
    },
    method: {
      eyebrow: "What a candidate had to survive",
      headline: "A profitable backtest was only the beginning.",
      steps: [
        {
          title: "Enough evidence",
          body: "At least 200 trade events or 36 calendar months.",
        },
        {
          title: "Positive net mean",
          body: "Returns calculated after stated trading and financing costs.",
        },
        {
          title: "Uncertainty above zero",
          body: "A dependent-data bootstrap interval with a strictly positive lower bound.",
        },
        {
          title: "Economic quality",
          body: "Profit factor above 1.10 and positive spread and delay stresses.",
        },
        {
          title: "Breadth",
          body: "No instrument or year could supply more than half the positive contribution.",
        },
        {
          title: "Controlled risk",
          body: "Development drawdown had to remain better than −40%.",
        },
        {
          title: "Multiple testing",
          body: "Global and family false-discovery-rate q-values below 0.10.",
        },
        {
          title: "Independent confirmation",
          body: "Only a complete gate pass could unlock the untouched annual holdout.",
        },
      ],
    },
    inside: {
      eyebrow: "The complete record",
      headline:
        "Every registered study. Every equation family. Every material correction.",
      items: [
        "Synthetic-index indicators and bots",
        "Generator forensics and information theory",
        "Evolutionary genomes and HMM gates",
        "Neural networks and PPO reinforcement learning",
        "Prospective and zero-refit transfer tests",
        "Stocks, FX, metal proxies, and cryptocurrency",
        "37 equations with disciplinary provenance",
        "EXP-001 through EXP-060 evidence register",
      ],
      integrity: "SHA-256 e56d602346c7b063…",
    },
    downloadNote:
      "The paper is provided as a single, searchable 43-page PDF with all tables, equations, figures, references, and the complete study register.",
    footerNote: "Research cutoff: 6 September 2026 · No orders were sent during the audit.",
  },
  {
    slug: "wits-staff-education",
    researcherSlug: "pakang-senosha",
    protocol: "Evidence protocol 02",
    field: "Higher education · provenance",
    title: "Academic provenance in",
    titleAccent: "South African higher education.",
    dek: "A full-census methods and results study of first tertiary education as a geographic provenance proxy for 4,333 University of the Witwatersrand staff profiles.",
    date: "September 2026",
    pdf: {
      href: "/papers/wits-staff-education/manuscript.pdf",
      pages: 18,
      size: "PDF",
      filename: "Wits-Staff-Education-Methods-and-Results.pdf",
    },
    stats: [
      { value: "4,333", label: "staff profiles" },
      { value: "87.5%", label: "domestic first degree" },
      { value: "12.5%", label: "international first degree" },
      { value: "42", label: "feeder countries" },
    ],
    finding: {
      kicker:
        "First tertiary education was used as the earliest systematically recorded provenance proxy:",
      headline:
        "International first education is rare overall, and rises sharply with academic rank.",
      body: "Among staff with a specified awarding institution, 87.5% completed their first degree in South Africa and 12.5% completed it abroad. International first education is uncommon among associate lecturers and lecturers, then climbs to more than one in three full professors and nearly half of research associates. Pre-tertiary school records were absent from the directory.",
    },
    results: {
      eyebrow: "The measured distribution",
      headline: "The first-degree map is domestic, with a seniority gradient.",
      intro:
        "The census covered 4,333 public directory profiles across five faculties. Direct citizenship and birthplace are protected under POPIA, so earliest recorded tertiary education was treated as the available provenance proxy.",
      metrics: [
        {
          value: "87.55%",
          label: "Domestic first degree",
          note: "3,087 of 3,526 staff with a specified awarding institution.",
        },
        {
          value: "12.45%",
          label: "International first degree",
          note: "439 staff, spanning 42 sovereign jurisdictions.",
        },
        {
          value: "4.12%",
          label: "Associate lecturers trained abroad",
          note: "Junior teaching lines remain overwhelmingly domestic.",
        },
        {
          value: "4.71%",
          label: "Lecturers trained abroad",
          note: "The core teaching corps is locally trained.",
        },
        {
          value: "35.80%",
          label: "Full professors trained abroad",
          note: "More than one in three chairs holds an international first degree.",
        },
        {
          value: "46.34%",
          label: "Research associates trained abroad",
          note: "Nearly half of this research-intensive rank is internationally trained.",
        },
        {
          value: "37.8%",
          label: "United Kingdom share",
          note: "166 staff; the largest international feeder jurisdiction.",
        },
        {
          value: "0.0%",
          label: "Pre-tertiary records",
          note: "No high-school or primary-school fields survived the directory audit.",
        },
      ],
      qualification: {
        title: "What the proxy can and cannot say",
        body: "First undergraduate institution is a provenance and academic-socialisation indicator, not a citizenship test. Postgraduate mobility is common and was not used as the origin marker. Unspecified records (807) include administrative and hospital titles without an awarding body.",
      },
    },
    evidence: {
      cards: [
        {
          value: "39.0%",
          title: "Inequality Studies",
          body: "The Southern Centre for Inequality Studies had the highest international first-education share among departments with at least 30 validated records.",
        },
        {
          value: "37.8%",
          title: "School of Governance",
          body: "Public-policy and administration staff showed high international integration relative to the university mean.",
        },
        {
          value: "35.6%",
          title: "School of Physics",
          body: "Pure-science units clustered with research centres, not with clinical hospital divisions.",
        },
        {
          value: "95–100%",
          title: "Clinical domestic retention",
          body: "Hospital-based medical divisions were almost entirely South African trained, consistent with CMSA licensing pathways.",
        },
      ],
    },
    method: {
      eyebrow: "What the census had to survive",
      headline: "A public directory was treated as a population, not a sample.",
      steps: [
        {
          title: "Full census ingestion",
          body: "4,333 profiles were harvested from 289 directory pages, then opened for qualifications, biography, and identifiers.",
        },
        {
          title: "Pre-tertiary audit",
          body: "Biographies and qualification fields were scanned for matric, high school, and primary school tokens. Detection was 0.0%.",
        },
        {
          title: "Deterministic NLP parsing",
          body: "Qualification strings were decomposed into degree tokens, awarding bodies, and a hierarchical academic taxonomy.",
        },
        {
          title: "Geographic resolution",
          body: "Institutions were mapped onto the South African higher-education network or 40+ international jurisdictions.",
        },
        {
          title: "First-education proxy",
          body: "The earliest recorded tertiary award was used as the provenance marker, not later master’s, doctoral, or fellowship mobility.",
        },
        {
          title: "Rank and faculty cuts",
          body: "International share was computed on valid records by designation, faculty, and department.",
        },
        {
          title: "Privacy constraint",
          body: "Citizenship, birthplace, and naturalisation are not published. Educational provenance is the observable substitute.",
        },
        {
          title: "Open manuscript",
          body: "Methods, classification rules, and empirical tables remain available as a downloadable paper.",
        },
      ],
    },
    inside: {
      eyebrow: "The complete record",
      headline: "Census, parser, ranks, faculties, and feeder countries.",
      items: [
        "Wits public staff directory harvest",
        "Qualification and first-education parser",
        "South African university taxonomy",
        "International institution disambiguation",
        "Academic-rank seniority gradient",
        "Faculty and departmental bifurcation",
        "42 international feeder countries",
        "Open methods-and-results manuscript",
      ],
    },
    downloadNote:
      "The original methods-and-results paper is available as a searchable PDF, including the classification rules, rank tables, and feeder-country register.",
    footerNote:
      "Census: September 2026 · Source: University of the Witwatersrand public staff directory.",
  },
];

export function getResearcher(slug: string) {
  return researchers.find((researcher) => researcher.slug === slug);
}

export function getResearcherBySubdomain(subdomain: string) {
  const key = subdomain.toLowerCase();
  return researchers.find(
    (researcher) =>
      researcher.subdomain === key || researcher.slug === key,
  );
}

export function getPaper(researcherSlug: string, paperSlug: string) {
  return papers.find(
    (paper) =>
      paper.researcherSlug === researcherSlug && paper.slug === paperSlug,
  );
}

export function papersFor(researcherSlug: string) {
  return papers.filter((paper) => paper.researcherSlug === researcherSlug);
}
