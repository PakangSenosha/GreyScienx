# Preregistered analysis plan

Protocol version 1.0 is frozen before interpreting the visible-world or replication outputs. The player manifest is assigned once and reused in all worlds. The visible seed commitment is SHA-256 of the unrevealed seed; this local completed run publishes both commitment and revealed seed in `run-metadata.json`.

## Primary hypotheses

1. Greater turnover predicts more negative expected and observed P&L when game mix is held constant.
2. Frequent cohorts approach weighted theoretical RTP faster than infrequent cohorts.
3. Large-stake cohorts have earlier ruin and wider short-run P&L dispersion.
4. Loss-chasing raises post-loss turnover and repeated-allocation exhaustion.
5. Strict session limits reduce exposure and session loss without changing wager expectation.
6. The two 96% RTP slots have similar expected loss but different ruin and winner distributions.
7. The profitable fraction declines with accumulated negative-expectation exposure.
8. Month-one leaders regress and imperfectly predict month-six rank.
9. Visible extreme winners are less extreme at the same policy's across-world median.
10. Matched American-roulette exposure has worse expectation than European roulette.

## Primary estimands

- Cohort differences in median final allocation-adjusted P&L, first-ruin probability, and allocations consumed.
- Relationship between turnover and observed/expected P&L.
- Ruin-distribution difference between the equal-RTP slot models.
- Difference between visible rank and median rank over 1,000 worlds.

All percentages retain the full player denominator. Inactive players are never silently removed. Results are descriptive of this model. Broad exploratory comparisons require false-discovery control and confirmation on held-out seeds before any inferential language.
