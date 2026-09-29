export const mathematicalStandard = {
  id: "GreyScienx Mathematical Standard 1.0",
  version: "1.0",
  title: "Mathematical writing",
  summary:
    "Rules for reporting variables, scenarios, sensitivity, and claim traceability in GreyScienx computational studies. Version 1.0 records the publication's current reporting practice.",
  sections: [
    {
      number: "01",
      label: "Scope",
      title: "What this standard governs",
      paragraphs: [
        "This standard applies to exploratory simulations, scenarios, and counterfactuals published by GreyScienx. It covers variable definitions, units, equation numbering, parameter provenance, uncertainty, sensitivity, seeds, software versions, and the path from an assumption to a claim.",
        "Prose tone is a separate editorial matter. A study can meet this standard in plain language. Meeting it does not confer peer review.",
      ],
    },
    {
      number: "02",
      label: "Quantities",
      title: "Variables, units, and equations",
      paragraphs: [
        "Every reported variable has a name, a definition, a unit, and a provenance. Provenance names the scenario, dataset, or assumption the number comes from. Parameters that are chosen rather than measured are labelled as assumptions.",
        "Equations are numbered. A result quotes the equation or accounting identity it uses, and it keeps the unit of that equation. Percentages, currency, people, and years are not mixed without the conversion being shown. Numerical precision stays within what the inputs support.",
      ],
    },
    {
      number: "03",
      label: "Language",
      title: "Scenarios, models, and counterfactuals",
      paragraphs: [
        "Simulation output is reported as a modelled result, a scenario, an estimate, or a counterfactual. A scenario is labelled as a scenario. A counterfactual is labelled with the alternative it compares.",
        "Cohabitation is reported as cohabitation. Household figures are reported at household level, and individual figures at individual level. Differences are reported in the units in which they were calculated. Absolute differences stay absolute differences.",
      ],
    },
    {
      number: "04",
      label: "Robustness",
      title: "Sensitivity, seeds, and software",
      paragraphs: [
        "A computational study reports the assumptions that move its results. Sensitivity runs name the parameter, the alternative values, and the direction of the change.",
        "Where a model uses random draws, the report includes the seed and the number of draws. The software name and version, and the model version, travel with the result. Data provenance names the public source or the constructed scenario the run used.",
      ],
    },
    {
      number: "05",
      label: "Traceability",
      title: "From assumption to claim",
      paragraphs: [
        "A published claim should identify the result it summarises, and that result should identify the assumptions that materially affect it. Stable identifiers are the route: a study is GSX:POP-009, and later a claim, assumption, result, or model can hang from that study without changing the study id.",
        "Until those sub-objects are extracted, the study record says so. The catalog summary is the public description of the study. It is not a conditional conclusion.",
      ],
    },
    {
      number: "06",
      label: "Status",
      title: "Epistemic status is part of the result",
      paragraphs: [
        "Every study record carries its study type, evidence status, peer-review status, external-review status, AI-assistance disclosure, version, and record date. Current GreyScienx studies are modelled and exploratory. Peer review is none. AI assistance in research, drafting, and computation is disclosed and is not itemised study by study until each manuscript is audited.",
        "Readers and agents should receive the status with the statement. A later version of a study keeps the same identifier and a new version number.",
      ],
    },
  ],
} as const;
