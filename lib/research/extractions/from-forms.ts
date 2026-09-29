// Generated from research/templates/semantic-twin/published by compile.mjs.
// Edit the YAML forms, then run: node research/templates/semantic-twin/compile.mjs
export const formExtractions = {
  "GSX:SRD-003": {
    "assumptions": [
      {
        "id": "GSX:SRD-003:A01",
        "local_id": "A01",
        "name": "Shared envelope and welfare values",
        "statement": "The comparison uses the R253.5 billion constant-2026-rand envelope and Paper 2's central welfare value of R426.9 billion, which is R358.2 billion in 2020 present value at 6 percent.",
        "value": "358.2",
        "unit": "billion 2020 present-value rand at 6 percent",
        "type": "model assumption",
        "provenance": "Manuscript central comparison table",
        "evidence_strength": "inherited from the companion papers",
        "sensitivity": "moderate",
        "alternatives": [
          "Conservative or severe welfare values"
        ]
      },
      {
        "id": "GSX:SRD-003:A02",
        "local_id": "A02",
        "name": "Central discount rate",
        "statement": "The central comparison uses a 6 percent real discount rate. The paper also reports 3.5 percent and the 10 percent public-project benchmark.",
        "value": "6",
        "unit": "percent real discount rate",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "normative timing weight",
        "sensitivity": "high",
        "alternatives": [
          "3.5 percent",
          "10 percent"
        ]
      },
      {
        "id": "GSX:SRD-003:A03",
        "local_id": "A03",
        "name": "Asset-inclusive test",
        "statement": "Counting the surviving public asset is legitimate only if the asset is viable, maintained, publicly owned and capable of being sold or of continuing to produce.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript definition of break-even",
        "evidence_strength": "accounting condition",
        "sensitivity": "high",
        "alternatives": [
          "Flow-only test"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:SRD-003:R01",
        "local_id": "R01",
        "statement": "At 6 percent, the best industrial case overtakes the central transfer value in 2040 if the surviving asset is counted, and in 2051 if only operating benefits are counted.",
        "value": "2040",
        "unit": "break-even year, asset-inclusive best case",
        "scenario": "Central comparison, 6 percent real discount rate",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:SRD-003:R02",
        "local_id": "R02",
        "statement": "At 6 percent, best-case industrial value in 2050 is R485.7 billion in present value. Average industrial value is R152.3 billion, R205.9 billion short of the central transfer. At a 10 percent discount rate, none of the industrial cases crosses by 2100.",
        "value": "152.3",
        "unit": "billion 2020 present-value rand, average industrial case in 2050",
        "scenario": "6 percent and 10 percent discount-rate tests",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:SRD-003:M01",
        "local_id": "M01",
        "name": "Transfer versus industrial present-value comparison",
        "statement": "The model compares the present value of the grant's social benefits with the present value of the industrial alternative, using the shared R253.5 billion envelope and a stated real discount rate."
      }
    ],
    "claims": [
      {
        "id": "GSX:SRD-003:C01",
        "local_id": "C01",
        "claim": "At a 6 percent real discount rate, the best industrial case overtakes the central value of the cash transfer in 2040 when the surviving public asset is counted, and in 2051 when only operating benefits are counted.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:SRD-003:A01",
          "GSX:SRD-003:A02",
          "GSX:SRD-003:A03"
        ],
        "result": "GSX:SRD-003:R01",
        "results": [
          "GSX:SRD-003:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "There is no universal year when a factory becomes better than a cash transfer. The best case requires exceptional execution and a credible residual asset. The original households are not necessarily repaid even if the aggregate account later wins.",
        "source_study": "GSX:SRD-003",
        "version": "1.0",
        "href": "https://greyscienx.com/research/r350-counterfactual/consumption-today-or-productive-capital-tomorrow/claims/C01",
        "supported_by": [
          "GSX:SRD-003:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:SRD-003:C02",
        "local_id": "C02",
        "claim": "The average and worst industrial cases do not overtake the central transfer value by 2100 at 6 percent. At the 10 percent public-project benchmark, none of the industrial cases crosses by 2100.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:SRD-003:A01",
          "GSX:SRD-003:A02"
        ],
        "result": "GSX:SRD-003:R02",
        "results": [
          "GSX:SRD-003:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "The discount rate does not change the factory's physical output. It changes how much present sacrifice the model treats as justified.",
        "source_study": "GSX:SRD-003",
        "version": "1.0",
        "href": "https://greyscienx.com/research/r350-counterfactual/consumption-today-or-productive-capital-tomorrow/claims/C02",
        "supported_by": [
          "GSX:SRD-003:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:POP-003": {
    "assumptions": [
      {
        "id": "GSX:POP-003:A01",
        "local_id": "A01",
        "name": "Comparison age",
        "statement": "Age 60 is the common comparison point. Ages 65, 70, and 75 are policy experiments. They are not a description of one current retirement age for every occupation.",
        "value": "60",
        "unit": "years, baseline retirement age",
        "type": "model assumption",
        "provenance": "Manuscript comparison design",
        "evidence_strength": "scenario",
        "sensitivity": "moderate",
        "alternatives": [
          "A different baseline age"
        ]
      },
      {
        "id": "GSX:POP-003:A02",
        "local_id": "A02",
        "name": "Average labour-market case",
        "statement": "The average public scenario follows a one-million-person cohort. It uses standard jobs, 85 percent older-worker productivity, and 0.15 net youth displacement for each additional older-worker job.",
        "value": "0.15",
        "unit": "youth jobs displaced per additional older job",
        "type": "model assumption",
        "provenance": "Manuscript average labour-market case",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "Best case, with a small youth complementarity",
          "Worst case, 0.55 youth displacement"
        ]
      },
      {
        "id": "GSX:POP-003:A03",
        "local_id": "A03",
        "name": "Continuous private saver",
        "statement": "The private-pension path follows a continuously employed saver earning R30,000 a month at 25. Real wages grow by 1.5 percent, 15 percent is contributed, and the account earns a smooth 3 percent real return. The pension is designed to last through age 100.",
        "value": "15",
        "unit": "percent contributed",
        "type": "model assumption",
        "provenance": "Manuscript private-saver exercise",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "The mixed-occupation path, where not everyone remains employed after 60"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:POP-003:R01",
        "local_id": "R01",
        "statement": "Relative to retirement at 60, the average scenario produces a cumulative modelled public gain of R213 billion at 65, R369 billion at 70, and R448 billion at 75. The step from 70 to 75 adds R79 billion.",
        "value": "213000000000",
        "unit": "constant rand, cumulative public gain at age 65",
        "scenario": "Average scenario, one-million-person cohort, versus retirement at 60",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-003:R02",
        "local_id": "R02",
        "statement": "The same average scenario produces 0.50 million lost youth job-years at 65, 0.79 million at 70, and 0.85 million at 75.",
        "value": "0.50",
        "unit": "million youth job-years at a retirement age of 65",
        "scenario": "Average scenario, 0.15 displacement per older job",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-003:R03",
        "local_id": "R03",
        "statement": "For the continuously employed saver, modelled monthly private pension income is R17,223 at a retirement age of 60, R23,309 at 65, R31,727 at 70, and R43,839 at 75.",
        "value": "17223",
        "unit": "constant rand per month at retirement age 60",
        "scenario": "Continuous formal employment, pension through age 100",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:POP-003:M01",
        "local_id": "M01",
        "name": "Retirement-age cohort",
        "statement": "One exercise follows a continuously employed private saver. The other follows one million people from 60 to the tested retirement age, with occupation-specific wages, capacity, and disability. Public results are cumulative balances against retirement at 60. Youth job-years use the scenario's displacement assumption."
      }
    ],
    "claims": [
      {
        "id": "GSX:POP-003:C01",
        "local_id": "C01",
        "claim": "In the average scenario, raising the comparison retirement age from 60 to 65 produces a cumulative modelled public gain of R213 billion for a one-million-person cohort. Age 70 produces R369 billion and age 75 produces R448 billion. The last five-year step adds R79 billion, about half the gain from moving from 65 to 70.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-003:A01",
          "GSX:POP-003:A02"
        ],
        "result": "GSX:POP-003:R01",
        "results": [
          "GSX:POP-003:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "This is a modelled public balance, not a forecast and not a recommendation that every occupation retire at one age. Age 65 is fiscally robust in the manuscript's three labour-market cases. Age 70 and age 75 need the employment and disability conditions stated in the paper. The gain can come from fewer years of old-age support as well as from extra tax-paying years.",
        "source_study": "GSX:POP-003",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/does-raising-the-retirement-age-actually-work/claims/C01",
        "supported_by": [
          "GSX:POP-003:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-003:C02",
        "local_id": "C02",
        "claim": "Under that same average scenario, the later retirement ages are associated with 0.50 million lost youth job-years at 65, 0.79 million at 70, and 0.85 million at 75.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-003:A01",
          "GSX:POP-003:A02"
        ],
        "result": "GSX:POP-003:R02",
        "results": [
          "GSX:POP-003:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "The youth figures are the result of assuming that each additional older-worker job displaces 0.15 of a youth job after demand, skill, and job-creation effects. They are not an observed count of lost jobs. A different displacement assumption changes the result.",
        "source_study": "GSX:POP-003",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/does-raising-the-retirement-age-actually-work/claims/C02",
        "supported_by": [
          "GSX:POP-003:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-003:C03",
        "local_id": "C03",
        "claim": "For a saver who remains continuously employed, the model's monthly private pension is R17,223 if retirement is at 60, R23,309 at 65, R31,727 at 70, and R43,839 at 75.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-003:A03"
        ],
        "result": "GSX:POP-003:R03",
        "results": [
          "GSX:POP-003:R03"
        ],
        "sensitivity": "moderate",
        "main_limitation": "The continuous-employment path is the strongest private case and the easiest to overstate. The manuscript's mixed-occupation path is lower because not everyone keeps a job after 60. A larger balance at a later age can coexist with years of weak earnings before the pension can be drawn.",
        "source_study": "GSX:POP-003",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/does-raising-the-retirement-age-actually-work/claims/C03",
        "supported_by": [
          "GSX:POP-003:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:HH-001": {
    "assumptions": [
      {
        "id": "GSX:HH-001:A01",
        "local_id": "A01",
        "name": "Two Gauteng earners",
        "statement": "The household is two adults in Gauteng with take-home pay of R30,000 and R20,000 a month. The results are combined household wealth, not each person's legal ownership.",
        "value": "30000",
        "unit": "constant 2026 rand per month, higher take-home pay",
        "type": "model assumption",
        "provenance": "Manuscript research claim and scenario table",
        "evidence_strength": "illustrative",
        "sensitivity": "high",
        "alternatives": [
          "Different earnings",
          "A different split of expenses and ownership"
        ]
      },
      {
        "id": "GSX:HH-001:A02",
        "local_id": "A02",
        "name": "Ten-year difference in household timing",
        "statement": "The Early couple combines adequate households at 25. The Later couple combines them at 35. From 35 onward the model gives both the same housing arrangement, income, expenses, shocks, and retirement assumptions.",
        "value": "10",
        "unit": "years",
        "type": "model assumption",
        "provenance": "Manuscript lifetime design",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "A shorter or longer period of separate households"
        ]
      },
      {
        "id": "GSX:HH-001:A03",
        "local_id": "A03",
        "name": "Average-case returns and costs",
        "statement": "In the average case, real salary growth and real living-cost growth are both 0.75% a year. The net real investment return is 3% a year after fees and tax drag. The initial monthly cohabitation dividend is R8,500.",
        "value": "3",
        "unit": "percent net real return per year",
        "type": "model assumption",
        "provenance": "Manuscript average-case table",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "Best case, 5% net real",
          "Worst case, 1% net real"
        ]
      },
      {
        "id": "GSX:HH-001:A04",
        "local_id": "A04",
        "name": "Surplus is invested",
        "statement": "The model invests the available surplus. It does not spend that surplus on a higher lifestyle.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript interpretation",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "The saving is consumed instead of invested"
        ]
      },
      {
        "id": "GSX:HH-001:A05",
        "local_id": "A05",
        "name": "The relationship remains intact",
        "statement": "Both relationships remain intact through the simulation. Separation, custody, maintenance, and a second replacement home are not given a numeric cost.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript limit on what is simulated",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "A breakup whose costs exceed the accumulated benefit"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:HH-001:R01",
        "local_id": "R01",
        "statement": "In the average case, the Early household holds R3.972 million more combined wealth at 75 than the Later household, in constant 2026 rand.",
        "value": "3972000",
        "unit": "constant 2026 rand",
        "scenario": "Average case, age 75, early consolidation minus later consolidation",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:HH-001:R02",
        "local_id": "R02",
        "statement": "In the average case, the Early household spends about R1.059 million less on living costs over the model. At 35, before the later years are financially identical, its lead is R1.188 million.",
        "value": "1059000",
        "unit": "constant 2026 rand of living costs avoided",
        "scenario": "Average case, lifetime living costs and age-35 lead",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:HH-001:R03",
        "local_id": "R03",
        "statement": "At 75 the Early household's lead is R11.287 million in the best case and R1.882 million in the worst case. In the worst case both positions are large funding gaps: about -R16.346 million and -R18.228 million.",
        "value": "11287000",
        "unit": "constant 2026 rand, best-case lead at 75",
        "scenario": "Best case and worst case at age 75",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:HH-001:M01",
        "local_id": "M01",
        "name": "Lifetime household-timing model",
        "statement": "The model follows two household paths from age 25 to 75 in constant 2026 rand. They differ in when they combine households. After 35 their housing arrangement matches, so the remaining gap comes from returns on the earlier balance or from the cost of a negative balance. Best, average, and worst cases change growth, returns, shocks, children, and housing."
      }
    ],
    "claims": [
      {
        "id": "GSX:HH-001:C01",
        "local_id": "C01",
        "claim": "For two Gauteng adults bringing home R30,000 and R20,000 a month, combining households at 25 rather than 35 leaves about R3.972 million more combined household wealth at 75 in the average scenario, in constant 2026 rand. The direct living-cost saving is about R1.059 million. The larger gap comes from investing that earlier saving and from avoiding expensive negative balances.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:HH-001:A01",
          "GSX:HH-001:A02",
          "GSX:HH-001:A03",
          "GSX:HH-001:A04"
        ],
        "result": "GSX:HH-001:R01",
        "results": [
          "GSX:HH-001:R01",
          "GSX:HH-001:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "This is a modelled scenario, not a forecast, and it is household wealth rather than each person's wealth. The manuscript keeps the relationship intact and invests the surplus. The advantage can disappear or reverse if the shared household costs almost as much as two homes, if the saving is consumed, or if separation costs exceed the accumulated benefit. Cohabitation here is a shared household, not a marriage result.",
        "source_study": "GSX:HH-001",
        "version": "1.0",
        "href": "https://greyscienx.com/research/household-economics/economics-of-living-together/claims/C01",
        "supported_by": [
          "GSX:HH-001:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:HH-001:C02",
        "local_id": "C02",
        "claim": "Across the manuscript's three scenarios, earlier household combination still leaves the stronger position at 75. The lead is R11.287 million in the best case, R3.972 million in the average case, and R1.882 million in the worst case. In the worst case that lead only narrows two large funding gaps.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:HH-001:A01",
          "GSX:HH-001:A02",
          "GSX:HH-001:A04",
          "GSX:HH-001:A05"
        ],
        "result": "GSX:HH-001:R01",
        "results": [
          "GSX:HH-001:R01",
          "GSX:HH-001:R03"
        ],
        "sensitivity": "high",
        "main_limitation": "Negative amounts are unmet consumption if the household does not change course. They are not a statement that a bank would finance the shortfall. The worst case cannot repair stagnant earnings, repeated unemployment, weak returns, or inadequate retirement income.",
        "source_study": "GSX:HH-001",
        "version": "1.0",
        "href": "https://greyscienx.com/research/household-economics/economics-of-living-together/claims/C02",
        "supported_by": [
          "GSX:HH-001:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:POP-005": {
    "assumptions": [
      {
        "id": "GSX:POP-005:A01",
        "local_id": "A01",
        "name": "Stress-test gap",
        "statement": "The study imposes a hypothetical R150 billion annual ageing-related fiscal gap in constant 2026 rand. The figure is a stress-test target, about 5.6 percent of the R2.67 trillion in spending cited from the 2026 Budget Speech. It is not a forecast of the current deficit.",
        "value": "150",
        "unit": "billion constant 2026 rand per year",
        "type": "model assumption",
        "provenance": "Manuscript stress-test design",
        "evidence_strength": "illustrative target",
        "sensitivity": "high",
        "alternatives": [
          "A larger or smaller gap"
        ]
      },
      {
        "id": "GSX:POP-005:A02",
        "local_id": "A02",
        "name": "Thirteen capped levers",
        "statement": "Thirteen policy levers are each capped at a visible but limited level. Their mature annual yields are scenario capacities assigned by the model, not official costings.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript lever table",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "A different cap on tax, retirement age, benefits, or borrowing"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:POP-005:R01",
        "local_id": "R01",
        "statement": "All five selected packages close R150 billion once fully implemented. The balanced transition has the lowest welfare-loss index, 64.5. Low visible pain scores 107.3 and leaves about R720 billion of emergency debt after ten years.",
        "value": "64.5",
        "unit": "internal welfare-loss index, balanced transition",
        "scenario": "Five packages, each closing the R150 billion gap",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-005:R02",
        "local_id": "R02",
        "statement": "The balanced transition uses R57 billion of targeted pension measures, R24 billion of additional pre-funding, R26 billion of worker tax, R22 billion from a phased retirement-age change, R6 billion of weaker indexation, and R15 billion of continuing borrowing. It avoids healthcare and non-age service cuts.",
        "value": "57",
        "unit": "billion constant 2026 rand of targeted pension measures",
        "scenario": "Balanced-transition package",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:POP-005:M01",
        "local_id": "M01",
        "name": "Ageing-austerity package comparison",
        "statement": "The model asks capped levers to close one annual gap and scores five packages on an internal welfare-loss index, political resistance, year-one borrowing, and debt after ten years. Lower index values are better. The scores are not percentages of national wellbeing."
      }
    ],
    "claims": [
      {
        "id": "GSX:POP-005:C01",
        "local_id": "C01",
        "claim": "Among five packages that each close a hypothetical R150 billion annual ageing gap, the balanced transition has the lowest modelled welfare-loss index, 64.5. The low-visible-pain package, which leans on inflation, diffuse cuts, and continuing borrowing, scores 107.3 and leaves about R720 billion of emergency debt after ten years.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-005:A01",
          "GSX:POP-005:A02"
        ],
        "result": "GSX:POP-005:R01",
        "results": [
          "GSX:POP-005:R01",
          "GSX:POP-005:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "The R150 billion gap is a stress test, not a forecast of today's deficit. The welfare scores are internal model indexes, not percentages and not estimates of national wellbeing. The manuscript does not declare any package the single correct answer.",
        "source_study": "GSX:POP-005",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/emergency-ageing-austerity/claims/C01",
        "supported_by": [
          "GSX:POP-005:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-005:C02",
        "local_id": "C02",
        "claim": "The balanced transition in the model closes the gap with R57 billion of targeted pension measures, R24 billion of additional pre-funding, R26 billion of worker tax, R22 billion from a phased retirement-age change, R6 billion of weaker indexation, and R15 billion of continuing borrowing. It does not cut healthcare or non-age services.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-005:A01",
          "GSX:POP-005:A02"
        ],
        "result": "GSX:POP-005:R01",
        "results": [
          "GSX:POP-005:R01",
          "GSX:POP-005:R02"
        ],
        "sensitivity": "moderate",
        "main_limitation": "These are the manuscript's assigned scenario yields for one package. They are not an official budget costing, and a different cap on any lever changes the mix.",
        "source_study": "GSX:POP-005",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/emergency-ageing-austerity/claims/C02",
        "supported_by": [
          "GSX:POP-005:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:POP-012": {
    "assumptions": [
      {
        "id": "GSX:POP-012:A01",
        "local_id": "A01",
        "name": "Common 2050 shock",
        "statement": "The shock combines a severe pandemic, war and security mobilisation, and a recession. The immediate financing need is 14 percent of shocked-year GDP, about R1.23 trillion in constant 2026 rand.",
        "value": "1.23",
        "unit": "trillion constant 2026 rand",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "scenario",
        "sensitivity": "high",
        "alternatives": [
          "A smaller or larger shock"
        ]
      },
      {
        "id": "GSX:POP-012:A02",
        "local_id": "A02",
        "name": "Three governance paths",
        "statement": "The best case is a guardrailed constitutional emergency ending in 2052. The average case is an extended executive emergency to 2058. The worst case is a permanent constitutional suspension that has not ended by 2080.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript Part I and legal-boundary table",
        "evidence_strength": "scenario",
        "sensitivity": "high",
        "alternatives": [
          "A different sunset date"
        ]
      },
      {
        "id": "GSX:POP-012:A03",
        "local_id": "A03",
        "name": "Not legal advice",
        "statement": "A literal suspension of the Constitution is modelled as constitutional rupture, not as an ordinary instrument under section 37.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "legal boundary stated in the manuscript",
        "sensitivity": "high",
        "alternatives": [
          "A path that remains inside section 37"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:POP-012:R01",
        "local_id": "R01",
        "statement": "In the guardrailed case, real output in 2080 is 1.2 percent below the no-shock path. The present value of lost output from 2050 to 2080 is R3.7 trillion.",
        "value": "3.7",
        "unit": "trillion constant 2026 rand, present value of lost output",
        "scenario": "Guardrailed emergency, 2050-2080",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-012:R02",
        "local_id": "R02",
        "statement": "In the extended-executive case, hidden claims rise to 35 percent of GDP, real output ends 21 percent lower, and private pension wealth and youth employment are each 39 percent lower than the comparison stated in the manuscript.",
        "value": "35",
        "unit": "percent of GDP, hidden claims",
        "scenario": "Extended executive emergency to 2058",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-012:R03",
        "local_id": "R03",
        "statement": "In the permanent-suspension case, official debt falls to 70 percent of GDP while hidden pension losses, arrears and deferred maintenance reach 95 percent of GDP. The augmented public burden is 165 percent of GDP. Real output ends 42 percent below the no-shock path, and the present value of output lost after 2050 is R65.8 trillion.",
        "value": "65.8",
        "unit": "trillion constant 2026 rand, present value of lost output",
        "scenario": "Permanent constitutional suspension through 2080",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:POP-012:M01",
        "local_id": "M01",
        "name": "2050 shock and emergency-rule paths",
        "statement": "A common 2050 pandemic, war and recession shock is applied to a hypothetical South-African-scale economy. Three governance paths close the same first-year accounting gap and are followed to 2080."
      }
    ],
    "claims": [
      {
        "id": "GSX:POP-012:C01",
        "local_id": "C01",
        "claim": "Every modelled path closes the first-year accounting gap of about R1.23 trillion. In the guardrailed case that ends in 2052, real output in 2080 is 1.2 percent below the no-shock path and the present value of lost output from 2050 to 2080 is R3.7 trillion.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-012:A01",
          "GSX:POP-012:A02"
        ],
        "result": "GSX:POP-012:R01",
        "results": [
          "GSX:POP-012:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "This is a counterfactual model, not a forecast and not legal advice. Closing the accounting gap does not create the doctors, food, energy, tax capacity or pension wealth that the shock removes.",
        "source_study": "GSX:POP-012",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/extreme-fiscal-pressure/claims/C01",
        "supported_by": [
          "GSX:POP-012:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-012:C02",
        "local_id": "C02",
        "claim": "The extended executive emergency makes the official debt ratio look no worse than the no-shock path by 2080, while hidden claims rise to 35 percent of GDP, real output ends 21 percent lower, and private pension wealth is 39 percent lower.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-012:A01",
          "GSX:POP-012:A02"
        ],
        "result": "GSX:POP-012:R02",
        "results": [
          "GSX:POP-012:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "The official debt ratio is not the full public burden. Hidden claims are part of the manuscript's result.",
        "source_study": "GSX:POP-012",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/extreme-fiscal-pressure/claims/C02",
        "supported_by": [
          "GSX:POP-012:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-012:C03",
        "local_id": "C03",
        "claim": "The permanent-suspension path shows an official debt ratio of 70 percent of GDP together with an augmented public burden of 165 percent of GDP and real output 42 percent below the no-shock path.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-012:A01",
          "GSX:POP-012:A02",
          "GSX:POP-012:A03"
        ],
        "result": "GSX:POP-012:R03",
        "results": [
          "GSX:POP-012:R03"
        ],
        "sensitivity": "high",
        "main_limitation": "The manuscript models this path as constitutional rupture. Apparent success on the official debt ratio is produced by concealing pension losses, arrears and deferred maintenance.",
        "source_study": "GSX:POP-012",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/extreme-fiscal-pressure/claims/C03",
        "supported_by": [
          "GSX:POP-012:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:POP-009": {
    "assumptions": [
      {
        "id": "GSX:POP-009:A01",
        "local_id": "A01",
        "name": "Hypothetical Gauteng-scale city-region",
        "statement": "The model follows a hypothetical region from 2026 to 2076. It starts with 1.2 million people, about 420,000 households, and 430,000 habitable homes. The zones are stylised. They are not labelled real Gauteng neighbourhoods.",
        "value": "1.2",
        "unit": "million people in 2026",
        "type": "model assumption",
        "provenance": "Manuscript central scenario",
        "evidence_strength": "illustrative",
        "sensitivity": "high",
        "alternatives": [
          "A different household-size path",
          "Faster or slower population decline"
        ]
      },
      {
        "id": "GSX:POP-009:A02",
        "local_id": "A02",
        "name": "Central shrinkage path",
        "statement": "In the central scenario, population falls by 0.5 percent a year and average household size falls from 2.86 to 2.15.",
        "value": "0.5",
        "unit": "percent population decline per year",
        "type": "model assumption",
        "provenance": "Manuscript central scenario",
        "evidence_strength": "scenario",
        "sensitivity": "high",
        "alternatives": [
          "Stable household size"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:POP-009:R01",
        "local_id": "R01",
        "statement": "By 2076 the region has 934,000 people and 434,000 households. Population is 22.2 percent smaller and the number of households is 3.5 percent larger. Misallocated construction and repairs can leave a shortage of roughly 54,000 habitable homes.",
        "value": "54000",
        "unit": "habitable homes short in 2076",
        "scenario": "Central scenario, deteriorating stock and misallocated repairs",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-009:R02",
        "local_id": "R02",
        "statement": "Managed shrinkage keeps school-seat use near 82 percent rather than 47 percent and reduces the fifty-year present value of the modelled system bill from R384.8 billion to R366.2 billion. Under delayed adjustment, satellite and outer-edge coverage fall to 41 and 72 percent by 2076.",
        "value": "366.2",
        "unit": "billion constant rand, fifty-year present value under managed shrinkage",
        "scenario": "Managed shrinkage compared with delayed adjustment",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:POP-009:M01",
        "local_id": "M01",
        "name": "Shrinking city-region accounts",
        "statement": "The model separates population, households, school-age children, and network length across four zones. Housing demand follows households. School demand follows children. Infrastructure cost follows the network, not only the litres sold."
      }
    ],
    "claims": [
      {
        "id": "GSX:POP-009:C01",
        "local_id": "C01",
        "claim": "In the central scenario, a 22.2 percent population decline by 2076 coincides with 3.5 percent more households. The same run can still produce a shortage of roughly 54,000 habitable homes after the city has lost 266,000 people.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-009:A01",
          "GSX:POP-009:A02"
        ],
        "result": "GSX:POP-009:R01",
        "results": [
          "GSX:POP-009:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "This is a hypothetical region, not a forecast for a named Gauteng municipality. Housing demand follows households, so a falling headcount is not itself a falling housing demand. The shortage also depends on the stock deteriorating and on repairs being misallocated.",
        "source_study": "GSX:POP-009",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/how-to-shrink-a-country-without-breaking-it/claims/C01",
        "supported_by": [
          "GSX:POP-009:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-009:C02",
        "local_id": "C02",
        "claim": "Managed shrinkage in the model keeps school-seat use near 82 percent rather than 47 percent and lowers the fifty-year present value of the modelled system bill from R384.8 billion to R366.2 billion.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-009:A01",
          "GSX:POP-009:A02"
        ],
        "result": "GSX:POP-009:R02",
        "results": [
          "GSX:POP-009:R02"
        ],
        "sensitivity": "moderate",
        "main_limitation": "The rand saving is not the whole argument. Delayed adjustment leaves the satellite town and outer edge at 41 and 72 percent maintenance coverage by 2076 while the centre stays above cost. Uniform policy can transfer money from viable networks to networks that no longer have enough users.",
        "source_study": "GSX:POP-009",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/how-to-shrink-a-country-without-breaking-it/claims/C02",
        "supported_by": [
          "GSX:POP-009:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:POP-008": {
    "assumptions": [
      {
        "id": "GSX:POP-008:A01",
        "local_id": "A01",
        "name": "Same R1 million, different arrival age",
        "statement": "The model compares one R1 million transfer received at 40, 55, 70, or 85, plus a living transfer at 35. If it stays invested until age 100, only the arrival age and the real return change. The illustrated values exclude tax, fees, and consumption.",
        "value": "1000000",
        "unit": "constant 2026 rand transferred",
        "type": "model assumption",
        "provenance": "Manuscript timing map",
        "evidence_strength": "illustrative",
        "sensitivity": "high",
        "alternatives": [
          "2 percent real return",
          "6 percent real return",
          "The heir consumes part of the transfer"
        ]
      },
      {
        "id": "GSX:POP-008:A02",
        "local_id": "A02",
        "name": "Average return and starting pay",
        "statement": "The recipient starts work at 25 on R30,000 a month. Real pay grows by 1.2 percent a year. Capital earns 4 percent above inflation in the average case. Values are constant 2026 rand.",
        "value": "4",
        "unit": "percent real return per year",
        "type": "model assumption",
        "provenance": "Manuscript average case",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "2 percent real",
          "6 percent real"
        ]
      },
      {
        "id": "GSX:POP-008:A03",
        "local_id": "A03",
        "name": "Clean compounding case",
        "statement": "If parents and children earn the same return, pay no tax, never consume the asset, and can borrow freely, family wealth does not depend on which generation legally holds the capital.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript qualification",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "Deposit constraints, expensive credit, tax, and consumption"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:POP-008:R01",
        "local_id": "R01",
        "statement": "At 4 percent real, R1 million kept invested until age 100 becomes R12.80 million if received at 35, R10.52 million at 40, R5.84 million at 55, R3.24 million at 70, and R1.80 million at 85.",
        "value": "10.52",
        "unit": "million constant 2026 rand at age 100, inheritance at 40",
        "scenario": "Average 4 percent real return, no tax, fees, or consumption",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-008:R02",
        "local_id": "R02",
        "statement": "The same inheritance received at 40 is worth R3.28 million by age 100 at 2 percent real and R32.99 million at 6 percent real. Received at 85, those three returns narrow to R1.35 million, R1.80 million, and R2.40 million.",
        "value": "32.99",
        "unit": "million constant 2026 rand at age 100, 6 percent, received at 40",
        "scenario": "Return sensitivity at ages 40 and 85",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:POP-008:M01",
        "local_id": "M01",
        "name": "Inheritance timing map",
        "statement": "One transfer is compounded to age 100 under alternative arrival ages and real returns. The map isolates timing. It does not estimate the current South African age at which people inherit."
      }
    ],
    "claims": [
      {
        "id": "GSX:POP-008:C01",
        "local_id": "C01",
        "claim": "If R1 million remains invested until age 100 at 4 percent above inflation, a living transfer at 35 becomes R12.80 million, an inheritance at 40 becomes R10.52 million, at 55 R5.84 million, at 70 R3.24 million, and at 85 R1.80 million, in constant 2026 rand.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-008:A01",
          "GSX:POP-008:A02"
        ],
        "result": "GSX:POP-008:R01",
        "results": [
          "GSX:POP-008:R01",
          "GSX:POP-008:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "These values exclude tax, fees, and consumption so that timing stays visible. The manuscript does not claim that 70 is today's average age of inheritance in South Africa. If the heir spends the money, or if returns differ by owner, the age-100 values do not apply.",
        "source_study": "GSX:POP-008",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/inheritance-after-retirement/claims/C01",
        "supported_by": [
          "GSX:POP-008:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-008:C02",
        "local_id": "C02",
        "claim": "Under equal returns, no tax, no consumption, and free borrowing, the same family wealth results wherever the capital sits. Timing still changes what a young adult can do, because a transfer at 35 or 40 can meet a deposit, debt, education, or career constraint that a transfer at 70 or 85 arrives too late to change.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-008:A01",
          "GSX:POP-008:A03"
        ],
        "result": "GSX:POP-008:R01",
        "results": [
          "GSX:POP-008:R01"
        ],
        "sensitivity": "moderate",
        "main_limitation": "The second statement is the manuscript's qualification of the pure compounding result. It is not a measured rand gap for every family. Control, tax, and credit constraints are the reasons timing matters once the clean case is dropped.",
        "source_study": "GSX:POP-008",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/inheritance-after-retirement/claims/C02",
        "supported_by": [
          "GSX:POP-008:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:WPL-001": {
    "assumptions": [
      {
        "id": "GSX:WPL-001:A01",
        "local_id": "A01",
        "name": "Matched descendants",
        "statement": "The modelled descendants share education, real salary, household size and saving behaviour. The property condition changes.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript modelled answer",
        "evidence_strength": "model design",
        "sensitivity": "high",
        "alternatives": [
          "Different earnings or saving behaviour"
        ]
      },
      {
        "id": "GSX:WPL-001:A02",
        "local_id": "A02",
        "name": "No identified causal share",
        "statement": "No national source follows an inherited property from parent to heir while jointly observing population group, title, location, competing claims, marketability and later wealth.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "data limit",
        "sensitivity": "high",
        "alternatives": [
          "A linked inheritance register"
        ]
      },
      {
        "id": "GSX:WPL-001:A03",
        "local_id": "A03",
        "name": "Observed wealth benchmarks",
        "statement": "In 2017 NIDS data cited by the manuscript, median Black household net worth was about R70,100 and median White household net worth was R1,364,900.",
        "value": "70100",
        "unit": "rand, 2017 median Black household net worth",
        "type": "model assumption",
        "provenance": "Manuscript descriptive answer, citing Chelwa, Maboshe and Hamilton (2024)",
        "evidence_strength": "cited survey statistic",
        "sensitivity": "moderate",
        "alternatives": [
          "A later wealth survey"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:WPL-001:R01",
        "local_id": "R01",
        "statement": "In the central Monte Carlo case, median marketable net worth after forty years is R3.04 million with no inherited property, R3.15 million with a communal family residence, R3.67 million with a titled township home, R5.24 million with a middle-value suburban home, R10.59 million with high-value property and R6.51 million with a productive farm, in constant 2024 rand.",
        "value": "5.24",
        "unit": "million constant 2024 rand, middle-value suburban median",
        "scenario": "Central Monte Carlo case, forty years",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:WPL-001:R02",
        "local_id": "R02",
        "statement": "The modelled gap between the titled-township and middle-suburb medians is R1.57 million. The gap between the communal-residence and high-property cases is R7.44 million.",
        "value": "1.57",
        "unit": "million constant 2024 rand",
        "scenario": "Central case differences after forty years",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:WPL-001:M01",
        "local_id": "M01",
        "name": "Matched-descendant property scenarios",
        "statement": "Descendants with the same education, real salary, household size and saving behaviour receive different inherited property conditions. The central case is a Monte Carlo scenario in constant 2024 rand over forty years."
      }
    ],
    "claims": [
      {
        "id": "GSX:WPL-001:C01",
        "local_id": "C01",
        "claim": "For matched descendants, the central scenario produces median marketable net worth after forty years of R3.67 million with a titled township home and R5.24 million with a middle-value suburban home. The difference is R1.57 million, in constant 2024 rand.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:WPL-001:A01"
        ],
        "result": "GSX:WPL-001:R01",
        "results": [
          "GSX:WPL-001:R01",
          "GSX:WPL-001:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "These are scenarios, not forecasts and not estimates for a racial group. The comparison shows that inherited property conditions can be large enough to matter. It does not show what share of the national wealth gap that mechanism causes.",
        "source_study": "GSX:WPL-001",
        "version": "1.0",
        "href": "https://greyscienx.com/research/wealth-and-place/inherited-geography/claims/C01",
        "supported_by": [
          "GSX:WPL-001:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:WPL-001:C02",
        "local_id": "C02",
        "claim": "The manuscript states that the causal share of the racial wealth gap attributable to inherited property geography cannot be identified from currently available data.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:WPL-001:A02",
          "GSX:WPL-001:A03"
        ],
        "result": "GSX:WPL-001:R02",
        "results": [
          "GSX:WPL-001:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "There is no core causal estimate. Observed gaps, probate records and the matched model answer different questions and are not averaged into one percentage.",
        "source_study": "GSX:WPL-001",
        "version": "1.0",
        "href": "https://greyscienx.com/research/wealth-and-place/inherited-geography/claims/C02",
        "supported_by": [
          "GSX:WPL-001:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:AFR-002": {
    "assumptions": [
      {
        "id": "GSX:AFR-002:A01",
        "local_id": "A01",
        "name": "Central hub shares",
        "statement": "Forty percent of gross capital formation is treated as institutionally or externally financeable. Johannesburg arranges, distributes, services or manages 8 percent of that pool.",
        "value": "8",
        "unit": "percent of the financeable pool",
        "type": "model assumption",
        "provenance": "Manuscript central regional-hub scenario",
        "evidence_strength": "scenario",
        "sensitivity": "high",
        "alternatives": [
          "A lower capture share"
        ]
      },
      {
        "id": "GSX:AFR-002:A02",
        "local_id": "A02",
        "name": "Starting financial depth",
        "statement": "The manuscript cites JSE market capitalisation of R24.18 trillion at the end of 2025 and banking-sector assets of R8.45 trillion in June 2025.",
        "value": "24.18",
        "unit": "trillion rand of JSE market capitalisation at end-2025",
        "type": "model assumption",
        "provenance": "Manuscript Part I, citing the JSE and SARB",
        "evidence_strength": "cited market statistic",
        "sensitivity": "low",
        "alternatives": [
          "A later exchange or banking report"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:AFR-002:R01",
        "local_id": "R01",
        "statement": "Under the central hub scenario, captured flow is approximately US$1.30 trillion. Fees and spreads produce about US$90.4 billion of cumulative financial-services revenue.",
        "value": "90.4",
        "unit": "billion US dollars of cumulative revenue",
        "scenario": "Central regional hub, 2026-2050",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:AFR-002:R02",
        "local_id": "R02",
        "statement": "About US$71.2 billion is retained as domestic value, US$2.85 billion a year on average, with roughly 15,800 direct jobs and 25,300 direct and indirect jobs.",
        "value": "71.2",
        "unit": "billion US dollars retained",
        "scenario": "Central hub after foreign inputs and offshore delivery",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:AFR-002:M01",
        "local_id": "M01",
        "name": "Regional-hub financial-services model",
        "statement": "The model takes a constructed path for African gross capital formation, treats part of it as financeable, applies a Johannesburg capture share, and converts captured flow into fees and retained value."
      }
    ],
    "claims": [
      {
        "id": "GSX:AFR-002:C01",
        "local_id": "C01",
        "claim": "In the central regional-hub scenario, an 8 percent capture share produces about US$90.4 billion of cumulative financial-services revenue and about US$71.2 billion of value retained in South Africa.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:AFR-002:A01"
        ],
        "result": "GSX:AFR-002:R01",
        "results": [
          "GSX:AFR-002:R01",
          "GSX:AFR-002:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "The captured flow is not South African GDP. The paths are constructed, not forecasts. Financial intermediation does not replace weak electricity, logistics, education or public institutions.",
        "source_study": "GSX:AFR-002",
        "version": "1.0",
        "href": "https://greyscienx.com/research/african-convergence/johannesburg-as-africas-financial-capital/claims/C01",
        "supported_by": [
          "GSX:AFR-002:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:AFR-002:C02",
        "local_id": "C02",
        "claim": "The manuscript's objective is retained financial value from African investment even when the project, issuer, investor or consumer is elsewhere. Inherited market depth does not by itself protect that role.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:AFR-002:A01",
          "GSX:AFR-002:A02"
        ],
        "result": "GSX:AFR-002:R02",
        "results": [
          "GSX:AFR-002:R02"
        ],
        "sensitivity": "moderate",
        "main_limitation": "A large transaction routed through Johannesburg can leave little domestic income if the structuring, insurance, domicile and investors sit abroad.",
        "source_study": "GSX:AFR-002",
        "version": "1.0",
        "href": "https://greyscienx.com/research/african-convergence/johannesburg-as-africas-financial-capital/claims/C02",
        "supported_by": [
          "GSX:AFR-002:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:AFR-001": {
    "assumptions": [
      {
        "id": "GSX:AFR-001:A01",
        "local_id": "A01",
        "name": "Conditional growth rates",
        "statement": "The central scenario assumes the rest of Africa sustains 4.2 percent annual real growth from 2024 to 2050 while South Africa grows at 3.5 percent.",
        "value": "3.5",
        "unit": "percent annual real growth, South Africa",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "scenario",
        "sensitivity": "high",
        "alternatives": [
          "A path that merely holds the present GDP share"
        ]
      },
      {
        "id": "GSX:AFR-001:A02",
        "local_id": "A02",
        "name": "Starting shares",
        "statement": "In 2024 South Africa contained about 4.2 percent of Africa's population and produced roughly 13.8 percent of the continent's measured GDP in current US dollars.",
        "value": "13.8",
        "unit": "percent of African GDP in 2024",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "observed starting point cited by the manuscript",
        "sensitivity": "low",
        "alternatives": [
          "A different base year"
        ]
      },
      {
        "id": "GSX:AFR-001:A03",
        "local_id": "A03",
        "name": "Platform-income share",
        "statement": "The platform strategy sets income retained by South African workers, firms and investors from the rest of Africa at 1.5 percent of that larger continental economy. It is not added mechanically to GDP.",
        "value": "1.5",
        "unit": "percent of the rest of Africa's economy",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "scenario",
        "sensitivity": "high",
        "alternatives": [
          "A lower retained share"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:AFR-001:R01",
        "local_id": "R01",
        "statement": "South African GDP more than doubles in real terms to about US$981 billion, real GDP per person rises by roughly 109 percent, and the share of African GDP falls from 13.8 to 11.9 percent.",
        "value": "981",
        "unit": "billion US dollars of South African GDP",
        "scenario": "Central scenario, 2050",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:AFR-001:R02",
        "local_id": "R02",
        "statement": "At a 1.5 percent retained share, the annual platform flow is about US$109 billion in 2050. In the platform scenario the manuscript also reports real economic growth of roughly 145 percent while the continental GDP share falls by two percentage points.",
        "value": "109",
        "unit": "billion US dollars in 2050",
        "scenario": "African-platform income flow",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:AFR-001:M01",
        "local_id": "M01",
        "name": "Continental growth and platform-income scenario",
        "statement": "The model holds a conditional African growth path and a South African growth path, then separates GDP rank from a platform-income flow."
      }
    ],
    "claims": [
      {
        "id": "GSX:AFR-001:C01",
        "local_id": "C01",
        "claim": "If the rest of Africa grows at 4.2 percent and South Africa at 3.5 percent, the manuscript's central scenario has South African GDP at about US$981 billion, real GDP per person up roughly 109 percent, and the continental GDP share down from 13.8 to 11.9 percent.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:AFR-001:A01",
          "GSX:AFR-001:A02"
        ],
        "result": "GSX:AFR-001:R01",
        "results": [
          "GSX:AFR-001:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "This is a conditional scenario, not a forecast that African convergence will happen. A falling rank is not a fall in South African income.",
        "source_study": "GSX:AFR-001",
        "version": "1.0",
        "href": "https://greyscienx.com/research/african-convergence/south-africa-in-a-richer-africa/claims/C01",
        "supported_by": [
          "GSX:AFR-001:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:AFR-001:C02",
        "local_id": "C02",
        "claim": "If South African-linked income from the rest of Africa reaches 1.5 percent of that larger economy, the annual flow is about US$109 billion in 2050. The manuscript does not add that flow on top of GDP.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:AFR-001:A03"
        ],
        "result": "GSX:AFR-001:R02",
        "results": [
          "GSX:AFR-001:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "Gross exports, brass-plate headquarters and outward investment can fail to retain income. The strategy is judged by retained value.",
        "source_study": "GSX:AFR-001",
        "version": "1.0",
        "href": "https://greyscienx.com/research/african-convergence/south-africa-in-a-richer-africa/claims/C02",
        "supported_by": [
          "GSX:AFR-001:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:IND-005": {
    "assumptions": [
      {
        "id": "GSX:IND-005:A01",
        "local_id": "A01",
        "name": "Central manufacturing path",
        "statement": "In the central catch-up case, African manufacturing value added grows from a rounded US$300 billion in 2025 to about US$1.14 trillion in 2050. Factory-equipment purchases average 24 percent of manufacturing value added.",
        "value": "24",
        "unit": "percent of manufacturing value added spent on factory equipment",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "scenario",
        "sensitivity": "high",
        "alternatives": [
          "Drift case",
          "Industrial-surge case"
        ]
      },
      {
        "id": "GSX:IND-005:A02",
        "local_id": "A02",
        "name": "South African share",
        "statement": "The central portfolio uses a weighted 6.7 percent South African share of equipment demand, with category shares from 3 to 10 percent.",
        "value": "6.7",
        "unit": "percent of equipment demand",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "scenario share",
        "sensitivity": "high",
        "alternatives": [
          "A lower or higher share"
        ]
      },
      {
        "id": "GSX:IND-005:A03",
        "local_id": "A03",
        "name": "Lifecycle ratios",
        "statement": "Spares, maintenance and refurbishment equal 4.5 percent of the surviving installed base each year. Software, training and finance add 1.8 percent.",
        "value": "4.5",
        "unit": "percent of the surviving installed base per year",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "scenario ratio",
        "sensitivity": "moderate",
        "alternatives": [
          "A different service intensity"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:IND-005:R01",
        "local_id": "R01",
        "statement": "The central case produces a cumulative capital-goods market of US$3.89 trillion and about US$262 billion of South African equipment sales over twenty-five years, in constant 2024 dollars.",
        "value": "262",
        "unit": "billion constant 2024 US dollars of equipment sales",
        "scenario": "Central catch-up case, 2026-2050",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:IND-005:R02",
        "local_id": "R02",
        "statement": "Lifecycle revenue is about US$105 billion. Cumulative value retained in South Africa is approximately US$201 billion, about US$8.0 billion a year on average, with an illustrative 80,000 direct jobs.",
        "value": "201",
        "unit": "billion constant 2024 US dollars retained in South Africa",
        "scenario": "Central case after removing non-South-African inputs",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:IND-005:M01",
        "local_id": "M01",
        "name": "African capital-goods scale test",
        "statement": "The model follows three African manufacturing paths from 2026 to 2050, applies equipment-purchase ratios and South African market shares, then adds lifecycle revenue and removes imported or non-South-African inputs."
      }
    ],
    "claims": [
      {
        "id": "GSX:IND-005:C01",
        "local_id": "C01",
        "claim": "In the central catch-up case, a weighted 6.7 percent equipment share produces about US$262 billion of South African equipment sales over twenty-five years and about US$201 billion of value retained in South Africa.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:IND-005:A01",
          "GSX:IND-005:A02",
          "GSX:IND-005:A03"
        ],
        "result": "GSX:IND-005:R01",
        "results": [
          "GSX:IND-005:R01",
          "GSX:IND-005:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "The paths are scenarios, not forecasts, and the retained value cannot be added mechanically to a GDP forecast. Some of this activity already exists. The result is a scale test of a selected machinery and service position, not a claim that South Africa should make every final product.",
        "source_study": "GSX:IND-005",
        "version": "1.0",
        "href": "https://greyscienx.com/research/strategic-industrialisation/the-capital-goods-economy/claims/C01",
        "supported_by": [
          "GSX:IND-005:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:IND-005:C02",
        "local_id": "C02",
        "claim": "Under the drift case, cumulative equipment demand is US$1.80 trillion. The industrial-surge case reaches US$7.11 trillion. The opportunity depends on African industrialisation actually occurring.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:IND-005:A01"
        ],
        "result": "GSX:IND-005:R01",
        "results": [
          "GSX:IND-005:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "Demography alone does not buy machines. The domestic machinery base is also described as eroding, so the share is not assured.",
        "source_study": "GSX:IND-005",
        "version": "1.0",
        "href": "https://greyscienx.com/research/strategic-industrialisation/the-capital-goods-economy/claims/C02",
        "supported_by": [
          "GSX:IND-005:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:AFR-003": {
    "assumptions": [
      {
        "id": "GSX:AFR-003:A01",
        "local_id": "A01",
        "name": "Urban anchor",
        "statement": "The demographic anchor is a rise from roughly 700 million urban residents to 1.4 billion by 2050. The manuscript attributes the trajectory to UN-Habitat and the United Nations, not to a GreyScienx population forecast.",
        "value": "700",
        "unit": "million additional urban residents",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "external demographic trajectory used as a scenario anchor",
        "sensitivity": "moderate",
        "alternatives": [
          "A slower urbanisation path"
        ]
      },
      {
        "id": "GSX:AFR-003:A02",
        "local_id": "A02",
        "name": "Contestable share and retention",
        "statement": "About US$7.1 trillion of the central market is treated as contestable by external suppliers. The retention case keeps 52 percent of captured sales as South African value added.",
        "value": "52",
        "unit": "percent of captured sales retained",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "scenario",
        "sensitivity": "high",
        "alternatives": [
          "A lower retention rate"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:AFR-003:R01",
        "local_id": "R01",
        "statement": "The central scenario is US$17.9 trillion of all-in urban capital formation. Captured South African-linked gross sales are US$264 billion.",
        "value": "264",
        "unit": "billion constant 2024 US dollars of gross sales",
        "scenario": "Central build-out, 2026-2050",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:AFR-003:R02",
        "local_id": "R02",
        "statement": "Domestic value added is about US$137 billion over twenty-five years, US$5.5 billion a year on average, with an illustrative 65,000 direct jobs.",
        "value": "137",
        "unit": "billion constant 2024 US dollars of domestic value added",
        "scenario": "Central case, 52 percent retention",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:AFR-003:M01",
        "local_id": "M01",
        "name": "Urban build-out supplier model",
        "statement": "The model turns an additional 700 million urban residents into an all-in capital-formation envelope, removes intrinsically local spending, applies sector shares, and retains a stated fraction as South African value."
      }
    ],
    "claims": [
      {
        "id": "GSX:AFR-003:C01",
        "local_id": "C01",
        "claim": "In the central build-out, South African-linked firms record US$264 billion of cumulative gross sales and about US$137 billion of domestic value added over twenty-five years.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:AFR-003:A01",
          "GSX:AFR-003:A02"
        ],
        "result": "GSX:AFR-003:R01",
        "results": [
          "GSX:AFR-003:R01",
          "GSX:AFR-003:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "The envelope is a constructed scenario, not an official infrastructure estimate, and it includes private buildings. The employment numbers are scale indicators, not forecasts. A 1.4 percent of GDP level effect is not a permanent 1.4 percentage-point addition to annual growth.",
        "source_study": "GSX:AFR-003",
        "version": "1.0",
        "href": "https://greyscienx.com/research/african-convergence/the-factory-for-african-urbanisation/claims/C01",
        "supported_by": [
          "GSX:AFR-003:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:AFR-003:C02",
        "local_id": "C02",
        "claim": "The supplier position in the manuscript is equipment, engineering, finance, standards and maintenance, with bulky production placed near demand. The basic-provision case is US$8.5 trillion and the convergence case is US$32.2 trillion.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:AFR-003:A01"
        ],
        "result": "GSX:AFR-003:R01",
        "results": [
          "GSX:AFR-003:R01"
        ],
        "sensitivity": "moderate",
        "main_limitation": "Most urban spending is local. Housing is a large market and a smaller external-supplier opportunity. An unreliable domestic port, grid or rail system can erase the geographic advantage.",
        "source_study": "GSX:AFR-003",
        "version": "1.0",
        "href": "https://greyscienx.com/research/african-convergence/the-factory-for-african-urbanisation/claims/C02",
        "supported_by": [
          "GSX:AFR-003:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:HH-002": {
    "assumptions": [
      {
        "id": "GSX:HH-002:A01",
        "local_id": "A01",
        "name": "Representative worker",
        "statement": "The central case is a 22-year-old worker in Johannesburg, expressed in constant 2026 rand.",
        "value": "22",
        "unit": "years at the start",
        "type": "model assumption",
        "provenance": "Manuscript central scenario",
        "evidence_strength": "illustrative",
        "sensitivity": "high",
        "alternatives": [
          "Lower salary case",
          "Higher salary case",
          "Cape Town rent scenario",
          "Durban rent scenario"
        ]
      },
      {
        "id": "GSX:HH-002:A02",
        "local_id": "A02",
        "name": "Middle starting salary",
        "statement": "The central worker earns R420,000 a year before tax. The manuscript also reports a lower case of R240,000 and a higher case of R720,000. These are illustrative starting salaries, not national percentiles.",
        "value": "420000",
        "unit": "constant 2026 rand per year, gross",
        "type": "model assumption",
        "provenance": "Manuscript earnings cases",
        "evidence_strength": "illustrative",
        "sensitivity": "high",
        "alternatives": [
          "240000",
          "720000"
        ]
      },
      {
        "id": "GSX:HH-002:A03",
        "local_id": "A03",
        "name": "Johannesburg housing bundle",
        "statement": "Independent housing in the Johannesburg scenario costs R9,600 a month in rent and R7,200 a month in other housing basics. The manuscript treats these as transparent city scenarios, not estimated city means.",
        "value": "9600",
        "unit": "constant 2026 rand per month, rent",
        "type": "model assumption",
        "provenance": "Manuscript city scenario, with the rent scale anchored on a published Gauteng rental average",
        "evidence_strength": "scenario",
        "sensitivity": "high",
        "alternatives": [
          "Cape Town rent R12,500",
          "Durban rent R9,400",
          "Johannesburg rent 30% lower"
        ]
      },
      {
        "id": "GSX:HH-002:A04",
        "local_id": "A04",
        "name": "Contribution while living at home",
        "statement": "While living in the family home, the worker contributes 12% of take-home pay, bounded between R2,500 and R6,000 a month, plus R1,200 of personal food and services. The manuscript counts this transfer as a private cost.",
        "value": "12",
        "unit": "percent of take-home pay",
        "type": "model assumption",
        "provenance": "Manuscript household rule",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "Contribution of about R15,900 a month, where the home-only advantage disappears"
        ]
      },
      {
        "id": "GSX:HH-002:A05",
        "local_id": "A05",
        "name": "Financed used car",
        "statement": "The car is a R230,000 used vehicle with a 10% deposit and 60-month finance at 11.5%, plus insurance, parking, fuel, maintenance, and depreciation as specified in the manuscript.",
        "value": "230000",
        "unit": "constant 2026 rand, purchase price",
        "type": "model assumption",
        "provenance": "Manuscript vehicle case",
        "evidence_strength": "model assumption",
        "sensitivity": "moderate",
        "alternatives": [
          "Vehicle costing R160,000"
        ]
      },
      {
        "id": "GSX:HH-002:A06",
        "local_id": "A06",
        "name": "Hybrid transport while the car is delayed",
        "statement": "Delaying the car uses a public-transport and ride-hailing mix. In the central case the worker travels about 640 kilometres a month.",
        "value": "640",
        "unit": "kilometres per month",
        "type": "model assumption",
        "provenance": "Manuscript hybrid transport case",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "25% ride-hailing surge",
          "More office days",
          "A family home far from work"
        ]
      },
      {
        "id": "GSX:HH-002:A07",
        "local_id": "A07",
        "name": "Common path after age 25",
        "statement": "At age 25 every strategy has moved out and acquired the modelled car. From then on the paths share the same real salary growth, a 10% retirement saving rate, and a 5% real investment return.",
        "value": "5",
        "unit": "percent real return per year",
        "type": "model assumption",
        "provenance": "Manuscript post-25 boundary",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "3% real return",
          "7% real return"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:HH-002:R01",
        "local_id": "R01",
        "statement": "Moving out and buying the car immediately leaves a modelled funding shortfall of R49,000 at age 25 in the central case.",
        "value": "-49000",
        "unit": "constant 2026 rand",
        "scenario": "Middle salary, Johannesburg, immediate independence",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:HH-002:R02",
        "local_id": "R02",
        "statement": "Delaying the move and the car for three years leaves R553,000 of modelled net capital at age 25 in the central case.",
        "value": "553000",
        "unit": "constant 2026 rand",
        "scenario": "Middle salary, Johannesburg, three-year delay",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:HH-002:R03",
        "local_id": "R03",
        "statement": "The central three-year combined delay creates R602,000 more modelled net capital at age 25 than immediate independence.",
        "value": "602000",
        "unit": "constant 2026 rand",
        "scenario": "Middle salary, Johannesburg, three-year delay minus immediate independence",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:HH-002:R04",
        "local_id": "R04",
        "statement": "If that age-25 gap is preserved on the common post-25 path, the manuscript reports R3.32 million more modelled wealth at age 60.",
        "value": "3320000",
        "unit": "constant 2026 rand",
        "scenario": "Middle salary, Johannesburg, gap carried to age 60 at a 5% real return",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:HH-002:R05",
        "local_id": "R05",
        "statement": "Staying at home for three years while buying the car immediately creates R486,000 more modelled capital by age 25. Moving out immediately while delaying the car creates R128,000.",
        "value": "486000",
        "unit": "constant 2026 rand, housing-delay gap at age 25",
        "scenario": "Middle salary, Johannesburg, housing delay versus car delay",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:HH-002:R06",
        "local_id": "R06",
        "statement": "The modelled three-year home-only advantage disappears at a household contribution of roughly R15,900 a month.",
        "value": "15900",
        "unit": "constant 2026 rand per month",
        "scenario": "Middle salary, Johannesburg, contribution break-even",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:HH-002:R07",
        "local_id": "R07",
        "statement": "Under the central hybrid mix, a financed used car has a lower private monthly money cost only above roughly 2,405 kilometres a month. A 25% ride-hailing surge lowers that threshold to about 1,585 kilometres.",
        "value": "2405",
        "unit": "kilometres per month",
        "scenario": "Central hybrid transport, private money cost",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:HH-002:M01",
        "local_id": "M01",
        "name": "First-three-years household budget",
        "statement": "The model follows the first 36 months in monthly detail, covering salary, tax, household contribution, housing, transport, moving costs, and vehicle finance. At month 36 every strategy has moved out and acquired the modelled car. A common salary, saving, and return path then carries the age-25 gap forward. Differences at age 60 are attributed to the first three years."
      }
    ],
    "claims": [
      {
        "id": "GSX:HH-002:C01",
        "local_id": "C01",
        "claim": "In the central middle-salary Johannesburg scenario, living in the family home and delaying a car purchase for three years creates R602,000 more modelled net capital at age 25, and R3.32 million more modelled wealth at age 60, than moving out and financing a car immediately. The age-60 figure holds when the gap is preserved on the manuscript's common post-25 path.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:HH-002:A01",
          "GSX:HH-002:A02",
          "GSX:HH-002:A03",
          "GSX:HH-002:A04",
          "GSX:HH-002:A05",
          "GSX:HH-002:A06",
          "GSX:HH-002:A07"
        ],
        "result": "GSX:HH-002:R01",
        "results": [
          "GSX:HH-002:R01",
          "GSX:HH-002:R02",
          "GSX:HH-002:R03",
          "GSX:HH-002:R04"
        ],
        "sensitivity": "high",
        "main_limitation": "This is a modelled counterfactual for one representative worker, not a forecast and not a statement that every graduate can or should live at home. The age-60 level includes a common 10% retirement-saving path. The manuscript treats the gap between strategies as the robust quantity, and the level as a scale illustration.",
        "source_study": "GSX:HH-002",
        "version": "1.0",
        "href": "https://greyscienx.com/research/household-economics/the-first-three-years-advantage/claims/C01",
        "supported_by": [
          "GSX:HH-002:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:HH-002:C02",
        "local_id": "C02",
        "claim": "In the central case, staying at home for three years while buying the car immediately accounts for R486,000 of extra modelled capital at age 25, while moving out immediately and delaying the car accounts for R128,000. The housing decision is the larger of the two.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:HH-002:A01",
          "GSX:HH-002:A02",
          "GSX:HH-002:A03",
          "GSX:HH-002:A04",
          "GSX:HH-002:A05",
          "GSX:HH-002:A06"
        ],
        "result": "GSX:HH-002:R05",
        "results": [
          "GSX:HH-002:R05"
        ],
        "sensitivity": "high",
        "main_limitation": "The two effects overlap slightly when they are combined, because interest on positive and negative balances differs. The split is a central-scenario comparison, not a rule for every city, salary, or commute.",
        "source_study": "GSX:HH-002",
        "version": "1.0",
        "href": "https://greyscienx.com/research/household-economics/the-first-three-years-advantage/claims/C02",
        "supported_by": [
          "GSX:HH-002:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:HH-002:C03",
        "local_id": "C03",
        "claim": "The modelled advantage of three years in the family home disappears when the household contribution reaches roughly R15,900 a month in the middle-income Johannesburg case.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:HH-002:A01",
          "GSX:HH-002:A02",
          "GSX:HH-002:A03",
          "GSX:HH-002:A04"
        ],
        "result": "GSX:HH-002:R06",
        "results": [
          "GSX:HH-002:R06"
        ],
        "sensitivity": "high",
        "main_limitation": "The threshold is a diagnostic for this scenario. The manuscript does not present it as a fair-rent recommendation. A higher contribution can still be the right family choice while no longer raising the worker's private wealth.",
        "source_study": "GSX:HH-002",
        "version": "1.0",
        "href": "https://greyscienx.com/research/household-economics/the-first-three-years-advantage/claims/C03",
        "supported_by": [
          "GSX:HH-002:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:HH-002:C04",
        "local_id": "C04",
        "claim": "Under the central hybrid transport mix, the financed used car has a lower private monthly money cost only above roughly 2,405 kilometres a month.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:HH-002:A05",
          "GSX:HH-002:A06"
        ],
        "result": "GSX:HH-002:R07",
        "results": [
          "GSX:HH-002:R07"
        ],
        "sensitivity": "high",
        "main_limitation": "The comparison is private money cost. It does not price safety, reliability, waiting, shift work, or access to a job. A 25% ride-hailing surge moves the modelled threshold to about 1,585 kilometres a month.",
        "source_study": "GSX:HH-002",
        "version": "1.0",
        "href": "https://greyscienx.com/research/household-economics/the-first-three-years-advantage/claims/C04",
        "supported_by": [
          "GSX:HH-002:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:POP-007": {
    "assumptions": [
      {
        "id": "GSX:POP-007:A01",
        "local_id": "A01",
        "name": "Extended healthy adulthood",
        "statement": "The scenario asks what changes if people routinely live to 100 or 120 with a substantial extension of healthy adult life. Current South African life expectancy is far shorter. This is not a projection that the average person will soon live to 120.",
        "value": "120",
        "unit": "years, scenario lifespan",
        "type": "model assumption",
        "provenance": "Manuscript scenario design",
        "evidence_strength": "illustrative",
        "sensitivity": "high",
        "alternatives": [
          "Death postponed more than illness",
          "A conventional life to a shorter age"
        ]
      },
      {
        "id": "GSX:POP-007:A02",
        "local_id": "A02",
        "name": "Common starting pay and saving",
        "statement": "All four lives begin with the same R30,000 monthly salary when work starts. Earnings grow by 1.2 percent a year above inflation. Pension contributions are 15 percent of pay and earn 4 percent a year above inflation. Values are constant 2026 rand.",
        "value": "30000",
        "unit": "constant 2026 rand per month at the start of work",
        "type": "model assumption",
        "provenance": "Manuscript common parameters",
        "evidence_strength": "model assumption",
        "sensitivity": "moderate",
        "alternatives": [
          "A manual worker without a pension or stable employment"
        ]
      },
      {
        "id": "GSX:POP-007:A03",
        "local_id": "A03",
        "name": "Conventional three-stage life",
        "statement": "The conventional life has three years of university, 42 years of full work, and retirement at 65. If the person lives to 120, retirement lasts 55 years.",
        "value": "65",
        "unit": "years, conventional retirement age",
        "type": "model assumption",
        "provenance": "Manuscript life-design table",
        "evidence_strength": "scenario",
        "sensitivity": "high",
        "alternatives": [
          "Long career",
          "Multi-stage life",
          "Portfolio life"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:POP-007:R01",
        "local_id": "R01",
        "statement": "Even with uninterrupted employment, the conventional pension fund finances only 57 percent of the target income if retirement at 65 is followed by life to 120.",
        "value": "57",
        "unit": "percent of target retirement income financed",
        "scenario": "Conventional three-stage life, life to 120",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-007:R02",
        "local_id": "R02",
        "statement": "Present-value lifetime earnings are R8.99 million for the conventional life, R12.71 million for the long career, R11.18 million for the multi-stage life, and R10.84 million for the portfolio life. Net fiscal contribution runs from R0.80 million to R1.99 million.",
        "value": "12.71",
        "unit": "million constant 2026 rand, long-career lifetime earnings",
        "scenario": "Four life designs from age 20 to 120",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:POP-007:M01",
        "local_id": "M01",
        "name": "Four life-course designs",
        "statement": "The model compares a conventional three-stage life, a long career, a multi-stage life with recurring education and a care break, and a portfolio life. It measures earnings and net fiscal contribution in constant 2026 rand under one extended healthy adulthood."
      }
    ],
    "claims": [
      {
        "id": "GSX:POP-007:C01",
        "local_id": "C01",
        "claim": "If a conventional life retires at 65 and the person lives to 120, retirement lasts 55 years and the modelled pension finances only 57 percent of the target income, even with uninterrupted employment.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-007:A01",
          "GSX:POP-007:A02",
          "GSX:POP-007:A03"
        ],
        "result": "GSX:POP-007:R01",
        "results": [
          "GSX:POP-007:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "South Africans do not currently live to 100 or 120 on average. The scenario explores extended healthy adulthood, not a forecast. If healthspan does not rise with lifespan, the financial results deteriorate and the care burden rises. A manual worker without stable work cannot simply be told to work to 85.",
        "source_study": "GSX:POP-007",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/the-hundred-year-life/claims/C01",
        "supported_by": [
          "GSX:POP-007:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-007:C02",
        "local_id": "C02",
        "claim": "Of the four designs, the long career has the highest modelled lifetime earnings, R12.71 million in present value, against R8.99 million for the conventional life. The multi-stage and portfolio designs sit between them, at R11.18 million and R10.84 million.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-007:A01",
          "GSX:POP-007:A02"
        ],
        "result": "GSX:POP-007:R02",
        "results": [
          "GSX:POP-007:R02"
        ],
        "sensitivity": "moderate",
        "main_limitation": "The long career is the strongest narrow financial result because it maximises paid work. It assumes that health, employer demand, and working conditions permit a very long career. It is not automatically the best life.",
        "source_study": "GSX:POP-007",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/the-hundred-year-life/claims/C02",
        "supported_by": [
          "GSX:POP-007:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:IND-003": {
    "assumptions": [
      {
        "id": "GSX:IND-003:A01",
        "local_id": "A01",
        "name": "Alternative products",
        "statement": "The sales tower for 1,000 tonnes of contained manganese compares ore, HPMSM, cathode material, cells and packs as alternative end products.",
        "value": "1000",
        "unit": "tonnes of contained manganese",
        "type": "model assumption",
        "provenance": "Manuscript finding 1",
        "evidence_strength": "illustrative tower",
        "sensitivity": "moderate",
        "alternatives": [
          "A different product boundary"
        ]
      },
      {
        "id": "GSX:IND-003:A02",
        "local_id": "A02",
        "name": "Central HPMSM plant",
        "statement": "The central plant is a hypothetical 30,000-tonne-a-year HPMSM facility with R4.5 billion of initial capital and USD1,100 a tonne of operating cost.",
        "value": "30000",
        "unit": "tonnes a year, nameplate",
        "type": "model assumption",
        "provenance": "Manuscript finding 3",
        "evidence_strength": "plant scenario",
        "sensitivity": "high",
        "alternatives": [
          "The 6,000-tonne brownfield plant already being commissioned"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:IND-003:R01",
        "local_id": "R01",
        "statement": "In the central illustration, 1,000 tonnes of contained manganese supports about USD0.5 million of ore sales, USD5.6 million of HPMSM sales, USD133 million of cathode-material sales, USD364 million of cell sales or USD545 million of pack-and-system sales.",
        "value": "5.6",
        "unit": "million US dollars of HPMSM sales per 1,000 tonnes contained",
        "scenario": "Central sales tower, alternative products",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:IND-003:R02",
        "local_id": "R02",
        "statement": "At 75 percent utilisation the central plant requires about USD2,454 a tonne in real product revenue to cover operating cost, annualised capital and sustaining capital. At 90 percent the requirement is about USD2,228. The paper's USD1,800 sales case does not clear the full economic cost.",
        "value": "2454",
        "unit": "US dollars per tonne required at 75 percent utilisation",
        "scenario": "Central 30,000-tonne HPMSM plant",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:IND-003:M01",
        "local_id": "M01",
        "name": "Manganese value tower and HPMSM plant",
        "statement": "The model compares alternative products from 1,000 tonnes of contained manganese and the cost of a hypothetical 30,000-tonne HPMSM plant. The product values are alternatives, not a stack."
      }
    ],
    "claims": [
      {
        "id": "GSX:IND-003:C01",
        "local_id": "C01",
        "claim": "The manuscript's first expansion is a qualified 30,000-tonne-a-year HPMSM platform linked to firm offtake, with partner-led cathode production and a later, conditional 4 to 6 GWh cell plant.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:IND-003:A01",
          "GSX:IND-003:A02"
        ],
        "result": "GSX:IND-003:R01",
        "results": [
          "GSX:IND-003:R01"
        ],
        "sensitivity": "moderate",
        "main_limitation": "Cell and pack revenue is not created by manganese alone. Most of it pays for other materials, components, capital and distribution. The tower values must not be added together.",
        "source_study": "GSX:IND-003",
        "version": "1.0",
        "href": "https://greyscienx.com/research/strategic-industrialisation/the-manganese-to-battery-economy/claims/C01",
        "supported_by": [
          "GSX:IND-003:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:IND-003:C02",
        "local_id": "C02",
        "claim": "Under the central plant assumptions, a sales price of USD1,800 a tonne does not cover the full economic cost at either 75 or 90 percent utilisation.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:IND-003:A02"
        ],
        "result": "GSX:IND-003:R02",
        "results": [
          "GSX:IND-003:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "The result can change with lower capital, lower operating cost, premium pricing, grants, concessional capital or higher co-product revenue. Nameplate capacity is not qualification or demand.",
        "source_study": "GSX:IND-003",
        "version": "1.0",
        "href": "https://greyscienx.com/research/strategic-industrialisation/the-manganese-to-battery-economy/claims/C02",
        "supported_by": [
          "GSX:IND-003:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:IND-006": {
    "assumptions": [
      {
        "id": "GSX:IND-006:A01",
        "local_id": "A01",
        "name": "Deposit rule",
        "statement": "All royalties first enter the National Revenue Fund. Only a fraction of royalties, windfall mining tax and public-industrial dividends is transferred to the savings fund. Mineral and petroleum royalties were R10.6 billion in 2024/25.",
        "value": "10.6",
        "unit": "billion rand of royalties in 2024/25",
        "type": "model assumption",
        "provenance": "Manuscript findings, citing the royalty base",
        "evidence_strength": "budget fact used as the deposit base",
        "sensitivity": "moderate",
        "alternatives": [
          "A larger deposit share",
          "Saving revenue while borrowing the same amount"
        ]
      },
      {
        "id": "GSX:IND-006:A02",
        "local_id": "A02",
        "name": "Central withdrawal rule",
        "statement": "Withdrawals wait 15 years and then equal 3 percent of the trailing five-year fund value.",
        "value": "3",
        "unit": "percent of the trailing five-year fund value",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "rule",
        "sensitivity": "high",
        "alternatives": [
          "Withdrawal after five years at 5 percent"
        ]
      },
      {
        "id": "GSX:IND-006:A03",
        "local_id": "A03",
        "name": "Separate institutions",
        "statement": "The industrial holding company and the savings fund are different balance sheets. The fund is diversified away from South African minerals, the rand and the domestic business cycle.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript findings",
        "evidence_strength": "institutional design",
        "sensitivity": "high",
        "alternatives": [
          "Using the fund to finance the holding company"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:IND-006:R01",
        "local_id": "R01",
        "statement": "In the central case the fund reaches about R258 billion in 2042, R586 billion in 2060, R893 billion in 2080 and R1.48 trillion in 2125, in constant 2026 rand.",
        "value": "586",
        "unit": "billion constant 2026 rand in 2060",
        "scenario": "Central case",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:IND-006:R02",
        "local_id": "R02",
        "statement": "The central annual budget transfer rises from about R6 billion when withdrawals begin to R16 billion in 2060 and R43 billion in 2125.",
        "value": "16",
        "unit": "billion constant 2026 rand in 2060",
        "scenario": "Central withdrawal path",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:IND-006:M01",
        "local_id": "M01",
        "name": "Mineral savings-fund paths",
        "statement": "Royalties, windfall mining tax and dividends are deposited by rule into a separate fund. The central case waits 15 years and then withdraws 3 percent of the trailing five-year fund value."
      }
    ],
    "claims": [
      {
        "id": "GSX:IND-006:C01",
        "local_id": "C01",
        "claim": "Under the central rule, the fund reaches about R586 billion by 2060 and transfers about R16 billion that year, rising to R1.48 trillion and R43 billion by 2125, in constant 2026 rand.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:IND-006:A01",
          "GSX:IND-006:A02",
          "GSX:IND-006:A03"
        ],
        "result": "GSX:IND-006:R01",
        "results": [
          "GSX:IND-006:R01",
          "GSX:IND-006:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "A fund does not create a fiscal surplus. If the deposit is matched by new borrowing at a higher cost, the country has a leveraged portfolio rather than national savings. The transfer is a marginal public income, not a self-financing welfare state.",
        "source_study": "GSX:IND-006",
        "version": "1.0",
        "href": "https://greyscienx.com/research/strategic-industrialisation/the-mineral-sovereign-wealth-fund/claims/C01",
        "supported_by": [
          "GSX:IND-006:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:IND-006:C02",
        "local_id": "C02",
        "claim": "The adverse case withdraws earlier, draws a larger share and earns only 1.5 percent real. The manuscript says that path ends the century with almost nothing.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:IND-006:A02",
          "GSX:IND-006:A03"
        ],
        "result": "GSX:IND-006:R02",
        "results": [
          "GSX:IND-006:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "The permanent character of the fund is the withdrawal rule, not the label. The rule has to survive a future government that wants the money.",
        "source_study": "GSX:IND-006",
        "version": "1.0",
        "href": "https://greyscienx.com/research/strategic-industrialisation/the-mineral-sovereign-wealth-fund/claims/C02",
        "supported_by": [
          "GSX:IND-006:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:IND-002": {
    "assumptions": [
      {
        "id": "GSX:IND-002:A01",
        "local_id": "A01",
        "name": "Upstream position",
        "statement": "USGS figures used in the manuscript put 2025 South African platinum mine output at about 120,000 kilograms, roughly 71 percent of reported world output, with about 63 million kilograms of PGM reserves.",
        "value": "120000",
        "unit": "kilograms of platinum mined in 2025",
        "type": "model assumption",
        "provenance": "Manuscript Part I, citing USGS Mineral Commodity Summaries 2026",
        "evidence_strength": "external commodity estimate cited by the manuscript",
        "sensitivity": "low",
        "alternatives": [
          "A later USGS revision"
        ]
      },
      {
        "id": "GSX:IND-002:A02",
        "local_id": "A02",
        "name": "Central hydrogen project",
        "statement": "The central 100 MW illustration uses R8 billion of integrated capital, 65 percent utilisation and electricity at R0.75 per kWh.",
        "value": "0.75",
        "unit": "rand per kWh",
        "type": "model assumption",
        "provenance": "Manuscript finding 6",
        "evidence_strength": "project scenario",
        "sensitivity": "high",
        "alternatives": [
          "A different power price or utilisation rate"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:IND-002:R01",
        "local_id": "R01",
        "statement": "In the model, one kilogram is worth about USD38,600 as refined metal and can enable USD3.2 million of complete fuel-cell systems. The endpoints are alternatives, not a sum.",
        "value": "38600",
        "unit": "US dollars per kilogram of refined metal in the model",
        "scenario": "Refined metal versus complete fuel-cell systems",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:IND-002:R02",
        "local_id": "R02",
        "statement": "The central 100 MW project breaks even near USD8.25 per kilogram of hydrogen.",
        "value": "8.25",
        "unit": "US dollars per kilogram of hydrogen",
        "scenario": "Central 100 MW project",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:IND-002:M01",
        "local_id": "M01",
        "name": "Selective platinum-to-hydrogen chain",
        "statement": "The model separates refined-metal value, component value and complete-system value, and it costs one central 100 MW hydrogen project."
      }
    ],
    "claims": [
      {
        "id": "GSX:IND-002:C01",
        "local_id": "C01",
        "claim": "The manuscript's industrial conclusion is a qualified PGM-component platform, with complete electrolysers and hydrogen exports only where customers, technology partners and low-cost electricity are already contracted.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:IND-002:A01"
        ],
        "result": "GSX:IND-002:R01",
        "results": [
          "GSX:IND-002:R01"
        ],
        "sensitivity": "moderate",
        "main_limitation": "Platinum ownership creates leverage, not automatic competitiveness. Most complete-system revenue pays for non-PGM components and services. The metal and system values are alternatives, not a sum.",
        "source_study": "GSX:IND-002",
        "version": "1.0",
        "href": "https://greyscienx.com/research/strategic-industrialisation/the-platinum-to-hydrogen-economy/claims/C01",
        "supported_by": [
          "GSX:IND-002:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:IND-002:C02",
        "local_id": "C02",
        "claim": "Under the central project assumptions, a 100 MW hydrogen plant breaks even near USD8.25 per kilogram. Capital utilisation and the power price dominate the electrolyser's PGM value.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:IND-002:A02"
        ],
        "result": "GSX:IND-002:R02",
        "results": [
          "GSX:IND-002:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "Nearby platinum does not make hydrogen cheap. A different electricity price or utilisation rate moves the break-even.",
        "source_study": "GSX:IND-002",
        "version": "1.0",
        "href": "https://greyscienx.com/research/strategic-industrialisation/the-platinum-to-hydrogen-economy/claims/C02",
        "supported_by": [
          "GSX:IND-002:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:POP-004": {
    "assumptions": [
      {
        "id": "GSX:POP-004:A01",
        "local_id": "A01",
        "name": "2025 starting population",
        "statement": "The simulation starts with South Africa in 2025: 63.1 million people, of whom 6.6 million are aged 60 or older. Ageing is moved forward one year at a time to 2100.",
        "value": "63.1",
        "unit": "million people in 2025",
        "type": "model assumption",
        "provenance": "Manuscript calibration, using the cited Statistics South Africa 2025 estimate",
        "evidence_strength": "sourced scale",
        "sensitivity": "moderate",
        "alternatives": [
          "Renewal, baseline ageing, and accelerated-ageing fertility paths"
        ]
      },
      {
        "id": "GSX:POP-004:A02",
        "local_id": "A02",
        "name": "2024 age-turnout pattern",
        "statement": "Votes are estimated by applying the Electoral Commission's 2024 age-turnout pattern. Those rates come from identification scans for 9.17 million of 16.29 million voters who voted, then extrapolated.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript, citing the 2024 national and provincial elections report",
        "evidence_strength": "observed pattern, extrapolated",
        "sensitivity": "high",
        "alternatives": [
          "A mobilisation path that changes youth turnout"
        ]
      },
      {
        "id": "GSX:POP-004:A03",
        "local_id": "A03",
        "name": "Age-60 boundary",
        "statement": "Older adult means a person aged 60 or older, the current old-age grant age and the series benchmark. It does not mean every such person has retired or shares one preference.",
        "value": "60",
        "unit": "years",
        "type": "model assumption",
        "provenance": "Manuscript definitions",
        "evidence_strength": "definition",
        "sensitivity": "low",
        "alternatives": [
          "A different age boundary"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:POP-004:R01",
        "local_id": "R01",
        "statement": "In the 2025 calibration, people aged 60 or older are 15.1 percent of adults and 20.7 percent of votes cast. The median voter is 43, four years older than the median adult.",
        "value": "20.7",
        "unit": "percent of votes cast by people aged 60 or older",
        "scenario": "2025 calibration with the 2024 age-turnout pattern",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-004:R02",
        "local_id": "R02",
        "statement": "Under baseline ageing, the age-60-plus bloc overtakes voters aged 18 to 34 around 2039 and supplies 46.0 percent of votes by 2100 with fixed turnout. The median voter is 57, still below retirement age. Accelerated ageing produces a median voter of 60 in 2085, or 2081 with turnout feedback.",
        "value": "46.0",
        "unit": "percent of votes in 2100, baseline ageing, fixed turnout",
        "scenario": "Baseline and accelerated scenarios to 2100",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:POP-004:M01",
        "local_id": "M01",
        "name": "Electorate-versus-population cohort",
        "statement": "A simple cohort model moves the 2025 age structure to 2100 under three fertility, longevity, and migration paths, then applies fixed or feedback turnout. It is built to expose relationships. It is not an official population forecast."
      }
    ],
    "claims": [
      {
        "id": "GSX:POP-004:C01",
        "local_id": "C01",
        "claim": "In the 2025 calibration, people aged 60 or older are 15.1 percent of adults but 20.7 percent of votes cast. Applying the 2024 age-turnout pattern produces a median voter aged 43, four years older than the median adult.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-004:A01",
          "GSX:POP-004:A02",
          "GSX:POP-004:A03"
        ],
        "result": "GSX:POP-004:R01",
        "results": [
          "GSX:POP-004:R01"
        ],
        "sensitivity": "moderate",
        "main_limitation": "The turnout rates are a strong pattern extrapolated from identification scans, not a perfect census of every voter. The median voter is the age that splits votes cast in half. It is not one person whose wishes become policy.",
        "source_study": "GSX:POP-004",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/the-politics-of-an-ageing-electorate/claims/C01",
        "supported_by": [
          "GSX:POP-004:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-004:C02",
        "local_id": "C02",
        "claim": "Under the baseline path, voters aged 60 or older overtake voters aged 18 to 34 around 2039 and cast 46.0 percent of votes by 2100 if age-specific turnout stays fixed. The median voter remains below retirement age. Only the accelerated-ageing scenario produces a retired median voter within the century, in 2085 with fixed turnout and in 2081 with feedback.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-004:A01",
          "GSX:POP-004:A02",
          "GSX:POP-004:A03"
        ],
        "result": "GSX:POP-004:R02",
        "results": [
          "GSX:POP-004:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "The paths are deliberately simple cohort mechanics, not an official forecast. Accelerated ageing is a severe stress test. Mobilisation can still change the electorate even when the population cannot change quickly.",
        "source_study": "GSX:POP-004",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/the-politics-of-an-ageing-electorate/claims/C02",
        "supported_by": [
          "GSX:POP-004:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:POP-011": {
    "assumptions": [
      {
        "id": "GSX:POP-011:A01",
        "local_id": "A01",
        "name": "Synthesis, not a new forecast",
        "statement": "The ten population studies are read as windows on one system. Their models are hypothetical, use South African rand and South-African or Gauteng-scale examples, and are not forecasts.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "synthesis",
        "sensitivity": "moderate",
        "alternatives": [
          "Reading each study as a separate crisis"
        ]
      },
      {
        "id": "GSX:POP-011:A02",
        "local_id": "A02",
        "name": "Household formation is the prequel",
        "statement": "Household formation changes housing demand, consumption, care, risk sharing and the capacity to save before any pension or demographic calculation begins.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript figure note and Part II",
        "evidence_strength": "synthesis",
        "sensitivity": "moderate",
        "alternatives": [
          "see the manuscript sensitivity discussion"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:POP-011:R01",
        "local_id": "R01",
        "statement": "Read together, the studies say demographic pressure is rarely a shortage of people in the abstract. It is a failure of timing, matching and institutions.",
        "value": "structural",
        "unit": "synthesis across the ten population studies",
        "scenario": "Ten studies read as one system",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:POP-011:M01",
        "local_id": "M01",
        "name": "Ten studies, one system",
        "statement": "The paper reads the ten population studies as one feedback system. It does not add a separate numerical model. Household formation is treated as the prequel because it changes housing demand, care, risk sharing and saving before the pension and demographic calculations begin."
      }
    ],
    "claims": [
      {
        "id": "GSX:POP-011:C01",
        "local_id": "C01",
        "claim": "Demographic pressure, in this synthesis, is rarely a shortage of people in the abstract. It is a failure of timing, matching and institutions. Income can arrive after it is useful, workers can exist outside the jobs that need them, homes can stand in the wrong places, and reform can begin after the cheaper options have expired.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-011:A01",
          "GSX:POP-011:A02"
        ],
        "result": "GSX:POP-011:R01",
        "results": [
          "GSX:POP-011:R01"
        ],
        "sensitivity": "moderate",
        "main_limitation": "This is a structural reading of ten hypothetical models, not a new forecast and not a single national estimate. The magnitudes belong to the individual studies. A smaller population can still need more homes, and higher productivity can preserve GDP while hospitals remain understaffed.",
        "source_study": "GSX:POP-011",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/the-population-system/claims/C01",
        "supported_by": [
          "GSX:POP-011:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-011:C02",
        "local_id": "C02",
        "claim": "The manuscript's policy lesson is a portfolio that acts on several clocks. Immediate protection, medium-term labour and housing adjustment, and long-term changes to careers, families and retirement are the three clocks it names.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-011:A01"
        ],
        "result": "GSX:POP-011:R01",
        "results": [
          "GSX:POP-011:R01"
        ],
        "sensitivity": "moderate",
        "main_limitation": "This is the paper's normative lesson drawn from the ten models. It does not rank a specific tax, grant or retirement age, and it does not replace the conditional results inside the individual studies.",
        "source_study": "GSX:POP-011",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/the-population-system/claims/C02",
        "supported_by": [
          "GSX:POP-011:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:POP-006": {
    "assumptions": [
      {
        "id": "GSX:POP-006:A01",
        "local_id": "A01",
        "name": "One million prospective households",
        "statement": "The model follows one million prospective households for five years and assumes 350,000 births without a new policy. It tests seven stylised interventions.",
        "value": "350000",
        "unit": "births without a new policy",
        "type": "model assumption",
        "provenance": "Manuscript model design",
        "evidence_strength": "illustrative",
        "sensitivity": "high",
        "alternatives": [
          "A different baseline birth count"
        ]
      },
      {
        "id": "GSX:POP-006:A02",
        "local_id": "A02",
        "name": "Only completed extra births count",
        "statement": "A birth paid for by a programme may be unchanged, brought forward, or permanently additional. Only the permanently additional group is credited as a lasting demographic response.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript counterfactual groups",
        "evidence_strength": "definition",
        "sensitivity": "high",
        "alternatives": [
          "Counting rescheduled births as additional"
        ]
      },
      {
        "id": "GSX:POP-006:A03",
        "local_id": "A03",
        "name": "Labour-market value of a birth",
        "statement": "Discounted to birth, an additional person's lifetime production is worth R1.45 million in a weak labour market, R3.73 million in an average one, and R5.83 million in a strong one. Government also pays for education, health, services, and old age.",
        "value": "3.73",
        "unit": "million constant rand of lifetime production, average labour market",
        "type": "model assumption",
        "provenance": "Manuscript fiscal-value cases",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "Weak labour market",
          "Strong labour market"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:POP-006:R01",
        "local_id": "R01",
        "statement": "In the average run, the median cost of one permanently additional birth is about R720,000 for free childcare and R4.18 million for a parent tax exemption. The targeted family package costs about R780,000 per added birth and produces nearly 99,000 additional births per million prospective households.",
        "value": "720000",
        "unit": "constant rand per permanently additional birth, free childcare",
        "scenario": "Average model run, seven stylised policies",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-006:R02",
        "local_id": "R02",
        "statement": "Net lifetime fiscal value of an additional person is negative R610,000 in the weak labour market, positive R190,000 in the average labour market, and positive R960,000 in the strong one. None of the programmes repays itself in the average case.",
        "value": "-610000",
        "unit": "constant rand, weak-labour-market net fiscal value",
        "scenario": "Lifetime fiscal value by labour-market case",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:POP-006:M01",
        "local_id": "M01",
        "name": "Additional-birth cost model",
        "statement": "The model separates births that would have happened, births that are brought forward, and births that permanently add to completed family size. Programme cost is judged against the permanently additional group and against the future fiscal value of that person."
      }
    ],
    "claims": [
      {
        "id": "GSX:POP-006:C01",
        "local_id": "C01",
        "claim": "In the average run, the median cost of one permanently additional birth ranges from about R720,000 for free childcare to R4.18 million for a parent tax exemption. The targeted family package costs about R780,000 per added birth and produces nearly 99,000 additional births per million prospective households. A cash top-up costs about R1.76 million per added birth and produces only about 12,000.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-006:A01",
          "GSX:POP-006:A02"
        ],
        "result": "GSX:POP-006:R01",
        "results": [
          "GSX:POP-006:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "The largest payment is not the cheapest birth. A programme can pay households that would have had the child anyway, or it can only move the timing. The cost figures are medians from a stylised model, with wide 10th-to-90th percentile ranges in the manuscript.",
        "source_study": "GSX:POP-006",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/the-price-of-another-child/claims/C01",
        "supported_by": [
          "GSX:POP-006:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-006:C02",
        "local_id": "C02",
        "claim": "Net lifetime fiscal value of an additional person is negative R610,000 in the weak labour market, positive R190,000 in the average labour market, and positive R960,000 in the strong one. None of the modelled programmes repays itself in the average case.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-006:A01",
          "GSX:POP-006:A03"
        ],
        "result": "GSX:POP-006:R02",
        "results": [
          "GSX:POP-006:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "Fertility policy is cheaper than ageing in this model only when the policy causes completed births, the future economy employs those children productively, and the new workers arrive before the fiscal emergency. Child support that does not cause extra births can still be poverty policy.",
        "source_study": "GSX:POP-006",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/the-price-of-another-child/claims/C02",
        "supported_by": [
          "GSX:POP-006:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:SRD-004": {
    "assumptions": [
      {
        "id": "GSX:SRD-004:A01",
        "local_id": "A01",
        "name": "Public envelope",
        "statement": "The arithmetic uses R225 billion of public industrial capital.",
        "value": "225",
        "unit": "billion rand of public industrial capital",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "scenario scale",
        "sensitivity": "moderate",
        "alternatives": [
          "A different envelope"
        ]
      },
      {
        "id": "GSX:SRD-004:A02",
        "local_id": "A02",
        "name": "Mixed portfolio",
        "statement": "The central portfolio spreads that capital across infrastructure, concessional debt, minority equity, first-loss capital, a guarantee reserve, project preparation, skills and supplier funds.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "scenario design",
        "sensitivity": "high",
        "alternatives": [
          "Full public ownership",
          "A guarantee-heavy stack"
        ]
      },
      {
        "id": "GSX:SRD-004:A03",
        "local_id": "A03",
        "name": "Gross is not additional",
        "statement": "Capital that would have been invested anyway, or that is delayed, unallocated or failed, is removed before the operating multiple is stated.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "accounting rule",
        "sensitivity": "high",
        "alternatives": [
          "Treating every private rand as additional"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:SRD-004:R01",
        "local_id": "R01",
        "statement": "The central mixed portfolio mobilises R506 billion of gross investment, a headline multiple of 2.25.",
        "value": "2.25",
        "unit": "gross rand of investment per rand of public capital",
        "scenario": "Central mixed portfolio",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:SRD-004:R02",
        "local_id": "R02",
        "statement": "After non-additional, delayed, unallocated and failed capital, R383 billion remains operating, 1.70 times the public envelope.",
        "value": "1.70",
        "unit": "operating rand per rand of public capital",
        "scenario": "Central portfolio after deductions",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:SRD-004:M01",
        "local_id": "M01",
        "name": "Public-capital mobilisation portfolio",
        "statement": "The model allocates R225 billion of public industrial capital across instruments and then deducts capital judged non-additional, delayed, unallocated or failed."
      }
    ],
    "claims": [
      {
        "id": "GSX:SRD-004:C01",
        "local_id": "C01",
        "claim": "In the central mixed portfolio, R225 billion of public industrial capital mobilises R506 billion of gross investment, 2.25 times the public envelope. After deductions, R383 billion remains operating, 1.70 times the envelope.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:SRD-004:A01",
          "GSX:SRD-004:A02",
          "GSX:SRD-004:A03"
        ],
        "result": "GSX:SRD-004:R01",
        "results": [
          "GSX:SRD-004:R01",
          "GSX:SRD-004:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "A multiplier is a description of a capital stack, not money created. Guarantees can show a high cash multiple while leaving the downside with the state. The multiples are not observed South African averages.",
        "source_study": "GSX:SRD-004",
        "version": "1.0",
        "href": "https://greyscienx.com/research/r350-counterfactual/the-public-capital-multiplier/claims/C01",
        "supported_by": [
          "GSX:SRD-004:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:SRD-004:C02",
        "local_id": "C02",
        "claim": "The manuscript's portfolio conclusion is a gross mobilisation range of roughly 1.5 to 2.5 times, judged by net additional operating investment, development value and risk-adjusted public cost.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:SRD-004:A02",
          "GSX:SRD-004:A03"
        ],
        "result": "GSX:SRD-004:R02",
        "results": [
          "GSX:SRD-004:R02"
        ],
        "sensitivity": "moderate",
        "main_limitation": "Maximising a single headline ratio is the comparison the paper rejects. Common infrastructure can have low measured leverage and high additionality.",
        "source_study": "GSX:SRD-004",
        "version": "1.0",
        "href": "https://greyscienx.com/research/r350-counterfactual/the-public-capital-multiplier/claims/C02",
        "supported_by": [
          "GSX:SRD-004:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:SRD-005": {
    "assumptions": [
      {
        "id": "GSX:SRD-005:A01",
        "local_id": "A01",
        "name": "Envelope and split",
        "statement": "R225 billion in constant 2026 rand is allocated across the programme. R96 billion, 43 percent, goes directly into production plants. The rest is power, water, logistics, parks, supplier finance, skills, worker housing and a R15 billion contingency.",
        "value": "225",
        "unit": "billion constant 2026 rand",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "scenario allocation",
        "sensitivity": "moderate",
        "alternatives": [
          "A different split between plant and enabling infrastructure"
        ]
      },
      {
        "id": "GSX:SRD-005:A02",
        "local_id": "A02",
        "name": "Modular production core",
        "statement": "The production core is 34 modules across manganese-battery materials, PGM-hydrogen components, vanadium storage and shared machinery or recycling.",
        "value": "34",
        "unit": "industrial modules",
        "type": "model assumption",
        "provenance": "Manuscript central conclusion",
        "evidence_strength": "stylised plant assumptions",
        "sensitivity": "high",
        "alternatives": [
          "Fewer or more modules"
        ]
      },
      {
        "id": "GSX:SRD-005:A03",
        "local_id": "A03",
        "name": "Utilisation hinge",
        "statement": "At 40 percent average use the portfolio creates almost no local value after its fixed burden. Above 70 percent the case becomes materially stronger.",
        "value": "70",
        "unit": "percent average capacity use",
        "type": "model assumption",
        "provenance": "Manuscript findings",
        "evidence_strength": "scenario threshold",
        "sensitivity": "high",
        "alternatives": [
          "40 percent utilisation"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:SRD-005:R01",
        "local_id": "R01",
        "statement": "In the central case the programme supports about 11,100 direct operating jobs, roughly 10,000 supplier jobs, R108 billion of annual sales, 700 MW of reliable power demand and 12 million cubic metres of annual industrial water demand.",
        "value": "11100",
        "unit": "direct operating jobs",
        "scenario": "Central case, after construction",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:SRD-005:R02",
        "local_id": "R02",
        "statement": "Construction employment peaks near 40,000 direct jobs and is temporary. Only R96 billion of the R225 billion goes directly into production plants.",
        "value": "40000",
        "unit": "peak direct construction jobs",
        "scenario": "Construction phase",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:SRD-005:M01",
        "local_id": "M01",
        "name": "Physical allocation of R225 billion",
        "statement": "The model turns R225 billion in constant 2026 rand into sites, utilities, 34 production modules, skills, supplier finance and logistics, using stylised plant assumptions from the mineral papers."
      }
    ],
    "claims": [
      {
        "id": "GSX:SRD-005:C01",
        "local_id": "C01",
        "claim": "A credible R225 billion programme could establish 34 industrial modules and, in the central case, support about 11,100 direct operating jobs, roughly 10,000 supplier jobs and R108 billion of annual sales.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:SRD-005:A01",
          "GSX:SRD-005:A02"
        ],
        "result": "GSX:SRD-005:R01",
        "results": [
          "GSX:SRD-005:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "The numbers are scenarios, not quotations or forecasts. Success depends more on utilisation and execution than on the number of ribbon cuttings. The programme takes close to a decade.",
        "source_study": "GSX:SRD-005",
        "version": "1.0",
        "href": "https://greyscienx.com/research/r350-counterfactual/the-r200-billion-factory/claims/C01",
        "supported_by": [
          "GSX:SRD-005:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:SRD-005:C02",
        "local_id": "C02",
        "claim": "More than half of the envelope enables production rather than buying production equipment. Peak construction employment near 40,000 direct jobs is not permanent operating employment.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:SRD-005:A01",
          "GSX:SRD-005:A03"
        ],
        "result": "GSX:SRD-005:R02",
        "results": [
          "GSX:SRD-005:R02"
        ],
        "sensitivity": "moderate",
        "main_limitation": "A plant without power, water, logistics, skills, working capital or customers is not productive capital. Presenting the construction peak as permanent employment would misstate the model.",
        "source_study": "GSX:SRD-005",
        "version": "1.0",
        "href": "https://greyscienx.com/research/r350-counterfactual/the-r200-billion-factory/claims/C02",
        "supported_by": [
          "GSX:SRD-005:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:SRD-001": {
    "assumptions": [
      {
        "id": "GSX:SRD-001:A01",
        "local_id": "A01",
        "name": "Programme envelope",
        "statement": "The envelope from 2020/21 through the 2026/27 allocation is R225.8 billion in nominal rand, about R253.5 billion in constant 2026 purchasing power. Later years include a revised estimate and a voted allocation, not only cash already spent.",
        "value": "253.5",
        "unit": "billion constant 2026 rand",
        "type": "model assumption",
        "provenance": "Manuscript Part I, citing the Department of Social Development and National Treasury",
        "evidence_strength": "programme records restated by the model",
        "sensitivity": "moderate",
        "alternatives": [
          "A ledger that stops at final outturns"
        ]
      },
      {
        "id": "GSX:SRD-001:A02",
        "local_id": "A02",
        "name": "Reprioritised fund",
        "statement": "The published asset paths withhold the grant and place the revenue in a ring-fenced fund. They do not describe the borrowed-fund case, which adds an asset and a matching liability.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript financing table",
        "evidence_strength": "counterfactual design",
        "sensitivity": "high",
        "alternatives": [
          "Debt reduction",
          "A borrowed industrial fund"
        ]
      },
      {
        "id": "GSX:SRD-001:A03",
        "local_id": "A03",
        "name": "Welfare is not counted here",
        "statement": "The model does not count food, transport, health protection, debt service or local demand purchased by the grant. That loss is the subject of the companion welfare paper.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "scope limit",
        "sensitivity": "high",
        "alternatives": [
          "A combined welfare and asset account"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:SRD-001:R01",
        "local_id": "R01",
        "statement": "By 2050 the best-case industrial fund holds about R789 billion in productive assets and generates roughly R39 billion a year in public cash, in 2026 rand.",
        "value": "789",
        "unit": "billion constant 2026 rand of productive assets",
        "scenario": "Best case, 2050",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:SRD-001:R02",
        "local_id": "R02",
        "statement": "By 2050 the average case reaches roughly R304 billion in productive assets and R9 billion in annual public cash. The worst case reaches R72 billion and R0.7 billion a year.",
        "value": "304",
        "unit": "billion constant 2026 rand of productive assets",
        "scenario": "Average case, 2050",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:SRD-001:M01",
        "local_id": "M01",
        "name": "SRD industrial-fund counterfactual",
        "statement": "The model restates the 2020/21-2026/27 SRD programme envelope in constant 2026 rand and follows best, average and worst industrial-fund paths to 2050. The asset paths use the reprioritised-fund version of the counterfactual."
      }
    ],
    "claims": [
      {
        "id": "GSX:SRD-001:C01",
        "local_id": "C01",
        "claim": "If the SRD envelope of about R253.5 billion in constant 2026 rand had been reprioritised into an industrial fund, the best case holds about R789 billion in productive assets by 2050 and generates roughly R39 billion a year in public cash. The annual cash flow exceeds one current SRD budget year only around 2049.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:SRD-001:A01",
          "GSX:SRD-001:A02"
        ],
        "result": "GSX:SRD-001:R01",
        "results": [
          "GSX:SRD-001:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "The envelope is a counterfactual resource, not yet a factory. The best case depends on projects being selected, built, operated and renewed for decades. This paper does not value what households would have lost if the grant had never been paid.",
        "source_study": "GSX:SRD-001",
        "version": "1.0",
        "href": "https://greyscienx.com/research/r350-counterfactual/the-r350-industrialisation-counterfactual/claims/C01",
        "supported_by": [
          "GSX:SRD-001:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:SRD-001:C02",
        "local_id": "C02",
        "claim": "The average case reaches roughly R304 billion in productive assets and R9 billion in annual public cash by 2050. The worst case reaches R72 billion and R0.7 billion a year.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:SRD-001:A01",
          "GSX:SRD-001:A02",
          "GSX:SRD-001:A03"
        ],
        "result": "GSX:SRD-001:R02",
        "results": [
          "GSX:SRD-001:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "These paths are the reprioritised-fund counterfactual. A borrowed fund would also carry a matching liability, and neither path is automatically superior to having paid the grant.",
        "source_study": "GSX:SRD-001",
        "version": "1.0",
        "href": "https://greyscienx.com/research/r350-counterfactual/the-r350-industrialisation-counterfactual/claims/C02",
        "supported_by": [
          "GSX:SRD-001:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:POP-010": {
    "assumptions": [
      {
        "id": "GSX:POP-010:A01",
        "local_id": "A01",
        "name": "Hypothetical starting scale",
        "statement": "The model follows a hypothetical South-African-scale economy from 2026 to 2076. It begins with 12 million full-year-equivalent workers, 3 million retirees, and a population of 22 million.",
        "value": "12",
        "unit": "million full-year-equivalent workers in 2026",
        "type": "model assumption",
        "provenance": "Manuscript opening scale",
        "evidence_strength": "illustrative",
        "sensitivity": "high",
        "alternatives": [
          "Best case",
          "Worst case"
        ]
      },
      {
        "id": "GSX:POP-010:A02",
        "local_id": "A02",
        "name": "Average response",
        "statement": "The average case combines later working lives, worth 700,000 additional workers, with 75,000 young immigrants a year. General productivity rises 0.6 percent a year and automation-related productivity 0.3 percent a year. Migrants enter work after a two-year lag and retire at 67.",
        "value": "75000",
        "unit": "young immigrants per year",
        "type": "model assumption",
        "provenance": "Manuscript average case",
        "evidence_strength": "scenario",
        "sensitivity": "high",
        "alternatives": [
          "About 90,000 arrivals a year, the inflow that would hold contributor headcount at 12 million"
        ]
      },
      {
        "id": "GSX:POP-010:A03",
        "local_id": "A03",
        "name": "Occupation mismatch",
        "statement": "Output is counted in worker-equivalents, but health, construction, education, and digital work are tracked separately. A displaced administrative worker is not treated as a nurse.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript occupation result",
        "evidence_strength": "model structure",
        "sensitivity": "high",
        "alternatives": [
          "Perfect retraining across occupations"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:POP-010:R01",
        "local_id": "R01",
        "statement": "In the average case the resident workforce falls to 8.88 million, output per worker rises about 57 percent, and real GDP reaches an index of 151. The total workforce ends at 11.60 million after immigration and later working lives.",
        "value": "151",
        "unit": "real GDP index, 2026 = 100",
        "scenario": "Average case, 2026 to 2076",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-010:R02",
        "local_id": "R02",
        "statement": "The same average case ends with a modelled shortage of 738,000 health and care workers, 123,000 construction and maintenance workers, and 121,000 workers in education, safety, and public services. The age-related contribution burden rises from about 8.3 percent of covered wages to 17.0 percent.",
        "value": "738000",
        "unit": "health and care workers short",
        "scenario": "Average case, 2076 occupation balance",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:POP-010:M01",
        "local_id": "M01",
        "name": "Scarce-worker cohort",
        "statement": "The model tracks full-year-equivalent workers, retirees, immigration, later working lives, and occupation-specific shortages from 2026 to 2076. Aggregate output and staffing are separate accounts."
      }
    ],
    "claims": [
      {
        "id": "GSX:POP-010:C01",
        "local_id": "C01",
        "claim": "In the average case, a smaller resident workforce can still coincide with real GDP at an index of 151, because output per worker rises about 57 percent. The total workforce ends at 11.60 million after 75,000 young immigrants a year and 700,000 additional older workers.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-010:A01",
          "GSX:POP-010:A02"
        ],
        "result": "GSX:POP-010:R01",
        "results": [
          "GSX:POP-010:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "This is a hypothetical scale, not a forecast of South Africa's labour market. The 75,000-person inflow is below the roughly 90,000 a year that would hold contributor headcount at 12 million. Early immigrant cohorts also retire: 480,000 are retirees by 2076.",
        "source_study": "GSX:POP-010",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/the-scarce-worker-economy/claims/C01",
        "supported_by": [
          "GSX:POP-010:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-010:C02",
        "local_id": "C02",
        "claim": "That same average case still ends short of 738,000 health and care workers, even while digital and administrative work is in surplus. The modelled age-related contribution burden rises from about 8.3 percent of covered wages to 17.0 percent.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-010:A01",
          "GSX:POP-010:A02",
          "GSX:POP-010:A03"
        ],
        "result": "GSX:POP-010:R02",
        "results": [
          "GSX:POP-010:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "Aggregate output capacity is not staffing capacity. Automation adds fiscal capacity only if the income it creates enters the tax base. The burden is 28.4 percent in the worst case and 10.9 percent in the best case.",
        "source_study": "GSX:POP-010",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/the-scarce-worker-economy/claims/C02",
        "supported_by": [
          "GSX:POP-010:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:IND-001": {
    "assumptions": [
      {
        "id": "GSX:IND-001:A01",
        "local_id": "A01",
        "name": "Illustrative value pool",
        "statement": "Each stage is assigned an illustrative share of total value added. The shares are a way to expose where value is assumed to remain local. They are not a forecast of GDP or company revenue.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript numerical headline",
        "evidence_strength": "model construct",
        "sensitivity": "high",
        "alternatives": [
          "A different stage weighting"
        ]
      },
      {
        "id": "GSX:IND-001:A02",
        "local_id": "A02",
        "name": "Strategy cases",
        "statement": "The comparison includes the existing footprint, focused integration, a frontier partnership case, and forced autarky after utilisation and market-access penalties.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "scenario design",
        "sensitivity": "high",
        "alternatives": [
          "A different partnership assumption"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:IND-001:R01",
        "local_id": "R01",
        "statement": "The existing footprint retains about 37.6 percent of the modelled pool. Focused integration reaches 66.3 percent. A frontier case with successful technology partnerships reaches 81.4 percent.",
        "value": "66.3",
        "unit": "percent of the modelled value pool, focused integration",
        "scenario": "Value-pool scenarios",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:IND-001:R02",
        "local_id": "R02",
        "statement": "Forced autarky realises about 52 percent of the value pool after utilisation and market-access penalties, compared with about 62 percent for focused integration and 73 percent for the frontier partnership case on that realised-value comparison.",
        "value": "52",
        "unit": "percent of the value pool realised under forced autarky",
        "scenario": "Realised value after penalties",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:IND-001:M01",
        "local_id": "M01",
        "name": "Value-pool localisation model",
        "statement": "The model assigns illustrative shares of a critical-minerals value pool to chain stages and compares an existing footprint, focused integration, frontier partnership and forced autarky."
      }
    ],
    "claims": [
      {
        "id": "GSX:IND-001:C01",
        "local_id": "C01",
        "claim": "On the manuscript's illustrative value pool, focused integration retains 66.3 percent, compared with 37.6 percent for the existing footprint and 81.4 percent for a frontier partnership case.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:IND-001:A01",
          "GSX:IND-001:A02"
        ],
        "result": "GSX:IND-001:R01",
        "results": [
          "GSX:IND-001:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "These are not forecasts of GDP or company revenue. Geology is not industrial power: the manuscript distinguishes reserve shares from mined-production shares.",
        "source_study": "GSX:IND-001",
        "version": "1.0",
        "href": "https://greyscienx.com/research/strategic-industrialisation/the-south-african-critical-minerals-industrial-complex/claims/C01",
        "supported_by": [
          "GSX:IND-001:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:IND-001:C02",
        "local_id": "C02",
        "claim": "Forced localisation realises about 52 percent of the value pool after utilisation and market-access penalties, below focused integration on the manuscript's realised-value comparison.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:IND-001:A01",
          "GSX:IND-001:A02"
        ],
        "result": "GSX:IND-001:R02",
        "results": [
          "GSX:IND-001:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "Nominal local content can rise while actual local value falls if plants fail qualification, lack offtake or operate intermittently.",
        "source_study": "GSX:IND-001",
        "version": "1.0",
        "href": "https://greyscienx.com/research/strategic-industrialisation/the-south-african-critical-minerals-industrial-complex/claims/C02",
        "supported_by": [
          "GSX:IND-001:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:IND-004": {
    "assumptions": [
      {
        "id": "GSX:IND-004:A01",
        "local_id": "A01",
        "name": "Resource position",
        "statement": "The manuscript uses USGS figures of about 5,000 tonnes of South African vanadium production in 2025, roughly 4.5 percent of estimated world output, and about 520,000 tonnes of reported reserves, around 2.5 percent of the world total.",
        "value": "5000",
        "unit": "tonnes of vanadium produced in 2025",
        "type": "model assumption",
        "provenance": "Manuscript Part I, citing USGS",
        "evidence_strength": "external commodity estimate cited by the manuscript",
        "sensitivity": "low",
        "alternatives": [
          "A later USGS revision"
        ]
      },
      {
        "id": "GSX:IND-004:A02",
        "local_id": "A02",
        "name": "Central cost assumptions",
        "statement": "Lifetime cost parity is reported under the paper's central assumptions about lithium cost, cycling, interest rates and flow-battery performance.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "Cheap lithium",
          "Low cycling",
          "High interest rates",
          "Poor flow-battery performance"
        ]
      },
      {
        "id": "GSX:IND-004:A03",
        "local_id": "A03",
        "name": "Electrolyte scale",
        "statement": "BELCO was designed for eight million litres a year. A single 100 MW, ten-hour project in the model needs about fifty million litres.",
        "value": "50",
        "unit": "million litres for one 100 MW, ten-hour project",
        "type": "model assumption",
        "provenance": "Manuscript finding 3",
        "evidence_strength": "plant-scale comparison",
        "sensitivity": "moderate",
        "alternatives": [
          "A larger electrolyte industry"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:IND-004:R01",
        "local_id": "R01",
        "statement": "Under the central assumptions, lifetime cost parity with lithium iron phosphate appears at about sixteen hours.",
        "value": "16",
        "unit": "hours of storage duration",
        "scenario": "Central cost comparison",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:IND-004:R02",
        "local_id": "R02",
        "statement": "One 100 MW, ten-hour project needs about fifty million litres of electrolyte, more than six years of BELCO's eight-million-litre design output.",
        "value": "50",
        "unit": "million litres",
        "scenario": "Single 100 MW, ten-hour project",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:IND-004:M01",
        "local_id": "M01",
        "name": "Duration comparison with lithium iron phosphate",
        "statement": "The model compares vanadium redox flow batteries with lithium iron phosphate across storage duration under stated cost, cycling and finance assumptions."
      }
    ],
    "claims": [
      {
        "id": "GSX:IND-004:C01",
        "local_id": "C01",
        "claim": "Under the paper's central assumptions, vanadium redox flow batteries reach lifetime cost parity with lithium iron phosphate at about sixteen hours of duration.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:IND-004:A01",
          "GSX:IND-004:A02"
        ],
        "result": "GSX:IND-004:R01",
        "results": [
          "GSX:IND-004:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "Sixteen hours is a model result, not a physical law. Cheap lithium, low cycling, high interest rates or poor flow-battery performance move the crossing later. The first market in the manuscript is roughly twelve to twenty-four hours, not the four-hour lithium market.",
        "source_study": "GSX:IND-004",
        "version": "1.0",
        "href": "https://greyscienx.com/research/strategic-industrialisation/the-vanadium-grid-storage-economy/claims/C01",
        "supported_by": [
          "GSX:IND-004:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:IND-004:C02",
        "local_id": "C02",
        "claim": "A single 100 MW, ten-hour project in the model needs more electrolyte than several years of the cited BELCO design output. One electrolyte facility is a base, not a full industrial ecosystem.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:IND-004:A03"
        ],
        "result": "GSX:IND-004:R02",
        "results": [
          "GSX:IND-004:R02"
        ],
        "sensitivity": "moderate",
        "main_limitation": "Domestic storage targets create a chance to compete. They are not an order book for vanadium batteries. Factory capacity is not demand.",
        "source_study": "GSX:IND-004",
        "version": "1.0",
        "href": "https://greyscienx.com/research/strategic-industrialisation/the-vanadium-grid-storage-economy/claims/C02",
        "supported_by": [
          "GSX:IND-004:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:SRD-002": {
    "assumptions": [
      {
        "id": "GSX:SRD-002:A01",
        "local_id": "A01",
        "name": "Same envelope",
        "statement": "The withheld resource is about R253.5 billion in constant 2026 purchasing power, the same base as the industrial-fund paper.",
        "value": "253.5",
        "unit": "billion constant 2026 rand",
        "type": "model assumption",
        "provenance": "Manuscript headline ledger",
        "evidence_strength": "shared counterfactual base",
        "sensitivity": "moderate",
        "alternatives": [
          "A different programme window"
        ]
      },
      {
        "id": "GSX:SRD-002:A02",
        "local_id": "A02",
        "name": "Distributional weights",
        "statement": "In the conservative, central and severe cases, R1 of consumption at the recipient margin is valued at R1.10, R1.50 and R2.00. The weights are normative assumptions.",
        "value": "1.50",
        "unit": "welfare rand per consumption rand, central case",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "normative assumption",
        "sensitivity": "high",
        "alternatives": [
          "Equal weights",
          "A higher hunger weight"
        ]
      },
      {
        "id": "GSX:SRD-002:A03",
        "local_id": "A03",
        "name": "No double-counting of local spending",
        "statement": "The local spending multiplier is reported separately and is not added into the welfare cost.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript Part I",
        "evidence_strength": "accounting rule",
        "sensitivity": "moderate",
        "alternatives": [
          "Adding the multiplier into the welfare total"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:SRD-002:R01",
        "local_id": "R01",
        "statement": "The explicit welfare-equivalent cost of withholding the envelope is between R237 billion and R743 billion. The central estimate is R426.9 billion, about R1.68 of social cost for every R1 withheld.",
        "value": "426.9",
        "unit": "billion welfare-equivalent 2026 rand, central estimate",
        "scenario": "Central welfare case",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:SRD-002:R02",
        "local_id": "R02",
        "statement": "Additional poverty exposure across the scenarios is 2.5 million to 11.0 million person-years.",
        "value": "2.5",
        "unit": "million person-years, low end of the scenario range",
        "scenario": "Seven-year poverty exposure range",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:SRD-002:M01",
        "local_id": "M01",
        "name": "Welfare-cost ledger",
        "statement": "The model prices the explicit welfare cost of withholding the same SRD envelope valued in the industrial-fund paper. It combines consumption, costly credit, scarring and labour effects and keeps the local spending multiplier out of the welfare total."
      }
    ],
    "claims": [
      {
        "id": "GSX:SRD-002:C01",
        "local_id": "C01",
        "claim": "Withholding the SRD envelope has a central explicit welfare cost of R426.9 billion in welfare-equivalent 2026 rand, about R1.68 of social cost for every R1 withheld. The scenario range is R237 billion to R743 billion.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:SRD-002:A01",
          "GSX:SRD-002:A02",
          "GSX:SRD-002:A03"
        ],
        "result": "GSX:SRD-002:R01",
        "results": [
          "GSX:SRD-002:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "This is not a Treasury invoice, a forecast or a confidence interval. Crime, unrest and household dissolution are left outside the priced total. The central case is an analytical benchmark.",
        "source_study": "GSX:SRD-002",
        "version": "1.0",
        "href": "https://greyscienx.com/research/r350-counterfactual/the-welfare-cost-of-not-paying-the-grant/claims/C01",
        "supported_by": [
          "GSX:SRD-002:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:SRD-002:C02",
        "local_id": "C02",
        "claim": "The average industrial outcome in the companion paper does not clear this central welfare hurdle. Only an exceptionally well-executed industrial programme clearly beats it, and the later beneficiaries are not automatically the households who gave up the grant.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:SRD-002:A01",
          "GSX:SRD-002:A02"
        ],
        "result": "GSX:SRD-002:R01",
        "results": [
          "GSX:SRD-002:R01",
          "GSX:SRD-002:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "The comparison is between a public asset and a social cost. It does not say that cash transfers are always better than investment.",
        "source_study": "GSX:SRD-002",
        "version": "1.0",
        "href": "https://greyscienx.com/research/r350-counterfactual/the-welfare-cost-of-not-paying-the-grant/claims/C02",
        "supported_by": [
          "GSX:SRD-002:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:POP-002": {
    "assumptions": [
      {
        "id": "GSX:POP-002:A01",
        "local_id": "A01",
        "name": "Common earning opportunity",
        "statement": "Six representative lives run from age 20 to 100. Each has the same age-specific earning opportunity, anchored at R30,000 a month at age 25. Potential salary grows by 1.5 percent a year in real terms. Amounts are constant 2026 rand.",
        "value": "30000",
        "unit": "constant 2026 rand per month at age 25",
        "type": "model assumption",
        "provenance": "Manuscript representative-life design",
        "evidence_strength": "illustrative",
        "sensitivity": "high",
        "alternatives": [
          "A different wage path",
          "A different retirement age"
        ]
      },
      {
        "id": "GSX:POP-002:A02",
        "local_id": "A02",
        "name": "Formal saving and return",
        "statement": "Formal workers save 15 percent and the private account earns a smooth 3 percent net real return. Retirement begins at 60. The private pension is price-indexed and calibrated to last through age 100.",
        "value": "15",
        "unit": "percent saved by formal workers",
        "type": "model assumption",
        "provenance": "Manuscript profile table",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "Informal saving of 5 percent",
          "Persistent-exclusion saving of 3 percent"
        ]
      },
      {
        "id": "GSX:POP-002:A03",
        "local_id": "A03",
        "name": "Work histories",
        "statement": "The profiles differ by access to work: stable formal employment from 20, a five-year youth shock, entry only at 30, an interrupted career, mostly informal work, and persistent exclusion.",
        "value": "qualitative",
        "unit": "not a scalar",
        "type": "model assumption",
        "provenance": "Manuscript six-profile table",
        "evidence_strength": "scenario",
        "sensitivity": "high",
        "alternatives": [
          "A different scar or a different number of unemployed years"
        ]
      },
      {
        "id": "GSX:POP-002:A04",
        "local_id": "A04",
        "name": "Simplified public top-up",
        "statement": "The cash transfer is an analytical top-up, not the legal SASSA means test. Its maximum is R2,400 a month. Healthcare costs are held equal across profiles.",
        "value": "2400",
        "unit": "constant 2026 rand per month, maximum top-up",
        "type": "model assumption",
        "provenance": "Manuscript public-support assumptions",
        "evidence_strength": "illustrative",
        "sensitivity": "moderate",
        "alternatives": [
          "A different grant rule"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:POP-002:R01",
        "local_id": "R01",
        "statement": "Private wealth at 60 is R4.84 million after a stable formal career, R3.99 million after a five-year youth shock, R3.09 million if work starts at 30, R0.91 million after a mostly informal career, and R0.15 million under persistent exclusion.",
        "value": "4840000",
        "unit": "constant 2026 rand at age 60, stable formal career",
        "scenario": "Six representative lives, private wealth at 60",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-002:R02",
        "local_id": "R02",
        "statement": "Under persistent exclusion, the modelled grant is 82 percent of retirement cash income.",
        "value": "82",
        "unit": "percent of retirement cash income",
        "scenario": "Persistent exclusion, retirement income",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-002:R03",
        "local_id": "R03",
        "statement": "One million excluded lives produce a modelled lifetime fiscal balance R1.80 trillion weaker, mostly from missing revenue plus higher grants.",
        "value": "1800000000000",
        "unit": "constant 2026 rand",
        "scenario": "One million persistently excluded lives",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:POP-002:M01",
        "local_id": "M01",
        "name": "Lifetime cohort from 20 to 100",
        "statement": "The model follows six work histories that share an earning schedule and differ in employment, formality, saving, and effective tax contribution. Private assets build until 60 and are then drawn through age 100. The fiscal comparison holds healthcare costs equal so the gap comes from taxes and cash transfers."
      }
    ],
    "claims": [
      {
        "id": "GSX:POP-002:C01",
        "local_id": "C01",
        "claim": "In these scenarios, private wealth at 60 is R4.84 million for a stable formal career, R3.99 million after a five-year youth shock, R3.09 million if entry waits until 30, R0.91 million for a mostly informal career, and R0.15 million under persistent exclusion. The amounts are constant 2026 rand and are anchored to the same R30,000 monthly opportunity at age 25.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-002:A01",
          "GSX:POP-002:A02",
          "GSX:POP-002:A03"
        ],
        "result": "GSX:POP-002:R01",
        "results": [
          "GSX:POP-002:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "These are conditional scenarios, not forecasts. Informal work is modelled as lower-paid work with weaker pension coverage, not as work without value. Years worked are not enough: earnings, coverage, and the contribution rate decide how much work becomes retirement wealth.",
        "source_study": "GSX:POP-002",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/todays-unemployment-is-tomorrows-pension-crisis/claims/C01",
        "supported_by": [
          "GSX:POP-002:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-002:C02",
        "local_id": "C02",
        "claim": "Under the persistent-exclusion profile, the modelled grant provides 82 percent of retirement cash income. Scaled to one million such lives, the manuscript reports a lifetime fiscal balance R1.80 trillion weaker, mostly from missing revenue plus higher grants.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-002:A01",
          "GSX:POP-002:A03",
          "GSX:POP-002:A04"
        ],
        "result": "GSX:POP-002:R02",
        "results": [
          "GSX:POP-002:R02",
          "GSX:POP-002:R03"
        ],
        "sensitivity": "high",
        "main_limitation": "The transfer is a simplified analytical top-up, not the legal social-grant means test. Healthcare costs are the same for every profile, so the model does not claim that unemployment itself causes ill health. The fiscal gap is missing tax capacity and greater cash-transfer exposure.",
        "source_study": "GSX:POP-002",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/todays-unemployment-is-tomorrows-pension-crisis/claims/C02",
        "supported_by": [
          "GSX:POP-002:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  },
  "GSX:POP-001": {
    "assumptions": [
      {
        "id": "GSX:POP-001:A01",
        "local_id": "A01",
        "name": "Representative funded saver",
        "statement": "The funded account starts at age 25 with a gross salary of R30,000 a month, continuous employment, and amounts in constant 2026 rand before personal income tax. Salary grows with productivity.",
        "value": "30000",
        "unit": "constant 2026 rand per month, starting gross salary",
        "type": "model assumption",
        "provenance": "Manuscript funded-account specification",
        "evidence_strength": "illustrative",
        "sensitivity": "high",
        "alternatives": [
          "A different contribution rate",
          "A different real return",
          "Retirement at 65 rather than 60"
        ]
      },
      {
        "id": "GSX:POP-001:A02",
        "local_id": "A02",
        "name": "Age-60 funded path",
        "statement": "The age-60 headline path contributes 12 percent, earns a 3 percent net real return, retires at 60, and is tested against life to 90. The target pension in the exhaustion path is 60 percent of final salary.",
        "value": "12",
        "unit": "percent of salary contributed",
        "type": "model assumption",
        "provenance": "Manuscript headline finding and scenario table",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "15 percent contribution",
          "18 percent contribution",
          "5 percent real return"
        ]
      },
      {
        "id": "GSX:POP-001:A03",
        "local_id": "A03",
        "name": "Public pension lens",
        "statement": "The public model is a pay-as-you-go lens, not a replica of South Africa's current tax and grant system. Working life begins at 20, 80 percent of working-age people contribute, and migration is excluded. Survival to the scenario age is rectangular.",
        "value": "80",
        "unit": "percent contributor coverage",
        "type": "model assumption",
        "provenance": "Manuscript public-system specification",
        "evidence_strength": "model assumption",
        "sensitivity": "high",
        "alternatives": [
          "Fertility of 1.3",
          "Fertility of 2.1",
          "Wage indexation instead of prices"
        ]
      },
      {
        "id": "GSX:POP-001:A04",
        "local_id": "A04",
        "name": "Payroll comparison line",
        "statement": "A required pension-only payroll rate at or below 20 percent is the manuscript's comparison ceiling. It is not a legal or universal maximum.",
        "value": "20",
        "unit": "percent of covered payroll",
        "type": "model assumption",
        "provenance": "Manuscript policy comparison line",
        "evidence_strength": "illustrative threshold",
        "sensitivity": "moderate",
        "alternatives": [
          "A country that accepts a higher or lower payroll share"
        ]
      }
    ],
    "results": [
      {
        "id": "GSX:POP-001:R01",
        "local_id": "R01",
        "statement": "For the age-60 path, a pension equal to 60 percent of final salary is exhausted around age 70 when life lasts to 90. The modelled pot at retirement is R3.25 million.",
        "value": "70",
        "unit": "age at which the 60 percent pension is exhausted",
        "scenario": "Start at 25, R30,000 a month, 12 percent contribution, 3 percent net real return, retire at 60, live to 90",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-001:R02",
        "local_id": "R02",
        "statement": "Under the same age-60 and age-90 assumptions, a 12 percent contribution with a 3 percent real return supports only about 27 percent of final salary for life.",
        "value": "27",
        "unit": "percent of final salary supported through age 90",
        "scenario": "Age-60 retirement, life to 90, 12 percent contribution, 3 percent real return",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-001:R03",
        "local_id": "R03",
        "statement": "The public model needs an 18 percent pension-only payroll rate in the short-retirement case, 42 percent in the ageing-squeeze case, and 65 percent in the century-life stress case.",
        "value": "42",
        "unit": "percent of covered payroll, ageing-squeeze case",
        "scenario": "Public pension lens, three demographic stress cases",
        "evidence_status": "modelled"
      },
      {
        "id": "GSX:POP-001:R04",
        "local_id": "R04",
        "statement": "With fertility at 1.7, 80 percent coverage, a 40 percent public benefit, and price indexation, a payroll rate at or below 20 percent requires retirement near 71 if longevity is 90, 75 if it is 95, and 79 if it is 100.",
        "value": "71",
        "unit": "retirement age when longevity is 90",
        "scenario": "Public lens held at or below the 20 percent comparison line",
        "evidence_status": "modelled"
      }
    ],
    "models": [
      {
        "id": "GSX:POP-001:M01",
        "local_id": "M01",
        "name": "Two retirement machines",
        "statement": "One lens is a funded individual account. The other is a pay-as-you-go public pension aged for 260 years so each fertility and longevity pair can settle. The manuscript uses them as lenses. They are not a literal replica of one South African institution."
      }
    ],
    "claims": [
      {
        "id": "GSX:POP-001:C01",
        "local_id": "C01",
        "claim": "In this funded-account model, a worker who starts at 25 on R30,000 a month, contributes 12 percent, and earns a 3 percent net real return exhausts a pension equal to 60 percent of final salary around age 70 if retirement begins at 60 and life lasts to 90.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-001:A01",
          "GSX:POP-001:A02"
        ],
        "result": "GSX:POP-001:R01",
        "results": [
          "GSX:POP-001:R01"
        ],
        "sensitivity": "high",
        "main_limitation": "This is one modelled path, not a forecast and not South Africa's current retirement system. Amounts are constant 2026 rand before personal income tax. A value below zero is a funding shortfall, not literal bank debt. The manuscript also shows that a higher contribution, a higher return, or a later retirement age can support the same target.",
        "source_study": "GSX:POP-001",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/when-retirement-becomes-impossible/claims/C01",
        "supported_by": [
          "GSX:POP-001:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-001:C02",
        "local_id": "C02",
        "claim": "Under those same age-60 and age-90 assumptions, the account supports only about 27 percent of final salary for life. It does not support a 60 percent replacement at a 12 percent contribution and a 3 percent real return.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-001:A01",
          "GSX:POP-001:A02"
        ],
        "result": "GSX:POP-001:R02",
        "results": [
          "GSX:POP-001:R02"
        ],
        "sensitivity": "high",
        "main_limitation": "The replacement map holds salary growth at 1.5 percent real and indexes the pension to prices. A 60 percent target in the manuscript requires a much higher contribution, a higher return, or a later retirement age.",
        "source_study": "GSX:POP-001",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/when-retirement-becomes-impossible/claims/C02",
        "supported_by": [
          "GSX:POP-001:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      },
      {
        "id": "GSX:POP-001:C03",
        "local_id": "C03",
        "claim": "In the public-pension lens, the required pension-only payroll rate is 18 percent in the short-retirement case, 42 percent in the ageing-squeeze case, and 65 percent in the century-life stress case. Holding fertility at 1.7, coverage at 80 percent, and the benefit at 40 percent with price indexation, a rate at or below 20 percent requires retirement near 71, 75, or 79 as longevity rises from 90 to 100.",
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": null,
        "depends_on": [
          "GSX:POP-001:A03",
          "GSX:POP-001:A04"
        ],
        "result": "GSX:POP-001:R03",
        "results": [
          "GSX:POP-001:R03",
          "GSX:POP-001:R04"
        ],
        "sensitivity": "high",
        "main_limitation": "These are modelled rates for one pension promise. They are not estimates of South Africa's current tax system. Rectangular survival and the exclusion of migration make the longevity stress easy to read and deliberately stark. The 20 percent line is a comparison ceiling chosen by the manuscript, not a universal law.",
        "source_study": "GSX:POP-001",
        "version": "1.0",
        "href": "https://greyscienx.com/research/population-futures/when-retirement-becomes-impossible/claims/C03",
        "supported_by": [
          "GSX:POP-001:PDF"
        ],
        "contradicted_by": [],
        "qualifies": [],
        "contradicts": []
      }
    ]
  }
};
