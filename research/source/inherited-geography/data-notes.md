# Data and model notes

## 1. Identification boundary

No available South African microdataset jointly observes population group, receipt of property inheritance, asset type, legal tenure, title quality, exact location, transaction liquidity, collateral access, rental income, agricultural productivity and descendant outcomes. The paper therefore keeps three layers separate:

1. **Observed evidence.** Census, probate, NIDS, deeds and agricultural statistics.
2. **Descriptive associations.** Peer-reviewed and institutional work on wealth, housing geography, legal administration, commuting and credit.
3. **Modeled counterfactuals.** Monte Carlo scenarios that vary inherited property while holding the descendant's earnings, education, household size and saving behavior fixed.

The model does not estimate the causal share of the national racial wealth gap attributable to property inheritance. It estimates the magnitude that the specified property mechanism could generate under transparent ranges.

## 2. Units and common descendant

All money is constant 2024 rand. Each matched descendant begins with R50,000 of liquid wealth, earns R420,000 a year in real terms, saves 8% of earnings, and earns a 3.5% real return on financial wealth. The horizon is 20, 40 or 60 years after inheritance. These are scenario controls, not claims about typical South African earnings.

The no-property scenario is the common baseline. Property scenarios change only the inherited asset. Education, occupation, salary, household size and saving are held constant in the main results. A separately reported opportunity module allows collateral-backed enterprise or education gains; it is excluded from the headline matched comparison because keeping earnings fixed and then adding an education earnings premium would be internally inconsistent.

## 3. Property as a bundle

The model distinguishes:

- gross physical or land value;
- the heir's equity after debt, administration and division among heirs;
- marketability and a liquid-equivalent value;
- residential service value and housing expenditure avoided;
- rental income;
- productive agricultural income;
- collateral capacity; and
- appreciation.

Social, custodial, ancestral and family value are discussed but never assigned a rand price. For communal property, broader resource value and marketable wealth are shown separately so that a weak resale market is not mistaken for worthlessness.

## 4. Empirical anchors

### Formal wealth and probate

Simson and Mahmoudzadeh's probate study reports that 3% of Black African, 9% of Coloured, 23% of Asian and 45% of White adults aged 20+ held probatable wealth above R250,000 in pooled 2009-2019 estimates. Its comparison with NIDS Wave 4 reports 8%, 15%, 25% and 47% respectively when all surveyed wealth is counted, or 5%, 9%, 26% and 42% when possessions and vehicles are excluded. Probate undercounts Black and Coloured estates more severely because of lower reporting and formal-title compliance.

The same study reports estate-to-death ratios for any estate of 35% for Black, 45% for Coloured, 59% for Asian and approximately 101% for White decedents; the White ratio above one demonstrates timing or denominator error and cannot be read literally. The synthetic receiver probabilities in `model.py` are therefore below these decedent-estate rates and have deliberately wide triangular ranges. They are **scenario brackets**, not measured inheritance receipt rates.

### Geography and type

Among gazetted Black estate-leavers in 2019, 42% lived in former townships and 17% in former homelands. These are addresses of a selected, formally processed subset, not a national distribution of inherited property types. They anchor but do not determine the Black African synthetic mixture. For Coloured, Indian/Asian and White scenarios, type weights are explicitly assumptions informed by formal-estate incidence, apartheid settlement history and the national property-value distribution. No individual is assigned a type from race.

### Residential values and market depth

The CAHF 2024 report, using Lightstone-cleaned deeds data at 31 December 2023, reports 6.91 million registered residential properties worth R6.789 trillion. Sixty-six per cent were valued at R900,000 or less and 76% below R1.2 million. It reports 150,738 resale transactions in 2023, down 19% from 2022; 59% of resales were bonded. Only 12% of resale transactions under R300,000 were bonded, compared with 47.8% at R300,000-R600,000 and about 60% from R600,000 to R3 million. This is direct evidence that liquidity and mortgageability vary across market segments.

Government-subsidised-property resales averaged R560,570 when mortgage-financed and R235,137 when not mortgage-financed in 2023. The titled-township central value is R560,000, with a broad lognormal distribution; this is a scenario anchor, not a claim that every township house is subsidised or has that value.

### Housing service value

