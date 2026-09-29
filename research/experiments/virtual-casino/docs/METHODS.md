# Methods

## Population and time

The run contains exactly 1,000 policies: 100 in each of ten preregistered cohorts. Each begins with 1,000,000 synthetic cents (R10,000). The shared calendar covers 181 days from 1 January 2026. A bankroll month is an allocation episode and is not a calendar month.

Sessions are scheduled from a player-specific stream over 26 weeks. Game choice, bet choice, stake variation, and each game's outcomes use independent xoshiro128** streams initialised by the documented cyrb128 string mixer over stable identifiers. SHA-256 is separately used for seed commitments, manifests, checkpoints, and the ledger hash chain. Worker count, dashboard refresh, and event batching do not enter stream derivation.

## Bankroll protocol

A stake is rounded down to whole rand, then bounded by the game's minimum and maximum, the policy cap, the experiment cap, and available bankroll. Ruin is tested after settlement when less than R1 remains, the minimum legal stake in the declared catalogue. Exactly R10,000 is injected after ruin until six allocations have been used; cumulative statistics are never reset. After sixth-allocation ruin the policy is inactive.

Lifetime net P&L is current bankroll minus all allocated capital. At the aggregate level, casino GGR equals handle minus gross payouts and equals the negative of player wager P&L. Allocation injections are not payouts or winnings.

## Game mathematics

- European roulette: 37 equiprobable pockets and standard payouts; every listed bet has exact RTP 36/37.
- American roulette: 38 equiprobable pockets including 00; every listed bet has exact RTP 36/38.
- Blackjack: frozen resolved-hand distributions for basic, novice, and random policy classes under the declared six-deck S17/DAS/3:2 abstraction. Exact RTPs are 97.55%, 95.35%, and 91.75%. This is not a card-by-card shoe implementation.
- Baccarat: standard eight-deck outcome probabilities rounded to one-million probability units. Banker pays 0.95 profit; Player pays even money; Tie pays 8:1.
- Three-reel slot: published one-million-stop categorical table, 96% RTP, 50% nonzero return, 31x maximum gross payout.
- High-volatility slot: published one-million-stop table, 96% RTP, 14% nonzero return, 137x maximum gross payout.
- Craps: restricted resolved-bet catalogue for pass line, field, and any seven.
- Virtual sports: synthetic independent event probabilities only. Offered decimal odds are `(1 - 0.06) / true_probability`; singles and two-leg parlays are supported.
- Crash: cash-out target declared before sampling, with `P(reach target) = 0.97 / target`.
- Lottery: one-million-ticket table with 80% RTP and a 40-in-one-million 10,000x gross jackpot.

The exact tables, bet-level RTPs, rules, realised returns, and event draw references are published in the artifact bundle.

## Replication

One thousand independent world seeds hold the manifest and rules fixed while resampling declared stochastic scheduling, choices, and outcomes. Player-level summaries publish probability of profit and ruin, 1st/5th/50th/95th/99th P&L percentiles, median turnover, median wagers, and median rank. The visible world is not used to tune policies.
