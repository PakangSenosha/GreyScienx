# GreyScienx Virtual Casino Experiment v1.0

This directory is the local minimum credible release of a synthetic, read-only statistical observatory. It contains no payment path, prize, transferable balance, visitor wager control, operator link, real-match feed, or strategy recommendation.

## Reproduce the release

From the repository root:

```bash
npm run casino:test
npm run casino:generate
npm run casino:replay
npm run build
```

`casino:generate` freezes the 1,000-player manifest, runs the six-calendar-month visible world, writes its hash-chained wager ledger, runs 1,000 independent replication worlds, and creates the dashboard/download bundle. `casino:replay` verifies every event hash and accounting invariant, reruns the visible world from the revealed seed, and compares final hashes.

Generated research artifacts live in `artifacts/v1.0/`. The explicitly public, read-only download copies live in `public/experiments/virtual-casino/v1.0/` with SHA-256 checksums.

## Local release boundary

The release is complete as a locally runnable research product. PostgreSQL, Redis, background workers, live pacing, external seed-commitment timestamping, durable object storage, and a scale-out 10,000-world run are intentionally not provisioned locally. See `PRODUCTION-SCALE.md`.

The blackjack engine uses frozen, exact resolved-hand probability tables for three declared policy classes. It does not claim to be a card-by-card casino shoe. That abstraction is visible in the methods, dashboard, and limitation text.
