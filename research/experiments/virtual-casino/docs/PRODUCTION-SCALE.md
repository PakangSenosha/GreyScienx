# Production-scale boundary

The local release validates the protocol and product without purchasing or provisioning infrastructure. The following components are deliberately documented rather than silently simulated as production services:

1. PostgreSQL append-only partitions for full ledgers, materialised aggregates, and authenticated administration.
2. Queue-backed deterministic workers with idempotent batch keys and checkpoint resume.
3. Object storage with retention policy, signed release manifests, and external timestamping of the pre-launch seed commitment.
4. A cache or event stream for 1–5 second public snapshot refreshes.
5. Rate limiting and export-size controls at the deployed edge.
6. A 10,000-world scale run after compute, storage, and rare-tail stability review.
7. A card-by-card blackjack shoe with legal-action policy tables and independently verified conditional EVs.
8. Independent accessibility, security, statistical, and responsible-gambling-content review before public launch.

The included SQL schema captures the intended relational constraints. Public routes remain snapshot-only until these controls exist. No deployment, public launch, secret provisioning, paid service, or seed escrow was performed.
