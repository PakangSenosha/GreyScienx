export type StudyOverlay = {
  primaryQuestion: string;
  relatedQuestions: string[];
  topics: string[];
  geographies: string[];
};

const southAfrica = ["South Africa"];

export const studyOverlays: Record<string, StudyOverlay> = {
  "economics-of-living-together": {
    primaryQuestion:
      "How do early cohabitation, delayed cohabitation, and separate households compare in a Gauteng lifetime scenario?",
    relatedQuestions: [
      "What is the lifetime household comparison between living together and maintaining separate households?",
      "How does the timing of cohabitation change the cost of living and saving?",
    ],
    topics: ["cohabitation", "lifetime-wealth", "housing", "south-africa"],
    geographies: ["South Africa", "Gauteng"],
  },
  "the-first-three-years-advantage": {
    primaryQuestion:
      "How can delaying rent and car ownership at the start of a career alter lifetime wealth?",
    relatedQuestions: [
      "How does living with parents during the first years of employment compare with paying rent for a separate household?",
      "What is the lifetime wealth comparison between delaying car ownership and buying a car at first employment?",
    ],
    topics: ["lifetime-wealth", "cohabitation", "housing", "south-africa"],
    geographies: ["South Africa", "Johannesburg", "Cape Town", "Durban"],
  },
  "when-retirement-becomes-impossible": {
    primaryQuestion: "What are the demographic and financial limits of retirement at 60?",
    relatedQuestions: [
      "Under what conditions does retirement at 60 remain financially viable?",
      "How do ageing and lifetime finances constrain retirement at a fixed age?",
    ],
    topics: ["retirement", "pensions", "population-decline", "south-africa"],
    geographies: southAfrica,
  },
  "todays-unemployment-is-tomorrows-pension-crisis": {
    primaryQuestion:
      "How does youth unemployment, followed across a lifetime, become old-age dependence?",
    relatedQuestions: [
      "How can today's unemployment become tomorrow's pension pressure?",
      "What happens to old-age income when early working years are spent unemployed?",
    ],
    topics: ["unemployment", "pensions", "retirement", "south-africa"],
    geographies: southAfrica,
  },
  "does-raising-the-retirement-age-actually-work": {
    primaryQuestion:
      "Does raising the retirement age still work once youth unemployment, productivity, and disability are taken into account?",
    relatedQuestions: [
      "What happens to a higher retirement age when younger workers are unemployed?",
      "How do productivity and disability change the case for a later retirement age?",
    ],
    topics: ["retirement", "unemployment", "fiscal-policy", "south-africa"],
    geographies: southAfrica,
  },
  "the-politics-of-an-ageing-electorate": {
    primaryQuestion: "How can voter age structure redirect spending and intergenerational transfers?",
    relatedQuestions: [
      "How does an ageing electorate change the politics of public spending?",
      "What happens to intergenerational transfers when the median voter is older?",
    ],
    topics: ["fiscal-policy", "retirement", "population-decline", "south-africa"],
    geographies: southAfrica,
  },
  "emergency-ageing-austerity": {
    primaryQuestion:
      "Which policy packages for closing an ageing-related fiscal deficit are examined for lower welfare loss?",
    relatedQuestions: [
      "How can an ageing-related fiscal deficit be closed?",
      "What is the welfare comparison among emergency responses to demographic fiscal pressure?",
    ],
    topics: ["fiscal-policy", "retirement", "population-decline", "south-africa"],
    geographies: southAfrica,
  },
  "the-price-of-another-child": {
    primaryQuestion: "When does fertility support become cheaper than financing demographic decline?",
    relatedQuestions: [
      "What is the fiscal comparison between supporting another child and financing an older population?",
      "How does population decline change the public cost of low fertility?",
    ],
    topics: ["population-decline", "fiscal-policy", "south-africa"],
    geographies: southAfrica,
  },
  "the-hundred-year-life": {
    primaryQuestion:
      "How would education, work, housing, and family life be redesigned for lives of 100 to 120 years?",
    relatedQuestions: [
      "What happens to housing when people live longer?",
      "How do longer lives change work, education, and family timing?",
    ],
    topics: ["population-decline", "housing", "retirement", "south-africa"],
    geographies: southAfrica,
  },
  "inheritance-after-retirement": {
    primaryQuestion: "What is the economic difference when inheritance arrives at 40, 55, 70, or 85?",
    relatedQuestions: [
      "How does the age at which inheritance arrives change its economic value?",
      "What happens to inheritance when retirement and longer lives move bequests later?",
    ],
    topics: ["inheritance", "retirement", "lifetime-wealth", "south-africa"],
    geographies: southAfrica,
  },
  "how-to-shrink-a-country-without-breaking-it": {
    primaryQuestion:
      "What happens to housing, cities, and public infrastructure under population contraction?",
    relatedQuestions: [
      "What happens to house prices when population declines?",
      "Can housing scarcity persist while population falls?",
      "How should cities and infrastructure adjust when a country shrinks?",
    ],
    topics: ["population-decline", "housing", "cities", "south-africa"],
    geographies: southAfrica,
  },
  "the-scarce-worker-economy": {
    primaryQuestion: "Can automation, productivity, and immigration substitute for missing workers?",
    relatedQuestions: [
      "What replaces workers when population decline leaves labour scarce?",
      "How do automation and immigration compare as responses to a smaller workforce?",
    ],
    topics: ["population-decline", "unemployment", "south-africa"],
    geographies: southAfrica,
  },
  "the-population-system": {
    primaryQuestion: "How do the population studies connect as one policy system?",
    relatedQuestions: [
      "How do retirement, fertility, housing, labour, and fiscal pressure interact?",
      "What does population decline look like when the separate studies are read together?",
    ],
    topics: ["population-decline", "fiscal-policy", "retirement", "south-africa"],
    geographies: southAfrica,
  },
  "extreme-fiscal-pressure": {
    primaryQuestion:
      "How could emergency government measures introduced in 2050 alter the population system?",
    relatedQuestions: [
      "What happens to the population system under extreme fiscal pressure?",
      "How do emergency measures in a future decade feed back into work, retirement, and public finance?",
    ],
    topics: ["fiscal-policy", "population-decline", "south-africa"],
    geographies: southAfrica,
  },
  "the-r350-industrialisation-counterfactual": {
    primaryQuestion:
      "What productive-capital alternative to repeated emergency cash transfers does the R350 counterfactual examine?",
    relatedQuestions: [
      "What might South Africa have built with the SRD grant budget?",
      "How does an industrialisation counterfactual compare with paying the R350 grant?",
    ],
    topics: ["grants", "industrialisation", "fiscal-policy", "south-africa"],
    geographies: southAfrica,
  },
  "the-welfare-cost-of-not-paying-the-grant": {
    primaryQuestion:
      "What poverty, consumption, and social costs does the industrialisation counterfactual leave out when the grant is not paid?",
    relatedQuestions: [
      "What is the welfare cost of withholding the SRD grant?",
      "Which social costs sit outside a productive-capital account of the grant budget?",
    ],
    topics: ["grants", "fiscal-policy", "south-africa"],
    geographies: southAfrica,
  },
  "consumption-today-or-productive-capital-tomorrow": {
    primaryQuestion:
      "What is the timing and distributional trade-off between relief today and productive capital tomorrow?",
    relatedQuestions: [
      "Who bears the wait if grant spending is redirected toward investment?",
      "How does the R350 choice split between consumption and productive capital?",
    ],
    topics: ["grants", "industrialisation", "fiscal-policy", "south-africa"],
    geographies: southAfrica,
  },
  "the-public-capital-multiplier": {
    primaryQuestion: "When do state-financed productive assets generate durable economic capacity?",
    relatedQuestions: [
      "What public-capital multiplier is at issue when grant-scale funds finance productive assets?",
      "How can state investment become lasting capacity rather than a one-round expenditure?",
    ],
    topics: ["industrialisation", "fiscal-policy", "south-africa"],
    geographies: southAfrica,
  },
  "the-r200-billion-factory": {
    primaryQuestion:
      "What industrial deployment does a scenario at the scale of the grant programme describe?",
    relatedQuestions: [
      "What does a factory programme at R200 billion scale contain?",
      "How is grant-scale public money represented as industrial plant?",
    ],
    topics: ["industrialisation", "grants", "south-africa"],
    geographies: southAfrica,
  },
  "the-south-african-critical-minerals-industrial-complex": {
    primaryQuestion: "How could South African mineral endowment be converted into industrial depth?",
    relatedQuestions: [
      "What industrial system connects critical minerals to domestic production?",
      "How does the critical-minerals complex differ from exporting unprocessed ore?",
    ],
    topics: ["critical-minerals", "industrialisation", "south-africa"],
    geographies: southAfrica,
  },
  "the-platinum-to-hydrogen-economy": {
    primaryQuestion: "How can platinum reserves connect to a hydrogen industrial base?",
    relatedQuestions: [
      "What value chain runs from platinum to a hydrogen economy?",
      "How does hydrogen industrialisation use South Africa's platinum endowment?",
    ],
    topics: ["critical-minerals", "industrialisation", "south-africa"],
    geographies: southAfrica,
  },
  "the-manganese-to-battery-economy": {
    primaryQuestion:
      "What route runs from manganese extraction to higher-value battery production?",
    relatedQuestions: [
      "How could a manganese industry move into battery manufacturing?",
      "What industrial steps sit between mined manganese and batteries?",
    ],
    topics: ["critical-minerals", "industrialisation", "south-africa"],
    geographies: southAfrica,
  },
  "the-vanadium-grid-storage-economy": {
    primaryQuestion: "Can domestic grid storage anchor a vanadium industry?",
    relatedQuestions: [
      "How does grid storage create a home market for vanadium?",
      "What industrial economy is built around vanadium and electricity storage?",
    ],
    topics: ["critical-minerals", "industrialisation", "south-africa"],
    geographies: southAfrica,
  },
  "the-capital-goods-economy": {
    primaryQuestion:
      "What equipment, capabilities, and supplier networks sit behind durable industrialisation?",
    relatedQuestions: [
      "Why do capital goods determine whether industrialisation lasts?",
      "What supplier base does a capital-goods economy require?",
    ],
    topics: ["industrialisation", "south-africa"],
    geographies: southAfrica,
  },
  "the-mineral-sovereign-wealth-fund": {
    primaryQuestion:
      "What fiscal architecture converts exhaustible mineral resources into permanent public wealth?",
    relatedQuestions: [
      "How can a sovereign wealth fund hold mineral rents for the public?",
      "What happens to public wealth when mineral revenue is saved rather than spent once?",
    ],
    topics: ["critical-minerals", "fiscal-policy", "industrialisation", "south-africa"],
    geographies: southAfrica,
  },
  "south-africa-in-a-richer-africa": {
    primaryQuestion:
      "What are the macroeconomic consequences for South Africa of broad African income convergence?",
    relatedQuestions: [
      "How does a richer African continent change the South African economy?",
      "What happens to South African growth if African incomes converge upward?",
    ],
    topics: ["african-economy", "south-africa"],
    geographies: southAfrica,
  },
  "johannesburg-as-africas-financial-capital": {
    primaryQuestion: "Under what conditions could Johannesburg finance a continent-scale economy?",
    relatedQuestions: [
      "What would make Johannesburg Africa's financial capital?",
      "How do continental growth and local institutions shape Johannesburg's financial role?",
    ],
    topics: ["african-economy", "cities", "south-africa"],
    geographies: ["South Africa", "Johannesburg"],
  },
  "the-factory-for-african-urbanisation": {
    primaryQuestion:
      "How can South African production serve the infrastructure of African city growth?",
    relatedQuestions: [
      "What industrial role does South Africa have in African urbanisation?",
      "Which city-building goods could a South African factory system supply?",
    ],
    topics: ["african-economy", "cities", "industrialisation", "south-africa"],
    geographies: southAfrica,
  },
  "inherited-geography": {
    primaryQuestion:
      "How does South Africa's unequal property geography continue to compound into differences in wealth?",
    relatedQuestions: [
      "How does inherited property geography relate to South Africa's racial wealth gap?",
      "How do the type, location, and tenure of inherited property carry advantage across generations?",
    ],
    topics: ["inheritance", "housing", "lifetime-wealth", "south-africa"],
    geographies: southAfrica,
  },
};