Statistics South Africa's 2014/15 Living Conditions Survey applied a 7.135% rental yield to owner-occupied dwelling value when estimating housing expenditure. The model uses lower net housing-service ranges after maintenance, vacancy and the fact that not every heir can occupy the property. The resulting housing-saving channel is therefore not a direct reproduction of the Stats SA imputation.

### Appreciation

There is no public, nationally representative, inheritance-linked repeat-sales series by historical settlement type and title status. Real appreciation is therefore modeled with wide triangular ranges that include negative outcomes. The CAHF report's 2.17% nominal increase in the total residential portfolio in 2023 is a one-year stock result and is not treated as a long-run real return.

### Collateral and enterprise

The OECD notes that clearly defined immovable-property rights can provide collateral for young firms with short credit histories, while timely insolvency and enforceable rights matter to recovery. CAHF's bonded-transaction gradient supplies a market-specific constraint. Collateral loan-to-value parameters remain scenario ranges. Enterprise outcomes include losses and are reported only in the extended opportunity case.

## 5. Agricultural module

The agricultural module begins each scenario with the same R2.5 million notional land resource and a 20-year horizon. It crosses two tenure conditions (communal/customary versus freehold) with two productive packages (rain-fed/low capital versus water access plus operating capital). The land area and starting resource value are identical; marketability, collateral, appreciation and productive income differ.

The module is anchored to these observations:

- the 2017 commercial-agriculture census counted 40,122 farming units using 46.4 million hectares and earning R332.8 billion in gross income; 77% of the land used was farmer-owned;
- the 2017 Land Audit could assign race only to private individual owners, not the full holdings of companies, trusts, institutions, community organisations, state land or unregistered communal land;
- the audit reports White individuals held 72%, Coloured individuals 15%, Indian individuals 5% and African individuals 4% of the 37.0 million hectares of farms and agricultural holdings held by individuals; these are **not shares of all agricultural land**;
- research on PLAS acquisitions finds farm size, location, water rights and extension access associated with prices, while less than 20% of beneficiaries in that study had water rights; and
- communal-tenure evidence rejects the idea that private title is the only form of secure or valuable tenure.

The agricultural scenarios are not assigned to population groups. This avoids turning incomplete individual-title statistics into racial claims about all agricultural land.

## 6. Monte Carlo mechanics

Each scenario uses 100,000 deterministic draws (`seed=20260920`). Initial values are lognormal because property values are right-skewed. Rates and institutional fractions are triangular because data support ranges and a central judgment rather than fitted parametric distributions. Multiple heirs, inherited debt, estate-administration haircuts, marketability, maintenance, rental choice, real appreciation and financial returns are independently drawn unless the model code explicitly links them.

Independence is a simplifying assumption and likely understates joint disadvantage: remote location, weak title, low service access and thin markets are often correlated. Conversely, it may overstate compounding by holding the property continuously and not modeling forced sale, disaster, expropriation, major renovation, migration or policy change.

## 7. What the group-conditioned layer means

The synthetic population-group intake layer is a stress test of aggregate historical differences. It combines uncertain receipt probabilities, broad type mixtures, multiple claimants and marketability haircuts. It is not a fitted micro-simulation and should not be used as a population forecast. Its purpose is to demonstrate three points:

- zeros matter to an unconditional distribution;
- formal estate incidence and inherited asset type can jointly widen liquid-equivalent differences; and
- every group contains a wide, overlapping distribution.

The matched-descendant layer, not the group-conditioned layer, is the paper's main mechanism test.

## 8. Known omissions

- inter vivos transfers, deposit help and private-school or university payments are discussed but not directly observed;
- title backlogs, informal sales and unreported succession are incompletely measured;
- municipal valuation rolls are not nationally harmonised with deeds transactions;
- household survey wealth is subject to missing values, self-valuation error, attrition and top-tail non-response;
- probate data select deaths, formal reporting and titled wealth, and infer population group from names;
- agricultural company, trust, community and state holdings cannot be racially allocated from the 2017 audit;
- tax, conveyancing fees, estate duty, capital-gains tax and detailed mortgage amortisation are simplified into debt and administration haircuts; and
- climate, crime, municipal failure and neighbourhood change are captured only indirectly through broad return distributions.

