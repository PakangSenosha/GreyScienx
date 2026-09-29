# Data dictionary

All monetary fields ending in `Cents` are integer synthetic South African cents.

## Wager event

- `betId`: unique accepted-wager settlement identifier.
- `sequenceNumber`: monotonically increasing world sequence.
- `playerId`, `cohortId`, `gameId`, `gameRuleVersion`: frozen entity/version references.
- `simulatedAt`, `sessionId`, `bankrollMonth`: the two clocks and session context.
- `bankrollBeforeCents`, `stakeCents`, `grossPayoutCents`, `netPnlCents`, `bankrollAfterCents`: settlement amounts satisfying `after = before - stake + payout`.
- `choice`, `outcome`: game-specific wager and realised result.
- `rngStreamId`, `rngCounterOrDrawReference`: deterministic draw address.
- `theoreticalEvCents`: wager-specific expected gross payout minus stake, rounded to cents.
- `policyStateBeforeHash`, `policyStateAfterHash`: hashes of decision-relevant state.
- `previousEventHash`, `eventHash`: immutable ledger chain.

## Player summary

- `currentBankrollCents`: balance in the active/final allocation.
- `cumulativeAllocatedCents`: R10,000 times allocations used.
- `netPnlCents`: current bankroll minus cumulative allocated capital.
- `cumulativeExpectedPnlCents`: sum of wager-specific theoretical expected P&L.
- `deviationFromExpectationCents`: observed minus expected P&L.
- `ruinCount`, `allocationsUsed`, `status`: reset/cap state.

## Casino summary

- `handleCents`: sum of stakes.
- `payoutCents`: sum of gross returned amounts.
- `ggrCents`: handle minus payouts.
- `actualRtp`: payouts divided by handle.
- `theoreticalRtp`: stake-weighted expected gross payout divided by handle.

The CSV exports use the same names. Nested objects are JSON-encoded inside CSV cells.
