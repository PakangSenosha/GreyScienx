# Make It Big study v1.0

This is a separate rare-event experiment within the GreyScienx Virtual Casino. It does not replace or alter the six-month 1,000-player bankroll experiment.

The study asks how often a synthetic low-stakes entrant receives one gross payout of at least R100,000 before spending R12,000 or R36,000. Four fixed-budget strategies each spend exactly R1,000 per simulated month. Four transparent Class C game models expose different tail shapes. They are controlled mathematical models, not copies of named commercial products.

## Reproduce the release

From the repository root:

```bash
npm run casino:make-it-big:test
npm run casino:make-it-big:generate
```

The generator runs 100,000 deterministic entrant paths in each of 16 preregistered cells. It publishes exact Bernoulli first-passage probabilities beside seeded Monte Carlo estimates, survival data, winner-economics summaries, an audit sample, source, protocol, and SHA-256 checksums.

## Interpretation boundary

The endpoint is a gross single-wager payout, not profit or wealth. A target hit is reported with spend before the hit. Results describe only the published synthetic distributions and must not be used as gambling advice or as estimates for an undisclosed real-world product.
