export type TopicDefinition = {
  slug: string;
  title: string;
  definition: string;
  connected: string[];
};

export const topicDefinitions: TopicDefinition[] = [
  {
    slug: "cohabitation",
    title: "Cohabitation",
    definition:
      "Studies of living together, household formation, and the lifetime cost of separate households.",
    connected: ["housing", "lifetime-wealth", "south-africa"],
  },
  {
    slug: "lifetime-wealth",
    title: "Lifetime wealth",
    definition:
      "Studies of how early household and career choices compound into later wealth.",
    connected: ["cohabitation", "inheritance", "housing"],
  },
  {
    slug: "housing",
    title: "Housing",
    definition:
      "Studies of dwellings, household formation, property, and how homes are occupied as populations change.",
    connected: ["population-decline", "cohabitation", "inheritance", "cities"],
  },
  {
    slug: "south-africa",
    title: "South Africa",
    definition:
      "Studies whose published scope is South Africa, its cities, public finances, households, or industrial base.",
    connected: ["industrialisation", "fiscal-policy", "population-decline", "housing"],
  },
  {
    slug: "retirement",
    title: "Retirement",
    definition:
      "Studies of retirement age, old-age dependence, and the limits of retiring on a fixed timetable.",
    connected: ["population-decline", "pensions", "fiscal-policy"],
  },
  {
    slug: "pensions",
    title: "Pensions",
    definition: "Studies that follow work and unemployment into old-age income and public cost.",
    connected: ["retirement", "unemployment", "fiscal-policy"],
  },
  {
    slug: "population-decline",
    title: "Population decline",
    definition:
      "Studies of shrinking or ageing populations, and of the housing, labour, and fiscal pressure that can follow.",
    connected: ["housing", "retirement", "inheritance", "fiscal-policy"],
  },
  {
    slug: "unemployment",
    title: "Unemployment",
    definition: "Studies of joblessness carried across a working life and into later public cost.",
    connected: ["pensions", "retirement", "population-decline"],
  },
  {
    slug: "fiscal-policy",
    title: "Fiscal policy",
    definition:
      "Studies of public budgets under demographic change, grants, and emergency fiscal pressure.",
    connected: ["retirement", "industrialisation", "population-decline", "grants"],
  },
  {
    slug: "inheritance",
    title: "Inheritance",
    definition:
      "Studies of when inherited wealth arrives, and of property advantages carried across generations.",
    connected: ["housing", "lifetime-wealth", "retirement"],
  },
  {
    slug: "grants",
    title: "Social grants",
    definition:
      "Studies of the SRD grant budget, the cost of withholding it, and other uses of the same funds.",
    connected: ["fiscal-policy", "industrialisation", "south-africa"],
  },
  {
    slug: "industrialisation",
    title: "Industrialisation",
    definition:
      "Studies of productive capital, mineral value chains, and public investment in durable capacity.",
    connected: ["south-africa", "fiscal-policy", "critical-minerals", "grants"],
  },
  {
    slug: "critical-minerals",
    title: "Critical minerals",
    definition:
      "Studies of South African mineral endowment and of moving that endowment further up the value chain.",
    connected: ["industrialisation", "south-africa"],
  },
  {
    slug: "african-economy",
    title: "African economy",
    definition:
      "Studies of South Africa’s role if incomes, cities, and capital markets grow across the continent.",
    connected: ["south-africa", "industrialisation", "cities"],
  },
  {
    slug: "cities",
    title: "Cities",
    definition:
      "Studies of urban form, financial centres, and infrastructure when population or African city growth changes.",
    connected: ["housing", "african-economy", "population-decline"],
  },
];

export const topicBySlug = new Map(topicDefinitions.map((topic) => [topic.slug, topic]));
