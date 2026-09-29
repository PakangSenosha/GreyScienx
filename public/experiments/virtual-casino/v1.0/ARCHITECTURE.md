# Architecture audit and release design

## Repository audit

The host repository is a small Next.js 16 App Router publication with static catalogue data, shared header/footer components, and one global visual system. Before this work it contained the v1.0 specification but no simulator, experiment storage, API, tests, or casino route. The working tree already contained unrelated research and social-publication files; this implementation does not modify them.

## Local reference architecture

```text
protocol-v1.0.json ──> policy manifest
         │                    │
         ├──> behaviour engine│
         └──> game engines ───┴──> deterministic world runner
                                      │
                         ┌────────────┴────────────┐
                         v                         v
                hash-chained ledger         1,000 world summaries
                         │                         │
                         └──────────┬──────────────┘
                                    v
                          reconciled artifacts
                                    │
                                    v
                     static read-only Next.js views/API
```

The local architecture deliberately uses versioned files rather than introducing a database and queue before the protocol is validated. The simulation is offline; public request paths only read generated snapshots. There is no public write endpoint and no simulator code runs because a visitor requested a wager.

## Service boundaries represented in code

- `engine/policies.mjs`: assignment, scheduling, game selection, choices, and bounded staking. It contains no payout logic.
- `engine/games.mjs`: validated outcomes, payouts, and wager-specific expected values. It contains no cohort logic.
- `engine/simulate.mjs`: session, bankroll, ruin, reset, allocation-cap, ledger, and world orchestration.
- `engine/random.mjs`: SHA-256-derived deterministic streams isolated by world, player, game, and purpose.
- `engine/analysis.mjs`: aggregates, distributions, checkpoints, and replication summaries.
- `scripts/replay.mjs`: independent hash-chain, arithmetic, duplicate-settlement, allocation-cap, final-state, and GGR reconciliation.

## Immutability model

Each ledger event contains its sequence number, the previous event hash, and a SHA-256 hash over its canonical payload and predecessor. Generated ledger files are never updated in place by application code. A rule or display-definition change requires a new version directory and changelog entry.
