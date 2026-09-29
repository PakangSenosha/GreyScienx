# Methods

## Separate experiment

Make It Big is a nested study under the GreyScienx Virtual Casino. The original experiment follows 1,000 heterogeneous policies with R10,000 bankroll allocations for six calendar months. This study instead holds monthly spend constant and models time to a single R100,000-or-larger gross payout. Its entrants, endpoints, seeds, and results are independent of the original experiment.

## Design

Each cell contains 100,000 synthetic entrants and combines one game model with one fixed-budget strategy: 20 × R50, 50 × R20, 100 × R10, or 200 × R5 wagers per month. Every arm therefore spends at most R1,000 per month, R12,000 in one year, and R36,000 in three years.

The primary endpoint is the first wager with gross payout of at least R100,000. The 12- and 36-month no-hit outcomes are reported as budget exhaustion at those horizons. A hit exits the entrant immediately. Spend before a hit includes the successful wager.

## Game models

All four rulesets are Class C synthetic experimental games. This is deliberate: the study compares tail structures under fully disclosed probability laws and makes no claim to reproduce a named operator product.

- Controlled jackpot slot: a fixed multiplier table with 96% theoretical RTP and separate 2,000×, 5,000×, 10,000×, and 20,000× tails.
- Controlled crash target: a declared multiplier with `P(success) = 0.97 / multiplier`, producing 97% theoretical RTP.
- Controlled lottery tail: an independent 100,000× outcome with probability 8 per million, producing 80% theoretical RTP.
- Controlled virtual accumulator: a declared synthetic target with `P(success) = 0.90 / multiplier`, producing 90% theoretical RTP. No real matches are used.

## Estimation

For a per-wager target probability `p` and `n` attempts, exact cumulative incidence is `1 - (1 - p)^n`; survival is `(1 - p)^n`. Seeded Monte Carlo draws a geometric first-passage index for every entrant. This compression is sufficient for the preregistered endpoint and avoids writing billions of redundant non-target wager rows. The audit file retains the first 25 entrants from every cell, while the source and seed reproduce every path.

The dashboard reports exact probabilities as the estimand and Monte Carlo values as a reproducibility check. It also reports entrants and aggregate synthetic spend per observed winner, median bets, months, and spend before a hit, and the probability of reaching each spending cap without success.

## Limits

- Synthetic entrants are not people.
- The four distributions are controlled models, not a catalogue of commercial games.
- RTP does not determine target-hit probability by itself.
- Gross target payout is not net profit.
- Independent wagers omit changing behaviour, credit constraints, and voluntary exit.
- Rare-event estimates for real products require verified, product-specific paytables.
