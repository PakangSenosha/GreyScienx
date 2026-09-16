import type { ResearchSeries, Researcher } from "./types";

export const researchers: Researcher[] = [
  {
    slug: "pakang-senosha",
    subdomain: "pakangsenosha",
    name: "Pakang Senosha",
    givenName: "Pakang",
    affiliation: "University of Pretoria",
    role: "MSc Epidemiology and Biostatistics",
    bio: "Pakang Senosha is an MSc student in Epidemiology and Biostatistics at the University of Pretoria and the founder of GreyScienx.",
    location: "Pretoria, South Africa",
    email: "senoshapakang@gmail.com",
    links: [
      { label: "LinkedIn", href: "https://www.linkedin.com/in/pakang-senosha/" },
      { label: "GitHub", href: "https://github.com/Pakang619" },
    ],
  },
];

export const researchSeries: ResearchSeries[] = [
  {
    number: "01",
    slug: "household-economics",
    title: "Household Economics",
    description:
      "How household formation changes the cost of living, saving and lifetime financial resilience.",
    papers: [
      {
        number: "01",
        slug: "economics-of-living-together",
        title: "The Economics of Living Together",
        description:
          "A Gauteng lifetime scenario comparing early cohabitation, delayed cohabitation and separate households.",
        href: "/research/household-economics/greyscienx-economics-of-living-together.pdf",
        pages: 19,
        size: "0.57 MB",
      },
    ],
  },
  {
    number: "02",
    slug: "population-futures",
    title: "Population Futures",
    description:
      "Twelve connected studies of ageing, work, fertility, retirement, inheritance and fiscal pressure.",
    papers: [
      {
        number: "01",
        slug: "when-retirement-becomes-impossible",
        title: "When Retirement Becomes Impossible",
        description: "The demographic and financial limits of retirement at 60.",
        href: "/research/population-futures/when-retirement-becomes-impossible.pdf",
        pages: 14,
        size: "1.01 MB",
      },
      {
        number: "02",
        slug: "todays-unemployment-is-tomorrows-pension-crisis",
        title: "Today’s Unemployment Is Tomorrow’s Pension Crisis",
        description: "Youth unemployment followed across a lifetime and into old-age dependence.",
        href: "/research/population-futures/todays-unemployment-is-tomorrows-pension-crisis.pdf",
        pages: 15,
        size: "0.83 MB",
      },
      {
        number: "03",
        slug: "does-raising-the-retirement-age-actually-work",
        title: "Does Raising the Retirement Age Actually Work?",
        description: "Later retirement tested against youth unemployment, productivity and disability.",
        href: "/research/population-futures/does-raising-the-retirement-age-actually-work.pdf",
        pages: 15,
        size: "0.95 MB",
      },
      {
        number: "04",
        slug: "the-politics-of-an-ageing-electorate",
        title: "The Politics of an Ageing Electorate",
        description: "How voter age structure can redirect spending and intergenerational transfers.",
        href: "/research/population-futures/the-politics-of-an-ageing-electorate.pdf",
        pages: 15,
        size: "0.93 MB",
      },
      {
        number: "05",
        slug: "emergency-ageing-austerity",
        title: "Emergency Ageing Austerity",
        description: "Policy packages for closing an ageing-related fiscal deficit with lower welfare loss.",
        href: "/research/population-futures/emergency-ageing-austerity.pdf",
        pages: 15,
        size: "1.06 MB",
      },
      {
        number: "06",
        slug: "the-price-of-another-child",
        title: "The Price of Another Child",
        description: "When fertility support becomes cheaper than financing demographic decline.",
        href: "/research/population-futures/the-price-of-another-child.pdf",
        pages: 19,
        size: "1.00 MB",
      },
      {
        number: "07",
        slug: "the-hundred-year-life",
        title: "The Hundred-Year Life",
        description: "Education, work, housing and family life redesigned for 100–120 year lives.",
        href: "/research/population-futures/the-hundred-year-life.pdf",
        pages: 23,
        size: "1.10 MB",
      },
      {
        number: "08",
        slug: "inheritance-after-retirement",
        title: "Inheritance After Retirement",
        description: "The economic value of inheritance arriving at 40, 55, 70 or 85.",
        href: "/research/population-futures/inheritance-after-retirement.pdf",
        pages: 20,
        size: "1.03 MB",
      },
      {
        number: "09",
        slug: "how-to-shrink-a-country-without-breaking-it",
        title: "How to Shrink a Country Without Breaking It",
        description: "Housing, cities and public infrastructure under population contraction.",
        href: "/research/population-futures/how-to-shrink-a-country-without-breaking-it.pdf",
        pages: 22,
        size: "1.29 MB",
      },
      {
        number: "10",
        slug: "the-scarce-worker-economy",
        title: "The Scarce-Worker Economy",
        description: "Automation, productivity and immigration as substitutes for missing workers.",
        href: "/research/population-futures/the-scarce-worker-economy.pdf",
        pages: 23,
        size: "1.40 MB",
      },
      {
        number: "11",
        slug: "the-population-system",
        title: "The Population System",
        description: "A synthesis of the ten population studies as one connected policy system.",
        href: "/research/population-futures/the-population-system.pdf",
        pages: 29,
        size: "1.08 MB",
      },
      {
        number: "12",
        slug: "extreme-fiscal-pressure",
        title: "Extreme Fiscal Pressure",
        description: "How emergency government measures introduced in 2050 could alter the population system.",
        href: "/research/population-futures/extreme-fiscal-pressure.pdf",
        pages: 29,
        size: "1.76 MB",
      },
    ],
  },
  {
    number: "03",
    slug: "r350-counterfactual",
    title: "The R350 Counterfactual",
    description:
      "What South Africa might have built with the SRD budget—and what society would have lost by withholding it.",
    papers: [
      {
        number: "01",
        slug: "the-r350-industrialisation-counterfactual",
        title: "The R350 Industrialisation Counterfactual",
        description: "The productive-capital alternative to repeated emergency cash transfers.",
        href: "/research/r350-counterfactual/the-r350-industrialisation-counterfactual.pdf",
        pages: 21,
        size: "1.38 MB",
      },
      {
        number: "02",
        slug: "the-welfare-cost-of-not-paying-the-grant",
        title: "The Welfare Cost of Not Paying the Grant",
        description: "The poverty, consumption and social cost omitted from the industrialisation counterfactual.",
        href: "/research/r350-counterfactual/the-welfare-cost-of-not-paying-the-grant.pdf",
        pages: 27,
        size: "1.44 MB",
      },
      {
        number: "03",
        slug: "consumption-today-or-productive-capital-tomorrow",
        title: "Consumption Today or Productive Capital Tomorrow?",
        description: "The timing and distributional trade-off between relief and investment.",
        href: "/research/r350-counterfactual/consumption-today-or-productive-capital-tomorrow.pdf",
        pages: 24,
        size: "1.55 MB",
      },
      {
        number: "04",
        slug: "the-public-capital-multiplier",
        title: "The Public-Capital Multiplier",
        description: "When state-financed productive assets generate durable economic capacity.",
        href: "/research/r350-counterfactual/the-public-capital-multiplier.pdf",
        pages: 19,
        size: "1.40 MB",
      },
      {
        number: "05",
        slug: "the-r200-billion-factory",
        title: "The R200 Billion Factory",
        description: "A concrete industrial deployment scenario at the scale of the grant programme.",
        href: "/research/r350-counterfactual/the-r200-billion-factory.pdf",
        pages: 21,
        size: "1.46 MB",
      },
    ],
  },
  {
    number: "04",
    slug: "strategic-industrialisation",
    title: "Strategic Industrialisation",
    description:
      "Industrial systems that move South African mineral and capital capacity further up the value chain.",
    papers: [
      {
        number: "01",
        slug: "the-south-african-critical-minerals-industrial-complex",
        title: "The South African Critical Minerals Industrial Complex",
        description: "An integrated strategy for converting mineral endowment into industrial depth.",
        href: "/research/strategic-industrialisation/the-south-african-critical-minerals-industrial-complex.pdf",
        pages: 25,
        size: "2.00 MB",
      },
      {
        number: "02",
        slug: "the-platinum-to-hydrogen-economy",
        title: "The Platinum-to-Hydrogen Economy",
        description: "A value-chain model connecting platinum reserves to a hydrogen industrial base.",
        href: "/research/strategic-industrialisation/the-platinum-to-hydrogen-economy.pdf",
        pages: 29,
        size: "1.97 MB",
      },
      {
        number: "03",
        slug: "the-manganese-to-battery-economy",
        title: "The Manganese-to-Battery Economy",
        description: "A route from mineral extraction to higher-value battery production.",
        href: "/research/strategic-industrialisation/the-manganese-to-battery-economy.pdf",
        pages: 28,
        size: "2.02 MB",
      },
      {
        number: "04",
        slug: "the-vanadium-grid-storage-economy",
        title: "The Vanadium Grid-Storage Economy",
        description: "Domestic grid storage as an anchor market for vanadium industrialisation.",
        href: "/research/strategic-industrialisation/the-vanadium-grid-storage-economy.pdf",
        pages: 29,
        size: "2.17 MB",
      },
      {
        number: "05",
        slug: "the-capital-goods-economy",
        title: "The Capital-Goods Economy",
        description: "The equipment, capabilities and supplier networks behind durable industrialisation.",
        href: "/research/strategic-industrialisation/the-capital-goods-economy.pdf",
        pages: 29,
        size: "1.48 MB",
      },
      {
        number: "06",
        slug: "the-mineral-sovereign-wealth-fund",
        title: "The Mineral Sovereign Wealth Fund",
        description: "A fiscal architecture for converting exhaustible resources into permanent public wealth.",
        href: "/research/strategic-industrialisation/the-mineral-sovereign-wealth-fund.pdf",
        pages: 20,
        size: "1.37 MB",
      },
    ],
  },
  {
    number: "05",
    slug: "african-convergence",
    title: "African Convergence",
    description:
      "South Africa’s economy, cities and industrial role in a substantially richer African continent.",
    papers: [
      {
        number: "01",
        slug: "south-africa-in-a-richer-africa",
        title: "South Africa in a Richer Africa",
        description: "The macroeconomic consequences of broad African income convergence.",
        href: "/research/african-convergence/south-africa-in-a-richer-africa.pdf",
        pages: 26,
        size: "1.48 MB",
      },
      {
        number: "02",
        slug: "johannesburg-as-africas-financial-capital",
        title: "Johannesburg as Africa’s Financial Capital",
        description: "The conditions under which Johannesburg could finance a continent-scale economy.",
        href: "/research/african-convergence/johannesburg-as-africas-financial-capital.pdf",
        pages: 38,
        size: "1.41 MB",
      },
      {
        number: "03",
        slug: "the-factory-for-african-urbanisation",
        title: "The Factory for African Urbanisation",
        description: "South African production positioned around the infrastructure of African city growth.",
        href: "/research/african-convergence/the-factory-for-african-urbanisation.pdf",
        pages: 29,
        size: "1.51 MB",
      },
    ],
  },
];

export const papers = researchSeries.flatMap((series) => series.papers);

export function getResearcher(slug: string) {
  return researchers.find((researcher) => researcher.slug === slug);
}

export function getSeries(slug: string) {
  return researchSeries.find((series) => series.slug === slug);
}

export function getPaper(seriesSlug: string, paperSlug: string) {
  const series = getSeries(seriesSlug);
  const paper = series?.papers.find((entry) => entry.slug === paperSlug);
  if (!series || !paper) return null;
  return { series, paper };
}
