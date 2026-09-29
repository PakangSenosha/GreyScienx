# GreyScienx Virtual Casino Experiment

**Status:** Full experiment and product specification  
**Version:** 1.0  
**Experiment type:** Public, live, synthetic-agent simulation  
**Population:** 1,000 coded behavioural agents  
**Games:** 10 mathematically specified virtual games  
**Primary duration:** Six simulated calendar months  
**Replication target:** Up to 10,000 independently seeded worlds  
**Money:** Synthetic South African rand only; no deposits, withdrawals, prizes, or items of value

> **Public premise:** 1,000 synthetic players enter with identical R10,000 bankrolls. Their behaviour differs, every wager is logged, and the resulting distribution unfolds in public.

---

## 1. Executive summary

The GreyScienx Virtual Casino Experiment is a reproducible simulation laboratory designed to show how casino mathematics, betting frequency, bet size, game selection, bankroll management, behavioural adaptation, and luck interact over time.

The experiment begins with 1,000 synthetic players. Every player receives an initial virtual bankroll of **R10,000** and follows a coded, auditable behavioural policy. The players are divided into ten primary cohorts of 100, but their parameters are varied within each cohort so they are not clones.

Players may choose among ten games with deliberately different combinations of house edge, volatility, decision intensity, betting frequency, and payout-tail shape. When a player exhausts a R10,000 bankroll, the experiment records a ruin event, supplies a fresh R10,000 virtual allocation, and advances that player to a new **bankroll month**. The primary run lasts six simulated calendar months and permits no more than six R10,000 allocations per player.

The public dashboard resembles a transparent casino operations console, while remaining clearly labelled as a research simulation. It reports total virtual turnover, player payouts, gross gaming result, actual and theoretical return to player, player profit and loss, ruin counts, allocation usage, cohort comparisons, and the full distribution of outcomes. Individual player pages expose the difference between observed profit and expected loss given the wagers actually placed.

The visible world is only one realised path. In the backend, the same 1,000 behavioural policies are rerun in independently seeded replication worlds. This reveals whether an apparent star player has a genuinely less harmful policy or merely occupied the extreme right tail in one world.

The project is not a gambling product. It accepts no money, pays no money or prizes, provides no player wagering interface, and must not promote or facilitate gambling. Its purpose is statistical education and behavioural research.

---

## 2. Research question

### Central question

> Over repeated gambling, how do bet size, betting frequency, game choice, behavioural style, and bankroll management affect the probability of remaining profitable when every player begins with the same amount of money?

### Supporting questions

1. How quickly does frequent play make realised returns converge toward each game's theoretical return?
2. Do large bettors have a higher probability of both spectacular short-term profit and early ruin?
3. Which matters more for ruin: stake size, game edge, game volatility, or betting frequency?
4. Does a stop-loss or stop-win rule change losses, turnover, time in play, or only the timing of exposure?
5. How often do loss-chasing policies create temporary recoveries before increasing cumulative losses and ruin risk?
6. How many players remain profitable after 1, 10, 100, 1,000, 10,000, and 100,000 wagers?
7. What proportion of Month 1 winners are still winners after Month 6?
8. How strongly does total turnover predict cumulative loss?
9. How long can an unusually lucky player appear skilful?
10. How many apparently successful strategies arise through chance when 1,000 policies are observed simultaneously?
11. Does a winning player's result replicate when the same policy is rerun under new random-number seeds?
12. Can two games with equal theoretical return produce radically different player experiences because their volatility differs?

---

## 3. Scope and non-goals

### In scope

- A deterministic, seeded simulation engine.
- 1,000 heterogeneous behavioural agents.
- Ten virtual games with published rules, outcome distributions, and theoretical returns.
- Six simulated calendar months in the primary world.
- R10,000 bankroll allocations and precisely logged reset events.
- A live, public, read-only dashboard.
- An immutable wager-level ledger.
- Cohort, game, player, and casino-level analytics.
- Repeated replication worlds for separating policy effects from luck.
- Downloadable configurations, seeds, aggregate data, and reproducibility documentation.
- Explicit uncertainty, limitations, and responsible presentation.

### Out of scope

- Real-money gambling or simulated deposits.
- Withdrawals, transferable credits, prizes, coupons, tokens, crypto-assets, or anything of value.
- User-controlled betting or the ability for visitors to imitate a casino session.
- Odds comparison, tips, strategy optimisation for real gambling, or claims that any system beats the house.
- Affiliate links, operator advertising, inducements, VIP mechanics, or acquisition funnels.
- Use of identifiable real gamblers or private gambling data.
- Autonomous large-language-model agents placing individual wagers.
- Claims about clinical gambling behaviour or causal effects on humans without a separately approved human-subject study.

---

## 4. Experimental design

### 4.1 Population

The primary population is:

\[
N = 1{,}000
\]

Each synthetic player has:

- a stable `player_id`;
- a primary cohort;
- a parameterised behavioural policy;
- a weighted game-preference vector;
- session frequency and duration rules;
- stake-sizing rules;
- responses to wins, losses, streaks, and bankroll changes;
- optional stop-loss and stop-win rules;
- a deterministic random stream derived from the world seed and player identifier.

Agents are coded state machines or policy functions. They may adapt according to predeclared rules, but they do not improvise via an LLM during the experiment.

### 4.2 Ten cohorts

The population is stratified into ten cohorts of 100 players:

| Cohort | Primary behaviour | Typical exposure | Defining rule |
|---:|---|---|---|
| 1 | Small bets, very frequent | High wager count, low stake | Small bankroll fraction per bet; many sessions and bets |
| 2 | Small bets, infrequent | Low wager count, low stake | Small bankroll fraction; few sessions |
| 3 | Medium bets, frequent | High wager count, medium stake | Moderate bankroll fraction; many sessions |
| 4 | Medium bets, infrequent | Low wager count, medium stake | Moderate bankroll fraction; few sessions |
| 5 | Large bets, frequent | Very high risk exposure | Large bankroll fraction; many sessions |
| 6 | Large bets, infrequent | High single-bet variance | Large bankroll fraction; few sessions |
| 7 | Loss-chasing | Path-dependent escalation | Stakes rise after losses or losing streaks |
| 8 | Strict limits | Bounded session exposure | Enforced stop-loss and stop-win thresholds |
| 9 | Variable/random staking | Irregular exposure | Stake and sometimes game drawn from declared distributions |
| 10 | Random control | Behavioural baseline | Choices sampled without outcome-responsive adaptation |

These labels describe dominant behaviour, not identical agents. Each player's exact values are sampled once from a preregistered range and saved in the player manifest.

### 4.3 Within-cohort heterogeneity

Within each cohort, vary at minimum:

- base stake as a percentage of available bankroll;
- sessions per simulated week;
- bets per session;
- preferred games and weights;
- stop-loss and stop-win thresholds;
- sensitivity to recent wins and losses;
- maximum permitted stake;
- propensity to switch games;
- willingness to end a session while ahead;
- cooldown after ruin;
- adaptation strength.

Example player policy:

```yaml
player_id: P0447
cohort: loss_chasing
starting_allocation_zar: 10000
base_stake_fraction: 0.028
sessions_per_week: 5
bets_per_session_mean: 43
game_weights:
  european_roulette: 0.40
  blackjack: 0.25
  standard_slot: 0.35
loss_response:
  stake_multiplier_after_loss: 1.18
  maximum_consecutive_escalations: 4
win_response:
  stake_multiplier_after_win: 0.95
stop_loss_fraction_of_session_start: 0.42
stop_win_fraction_of_session_start: 0.75
```

### 4.4 Assignment and balance

- Cohort membership is fixed before the run.
- Game preferences are assigned from balanced distributions so every game receives adequate exposure.
- Player parameters are generated from versioned distributions using a dedicated assignment seed.
- The same player-policy manifest is reused across all replication worlds.
- Only stochastic game outcomes and any explicitly randomised policy choices change between worlds.
- Where a comparison requires causal interpretation, use paired policies or factorial assignments rather than comparing self-selected game use alone.

---

## 5. Bankroll and reset protocol

### 5.1 Initial state

Every player begins the primary world with:

\[
B_0 = R10{,}000
\]

All money is synthetic. The ledger records amounts in integer cents to prevent floating-point rounding errors.

### 5.2 Two clocks

The experiment distinguishes two concepts that must never be conflated:

1. **Simulated calendar time:** the shared six-month experimental timeline.
2. **Bankroll month:** a player's numbered R10,000 allocation episode.

A player may remain in Bankroll Month 1 for the entire six-month calendar run if they never exhaust the first allocation. A player who goes broke repeatedly can advance through several bankroll months in a short span of simulated calendar time.

### 5.3 Ruin definition

A player is ruined when the available bankroll is below the minimum legal stake for every game the policy may select, or equals zero. The engine must not allow a stake larger than the available bankroll.

Ruin is evaluated after all payouts for the wager are settled. The event records:

- simulated timestamp;
- bankroll immediately before the final wager;
- final stake, outcome, and payout;
- number of wagers in the allocation;
- turnover in the allocation;
- allocation duration;
- cumulative allocations consumed.

### 5.4 Reset rule

On ruin:

1. Close the current allocation episode.
2. Record one ruin event.
3. Increment `bankroll_month` by one.
4. Add exactly R10,000 in synthetic funds if the player has not reached the allocation cap.
5. Preserve lifetime profit-and-loss, turnover, and ruin history; do not reset cumulative statistics.
6. Apply any preregistered cooldown before the next session.

### 5.5 Allocation cap

The primary protocol allows six allocations:

\[
A_{max} = 6
\]

The maximum synthetic capital supplied to one player is therefore:

\[
6 \times R10{,}000 = R60{,}000
\]

After the sixth allocation is exhausted, the player becomes inactive for the remainder of the primary run and is labelled **used all six allocations**.

### 5.6 Profit-and-loss definitions

For player \(i\):

\[
\text{Total Allocated}_i = R10{,}000 \times \text{Allocations Used}_i
\]

\[
\text{Net P\&L}_i = \text{Ending Bankroll}_i - \text{Total Allocated}_i
\]

This definition prevents a reset from being mistaken for a recovery. A player with R5,000 remaining after consuming three allocations has:

\[
R5{,}000 - R30{,}000 = -R25{,}000
\]

If a player turns the first R10,000 into R607,000 and never resets, net P&L is:

\[
R607{,}000 - R10{,}000 = +R597{,}000
\]

The dashboard must show both current bankroll and lifetime net P&L.

---

## 6. Game catalogue

Each game is defined in a versioned configuration containing its outcome space, probabilities, payout function, permitted choices, minimum and maximum stakes, theoretical return, and variance characteristics. Published values must be calculated from the implemented rules, not entered as decorative labels.

| # | Game | Decision intensity | Volatility | Typical frequency | Scientific role |
|---:|---|---|---|---|---|
| 1 | European Roulette | Medium | Medium | Medium | Simple baseline; single-zero wheel |
| 2 | American Roulette | Medium | Medium | Medium | Clean rule-change comparison using `00` |
| 3 | Blackjack | High | Medium | Medium | Tests decision quality and strategy errors |
| 4 | Baccarat | Low | Low–medium | Medium | Compares Banker, Player, and high-edge Tie choices |
| 5 | Three-Reel Slot | None | Medium | Very high | Repeated small bets and rapid convergence |
| 6 | High-Volatility Video Slot | None | Very high | Very high | Rare large payouts; same-RTP volatility study |
| 7 | Craps / Dice | High | Medium–high | High | Wide range of bet-specific house edges |
| 8 | Virtual Sports Betting | High | High | Low–medium | Bookmaker margin, parlays, favourites, and underdogs |
| 9 | Crash | Medium | Very high | High | Cash-out thresholds and tail-chasing behaviour |
| 10 | Lottery / Jackpot | Minimal | Extreme | Low | Extreme right tail and winner salience |

### 6.1 European Roulette

- Use a 37-pocket wheel numbered 0–36.
- Support even-money, dozen, column, straight-up, and a limited set of split/corner bets.
- Record bet type separately because theoretical loss differs by neither layout nor staking system under standard payouts, while volatility does.
- Use it as the primary transparent demonstration of expected value.

### 6.2 American Roulette

- Use a 38-pocket wheel numbered 0, 00, and 1–36.
- Match the European implementation wherever possible except for the added `00`.
- Use paired agents to quantify the long-run impact of a small rules change.

### 6.3 Blackjack

- Freeze deck count, penetration, dealer rules, blackjack payout, doubling, splitting, surrender, and reshuffle behaviour in the experiment config.
- Provide declared policies such as basic strategy, random legal action, simplified novice play, conservative play, and aggressive doubling/splitting.
- Calculate expected value conditional on rule set and policy; do not publish one universal blackjack RTP.
- Keep card streams deterministic and auditable.

### 6.4 Baccarat

- Implement Player, Banker, and Tie outcomes using a specified shoe and drawing rules.
- Apply the declared Banker commission or alternative payout rule.
- Track bet-type selection because Tie betting has a materially different expectation from the main bets.

### 6.5 Three-Reel Slot

- Implement explicit virtual reels or a published probability table.
- Use a moderate-volatility paytable and a fixed target theoretical return.
- Log the raw stop positions or outcome identifier so every spin can be replayed.

### 6.6 High-Volatility Video Slot

- Set the same target theoretical return as the three-reel slot for the primary volatility comparison.
- Concentrate more return in rare, large payouts.
- Make the full paytable, hit rate, and maximum payout public.

The critical experiment is:

\[
RTP_A = RTP_B, \qquad Var(A) \ll Var(B)
\]

The expected long-run loss is similar, but the distribution of ruin, temporary profit, and extreme winners can differ sharply.

### 6.7 Craps / Dice

- Implement a restricted, clearly documented set of bets rather than an entire casino table on day one.
- Include low-edge and high-edge choices.
- Track whether adaptive agents migrate toward more visually exciting but mathematically worse wagers.

### 6.8 Virtual Sports Betting

- Generate synthetic events from a calibrated probability model; do not ingest real matches or enable real-world wagering.
- Construct odds by applying a declared bookmaker margin to latent event probabilities.
- Include singles and limited parlays.
- Store the true simulated event probability, offered odds, implied probability, and margin for each wager.

### 6.9 Crash

- Generate crash multipliers from a published, seeded distribution with a known house edge.
- Policies declare cash-out targets before the round result is sampled.
- Never let an agent revise a cash-out threshold after seeing the result.
- Compare low cash-out targets with tail-chasing targets.

### 6.10 Lottery / Jackpot

- Use a published prize table and exact draw probabilities.
- Keep bet frequency low and right-tail payouts extreme.
- Separate jackpot contributions, ordinary prizes, and unclaimed synthetic prize states.

### 6.11 Game validation requirement

Before launch, each game must pass:

- exact or independently calculated theoretical return verification;
- payout conservation and boundary tests;
- Monte Carlo convergence tests at large sample sizes;
- deterministic replay tests from seed and wager input;
- invalid-bet and insufficient-bankroll tests;
- statistical tests of outcome frequencies;
- review confirming that dashboard labels match ledger definitions.

---

## 7. Player behaviour engine

### 7.1 Policy cycle

At each eligible session, the engine performs:

1. Determine whether the player starts a session according to the schedule policy.
2. Select a game from the current preference vector.
3. Select a legal bet type or action policy.
4. Calculate the proposed stake.
5. Clamp the stake to game limits and available bankroll.
6. Sample the game outcome from the correct deterministic random stream.
7. Settle the wager and append an immutable ledger event.
8. Update player state, streak state, and behavioural parameters.
9. Test stop-loss, stop-win, session-length, and ruin conditions.
10. Schedule the next decision.

### 7.2 Stake model

A general stake function may be expressed as:

\[
s_{i,t} = \min\left(B_{i,t},\; L_g,\; B_{i,t} \cdot f_i \cdot m_{i,t}\right)
\]

where:

- \(B_{i,t}\) is available bankroll;
- \(L_g\) is the game stake cap;
- \(f_i\) is the player's base bankroll fraction;
- \(m_{i,t}\) is a bounded behavioural multiplier based on recent outcomes.

All multipliers require hard caps. No policy may create an invalid stake or an unbounded escalation loop.

### 7.3 Adaptive behaviour

Permitted adaptations include:

- increasing or decreasing stakes after a win or loss;
- bounded loss-chasing after a losing streak;
- switching games after repeated losses;
- increasing preference for a game after a large win;
- leaving while ahead;
- pausing after ruin;
- reverting toward baseline preferences over time.

Every adaptation must be specified before the run. No post hoc change may be introduced into the live world without creating a new experiment version.

### 7.4 Preference examples

```text
Player P0042
European Roulette     50%
Blackjack             30%
Three-Reel Slot       10%
Virtual Sports        10%
```

```text
Player P0723
High-Volatility Slot  80%
Crash                 20%
```

### 7.5 Expected outcome decomposition

For each player, report:

\[
\text{Observed P\&L}
=
\text{Expected P\&L given wagers}
+
\text{Deviation from expectation}
\]

The expected component is computed wager by wager using the selected game's rules and the exact bet choice:

\[
E[\text{P\&L}_i] = \sum_{j=1}^{n_i} E[X_{ij}]
\]

The deviation is descriptive of realised luck, not proof of a separately identifiable causal quantity. Behaviour affects both the wagers chosen and the distribution of exposures, so the public explanation must avoid implying that luck and behaviour can always be perfectly separated in one observed path.

Example display:

```text
Player P0023
Expected P&L given wagers    -R43,000
Observed P&L                +R607,000
Deviation from expectation  +R650,000
```

---

## 8. Time and simulation pacing

### 8.1 Primary run

- Duration: six simulated calendar months.
- Default public pacing: configurable, for example one simulated day every 10 real minutes.
- The backend is authoritative; animation speed must not change results.
- Session timestamps are generated in simulated time.
- The primary world seed and player manifest are frozen before launch.

### 8.2 Public update cadence

- Wagers may be processed continuously in batches.
- Dashboard summaries update every 1–5 seconds.
- Player pages may update at a lower frequency to control load.
- Charts use aggregated windows rather than rendering every wager.
- A visible timestamp states the latest fully processed simulated time.

### 8.3 Checkpoints

Create signed or hashed checkpoints at:

- initial state;
- end of every simulated day;
- end of every simulated month;
- final state.

Each checkpoint stores the experiment version, config hash, seed manifest hash, last ledger event, aggregate totals, and player state hash.

---

## 9. Hypotheses

The analysis plan should be preregistered before the primary seed is revealed or the visible run starts.

### Primary hypotheses

**H1 — Exposure hypothesis**  
Greater cumulative turnover will predict more negative expected and observed player P&L, holding game mix constant.

**H2 — Frequency convergence hypothesis**  
High-frequency cohorts will converge toward their weighted theoretical return more quickly than low-frequency cohorts.

**H3 — Stake-size ruin hypothesis**  
Large-stake cohorts will show higher early ruin probability and wider short-run P&L dispersion than otherwise similar small-stake cohorts.

**H4 — Loss-chasing hypothesis**  
Loss-chasing policies will increase turnover following losses and raise the probability of exhausting multiple allocations.

**H5 — Limit-setting hypothesis**  
Strict stop-loss policies will reduce per-session loss and total exposure, although they do not reverse negative expected value on wagers placed.

**H6 — Volatility hypothesis**  
Equal-RTP slot games with different variance will have similar long-run aggregate expected loss but substantially different ruin rates, winner concentration, and short-run player experiences.

**H7 — Persistence hypothesis**  
The proportion of players in cumulative profit will decline as wager count and exposure increase in negative-expectation games.

**H8 — Winner persistence hypothesis**  
Many early leaders will regress toward the population distribution, and Month 1 rank will imperfectly predict Month 6 rank.

**H9 — Replication hypothesis**  
Extreme winners in the visible world will usually show much less extreme median results across independently seeded worlds.

**H10 — Rules-matter hypothesis**  
Paired policies exposed to American roulette will experience worse long-run outcomes than those exposed to European roulette under otherwise matched conditions.

### Secondary and exploratory hypotheses

- High-volatility games will create more visually salient winners despite equal or worse median outcomes.
- Variable staking will widen distributions without improving mean expected return.
- Game switching after losses will not create positive expectation when all destination games remain negative expectation.
- Parlays and high-edge side bets will increase the gap between handle and payout.
- Some policies will appear superior in a single world but fail out-of-sample across replication worlds.

Exploratory findings must be labelled exploratory and should not be presented as confirmed hypotheses.

---

## 10. Outcome measures

### 10.1 Casino-level metrics

Total handle:

\[
\text{Handle} = \sum \text{all stakes}
\]

Player payouts:

\[
\text{Payouts} = \sum \text{all returned amounts}
\]

Gross gaming result:

\[
GGR = \text{Handle} - \text{Payouts}
\]

Actual return to player:

\[
RTP_{actual} = \frac{\text{Payouts}}{\text{Handle}}
\]

Weighted theoretical return:

\[
RTP_{theoretical} =
\frac{\sum_j \text{Stake}_j \times RTP_j}{\sum_j \text{Stake}_j}
\]

Also report:

- total wagers;
- active players;
- casino result by game and simulated day;
- deviation of actual from theoretical return;
- concentration of payouts among top winners;
- number and value of allocations supplied.

### 10.2 Player-level metrics

- current bankroll;
- total allocated capital;
- lifetime net P&L;
- expected P&L given actual wagers;
- deviation from expectation;
- total turnover;
- wager count;
- sessions completed;
- allocations used;
- ruin count and time to first ruin;
- maximum drawdown;
- peak bankroll;
- longest win and loss streaks;
- game mix;
- average and median stake;
- realised return;
- status: ahead, behind, inactive after cap, or active.

### 10.3 Distribution metrics

- percentage of players ahead and behind;
- probability of any profit;
- probability of profit above R50,000;
- probability of first ruin and repeated ruin;
- mean and median P&L;
- 5th, 25th, 75th, and 95th percentiles;
- Gini coefficient or other concentration measure for positive payouts;
- cohort-specific survival curves;
- fraction still profitable at wager-count checkpoints;
- rank persistence across months;
- distribution of outcomes across replication worlds.

### 10.4 Required denominators

Every percentage must expose its denominator. For example:

- `Players ahead: 138 / 1,000 (13.8%)`
- `Bankrupt at least once: 491 / 1,000 (49.1%)`
- `Used all six allocations: 74 / 1,000 (7.4%)`

Do not report percentages that silently exclude inactive or capped players.

---

## 11. Live dashboard specification

The public dashboard should feel data-rich and immediate, but not like a playable gambling interface.

### 11.1 Global casino view

Hero statement:

> 1,000 synthetic players entered with identical R10,000 bankrolls. Watch what happens.

Primary live counters:

```text
TOTAL VIRTUAL WAGERED      R1,842,762,430
TOTAL PAID TO PLAYERS      R1,763,924,811

HOUSE RESULT                  R78,837,619

ACTUAL RTP                       95.72%
THEORETICAL RTP                  95.60%

PLAYERS AHEAD                 138 / 1,000
PLAYERS BEHIND                862 / 1,000

BANKRUPT AT LEAST ONCE       491 / 1,000
USED ALL SIX ALLOCATIONS      74 / 1,000
```

All launch values are generated by the simulation; the numbers above are layout examples only.

Charts:

- cumulative handle, payout, and GGR over time;
- actual versus weighted theoretical RTP with uncertainty bands;
- histogram or density plot of player P&L;
- percentage profitable over time;
- active-player and ruin counts over time;
- game-level handle and result;
- cohort-level median P&L and ruin rate;
- top and bottom player table with lifetime allocation-adjusted P&L.

### 11.2 Player distribution view

Show the complete ordered distribution, not only winners:

```text
P0023    +R597,000
P0744    +R184,200
P0102     +R91,300
...
P0288      -R4,200
...
P0519     -R60,000
```

Controls may filter by cohort, game exposure, bankroll month, status, or wager-count range. Filters must not change the underlying experiment.

### 11.3 Player detail page

Each player page includes:

- policy card and cohort;
- current bankroll and total allocated;
- observed versus expected P&L;
- bankroll line chart with reset markers;
- drawdown chart;
- wagers and turnover by game;
- stake progression;
- session outcomes;
- ruin and allocation timeline;
- current rank in the visible world;
- distribution of the same policy's final P&L across replication worlds;
- plain-language explanation of whether the visible outcome is typical for that policy.

### 11.4 Cohort comparison view

For all ten cohorts, display:

- median and mean P&L;
- interquartile and 5th–95th percentile ranges;
- probability of finishing ahead;
- probability and timing of ruin;
- total turnover;
- allocations used;
- weighted theoretical loss;
- replication-world distribution.

Avoid a simplistic “best strategy” badge. Prefer phrasing such as **lowest median loss in this protocol** or **lowest observed ruin rate**, with uncertainty shown.

### 11.5 Game laboratory view

For every game:

- published rules and paytable;
- theoretical return and house edge by bet type;
- realised return in the visible world;
- wager count and turnover;
- volatility and payout histogram;
- unique players and cohort mix;
- actual-minus-theoretical return over time.

Include a dedicated equal-RTP slot comparison showing that the same expected return can coexist with very different ruin and winner distributions.

### 11.6 Replication worlds view

Show:

- number of completed worlds;
- visible-world percentile among all worlds;
- distribution of final casino result;
- distribution of profitable-player percentages;
- policy-level median, range, and probability of profit;
- rank stability across worlds;
- selected player's outcomes across a sample of universes.

Example:

```text
Player P0023 policy across worlds
World 0001    +R607,000
World 0002     -R41,000
World 0003     -R60,000
World 0004      +R8,400
World 0005     -R29,300
...
Median         -R37,600
```

### 11.7 Methods and audit view

Publish:

- current experiment version;
- configuration hash;
- source-code revision;
- visible-world seed commitment and later reveal policy;
- player manifest hash;
- game rules and validation reports;
- ledger schema;
- known limitations;
- changelog;
- downloadable aggregate data and reproducibility bundle.

---

## 12. Replication worlds

### 12.1 Purpose

A single simulation cannot distinguish a strong policy from a lucky realised path. Replication worlds hold player policies constant while changing the random-number seed.

\[
World_1, World_2, \ldots, World_{10{,}000}
\]

### 12.2 Design

- Reuse the identical player-policy manifest in every world.
- Reuse identical game rules, schedule parameters, and experiment duration.
- Use independent, recorded world seeds.
- Preserve paired player identifiers across worlds.
- Keep the visible public world out of policy tuning and model selection.
- Run an initial minimum of 1,000 worlds; expand toward 10,000 once performance and storage are validated.

### 12.3 Replication outputs

For every player policy:

- mean and median final P&L;
- probability of finishing ahead;
- probability of at least one ruin;
- probability of consuming all allocations;
- 5th–95th and 1st–99th percentile ranges;
- median turnover and wager count;
- rank distribution across worlds.

For every cohort and game:

- distribution of median player outcomes;
- ruin-rate distribution;
- expected versus realised return distribution;
- probability that a visible-world ranking reverses in a new world.

### 12.4 Multiple-comparison protection

With 1,000 players, someone will look exceptional by chance. Therefore:

- do not infer skill from top rank in the visible world;
- treat policy comparisons as paired across worlds;
- report false-discovery-controlled results for broad exploratory comparisons;
- validate any discovered rule on held-out seeds;
- distinguish preregistered hypotheses from post hoc discoveries;
- show shrinkage or uncertainty intervals where policy rankings are displayed.

### 12.5 Visible-world integrity

Before launch:

1. Generate the visible-world seed.
2. Publish a cryptographic commitment to the seed, not the seed itself.
3. Run the live experiment without alteration.
4. Reveal the seed after the primary world closes.
5. Allow independent replay against the immutable ledger and versioned code.

This prevents selective seed choice while preserving the public live experience.

---

## 13. Statistical analysis plan

### 13.1 Primary estimands

- Difference in median final P&L between prespecified cohorts.
- Difference in probability of first ruin by cohort.
- Difference in allocations consumed by cohort.
- Relationship between turnover and net P&L.
- Difference in ruin distribution between equal-RTP, different-volatility slots.
- Difference between visible-world player rank and median rank across worlds.

### 13.2 Methods

- Descriptive distributions rather than averages alone.
- Bootstrap or across-world intervals for medians and quantiles.
- Kaplan–Meier-style time-to-ruin curves, with clear definition of the time scale used.
- Regression of P&L on turnover, game mix, cohort, stake size, and interaction terms.
- Paired world-level comparisons for fixed player policies.
- Rank correlations between early and final outcomes.
- Calibration plots comparing actual and theoretical return by wager-count bands.
- Sensitivity analyses under alternative stake caps, allocation counts, and calendar lengths.

### 13.3 Analysis cautions

- The casino's P&L and players' aggregate P&L are mechanically linked; they are not independent findings.
- Cohort comparisons combine policy decisions with resulting exposure unless exposure is experimentally fixed.
- Stopping rules can reduce exposure without improving the expected value of each wager.
- A policy that loses less is not necessarily profitable.
- Simulation results describe the specified model, not all human gamblers or all commercial casinos.
- Very rare jackpot outcomes may require many more than 10,000 worlds for stable tail estimates.

---

## 14. System architecture

### 14.1 Reference architecture

```text
Versioned experiment configuration
                |
                v
      Simulation orchestrator
                |
        +-------+-------+
        |               |
        v               v
 Behaviour engine    Game engines
        |               |
        +-------+-------+
                |
                v
     Immutable wager event ledger
                |
        +-------+--------+
        |                |
        v                v
 Aggregate pipeline   Replay/validation
        |
        v
 Postgres / analytical store
        |
        v
 Redis or event stream
        |
        v
 Read-only API -> Live web dashboard
```

One practical implementation stack is:

- **Web application:** Next.js with server-rendered methods pages and streamed dashboard updates.
- **Primary database:** PostgreSQL, optionally hosted through Supabase.
- **Simulation workers:** Python processes for game, behaviour, and statistical engines.
- **Event distribution:** Redis streams, a managed queue, or database change feed.
- **Analytical layer:** materialised views plus columnar exports for replication-world summaries.
- **Object storage:** versioned manifests, snapshots, aggregate datasets, and reproducibility bundles.

Equivalent technologies are acceptable if they preserve determinism, auditability, and read-only public access.

### 14.2 Service boundaries

**Experiment registry**

- stores versioned configs, hashes, status, and seed commitments;
- prevents edits to an active experiment;
- links every event to one exact experiment version.

**Simulation orchestrator**

- advances simulated time;
- schedules player sessions;
- assigns work deterministically;
- handles checkpoints and resumable batches.

**Behaviour engine**

- reads player policy and current state;
- proposes game, bet, stake, and session action;
- contains no payout logic.

**Game engine**

- validates the wager;
- draws the outcome from the assigned RNG stream;
- calculates payout and expected value;
- contains no cohort-specific behaviour.

**Ledger service**

- appends wager, allocation, ruin, session, and checkpoint events;
- rejects mutation of settled events;
- supports deterministic replay.

**Aggregation service**

- calculates live counters and chart series;
- reconciles aggregates against ledger totals;
- publishes cacheable snapshots.

**Public API**

- read-only;
- rate-limited;
- exposes aggregates, players, cohorts, games, worlds, methods, and downloads;
- exposes no endpoint that can place or alter a wager.

### 14.3 Scaling model

- Partition wager events by `experiment_id` and simulated date or world.
- Process visible-world events in small ordered batches.
- Process replication worlds in parallel because they are independent.
- Store full wager ledgers for the visible world and validation worlds.
- For large replication counts, retain full ledgers only when required and store signed aggregate outputs plus reproducible seeds for the rest.
- Use idempotent batch identifiers so retries cannot duplicate wagers.

---

## 15. Data model

### 15.1 Core entities

**Experiment**

```text
experiment_id
version
status
start_simulated_at
end_simulated_at
config_hash
code_revision
player_manifest_hash
seed_commitment
created_at
```

**World**

```text
world_id
experiment_id
world_index
seed_reference
is_public_world
status
started_at
completed_at
final_state_hash
```

**Player policy**

```text
player_id
experiment_id
cohort_id
policy_version
policy_parameters_json
game_weights_json
assignment_seed_reference
```

**Player world state**

```text
world_id
player_id
simulated_at
current_bankroll_cents
bankroll_month
allocations_used
cumulative_allocated_cents
cumulative_turnover_cents
cumulative_payout_cents
cumulative_expected_pnl_cents
ruin_count
status
state_version
```

### 15.2 Immutable wager event

```text
bet_id
experiment_id
world_id
sequence_number
player_id
cohort_id
game_id
game_rule_version
simulated_at
session_id
bankroll_month
bankroll_before_cents
stake_cents
choice_json
rng_stream_id
rng_counter_or_draw_reference
outcome_json
gross_payout_cents
net_pnl_cents
bankroll_after_cents
theoretical_ev_cents
policy_state_before_hash
policy_state_after_hash
event_hash
```

### 15.3 Other event types

- `allocation_started`
- `session_started`
- `session_ended`
- `ruin_recorded`
- `allocation_exhausted`
- `player_inactivated`
- `checkpoint_created`
- `world_completed`

### 15.4 Invariants

For every settled wager:

\[
\text{Bankroll After}
=
\text{Bankroll Before}
-
\text{Stake}
+
\text{Gross Payout}
\]

At every aggregate checkpoint:

\[
\text{Casino GGR}
=
-\sum_i \text{Player Net Wager P\&L}_i
\]

after excluding allocation injections from wager P&L.

Other invariants:

- no negative bankroll;
- no stake above bankroll or configured cap;
- no event with an unknown policy or game version;
- monotonically increasing sequence numbers within a world;
- exactly one settlement per accepted wager;
- allocation count never exceeds six in the primary protocol;
- cumulative values equal the sum of immutable events.

---

## 16. Randomness and reproducibility

### 16.1 Deterministic random streams

Use a modern, documented pseudorandom-number generator with deterministic stream derivation. Do not use a single global random stream whose results change when worker concurrency changes.

Derive independent streams from stable identifiers, for example:

\[
seed_{w,p,g,k} = H(seed_w, player_id, game_id, stream_type, k)
\]

Separate streams should cover:

- player-policy assignment;
- session scheduling;
- game selection;
- stake variation;
- each game's outcomes;
- synthetic sports events;
- any adaptive random choice.

Changing dashboard refresh frequency, worker count, or database batching must not change simulation outcomes.

### 16.2 Reproducibility bundle

Publish after the primary run:

- source-code revision or archived source release;
- complete experiment configuration;
- player-policy manifest;
- revealed visible-world seed;
- seed derivation specification;
- game rule and paytable versions;
- database schema;
- aggregate datasets;
- visible-world wager ledger or a privacy-safe compressed equivalent;
- validation tests and expected hashes;
- command or documented procedure to replay the world;
- software environment lock file and container image digest where practical.

### 16.3 Change control

- An active experiment version is immutable.
- Any rule, paytable, cohort, bug fix, or display-definition change creates a new version.
- A simulation bug discovered mid-run is disclosed; the run is either marked invalid or completed under the frozen rules and then rerun as a new version.
- Never silently rewrite prior results.
- Preserve a public changelog and supersession links.

### 16.4 Reconciliation

Automated reconciliation must compare:

- ledger totals with database aggregates;
- player totals with casino totals;
- checkpoint hashes with replayed state;
- realised large-sample return with theoretical return within a preregistered tolerance;
- replication summaries with reproducible reruns of sampled worlds.

---

## 17. Public API and exports

Suggested read-only endpoints:

```text
GET /api/experiments/current
GET /api/experiments/{id}/summary
GET /api/experiments/{id}/timeseries
GET /api/experiments/{id}/players
GET /api/experiments/{id}/players/{player_id}
GET /api/experiments/{id}/cohorts
GET /api/experiments/{id}/games
GET /api/experiments/{id}/worlds/summary
GET /api/experiments/{id}/methods
GET /api/experiments/{id}/downloads
```

Export formats:

- CSV for summary tables;
- Parquet for larger analytical datasets;
- JSON for configurations and manifests;
- Markdown or HTML for methods and data dictionaries;
- checksums for every downloadable artifact.

No public write endpoint may create players, select bets, alter policies, or influence the running world.

---

## 18. Safety and ethical boundaries

### 18.1 Synthetic-only rule

The system must remain:

- zero-deposit;
- zero-withdrawal;
- zero-real-money;
- zero-prize;
- non-transferable;
- read-only for the public.

Virtual balances have no cash value, cannot be purchased, and cannot be redeemed.

### 18.2 No playable casino

The public interface must not include:

- a “bet,” “spin,” “deal,” or “play now” control;
- user-created wagering accounts;
- free credits that imitate personal bankrolls;
- reward sounds, near-miss effects, flashing win celebrations, or variable-ratio engagement mechanics;
- leaderboards that invite visitors to compete;
- personalised predictions or strategies;
- links to gambling operators, affiliates, or bonus offers.

The product is an observatory, not a game.

### 18.3 Responsible presentation

- Keep the synthetic and educational nature visible on every page.
- Present winners together with the full outcome distribution.
- Show total allocated capital, not only current balance.
- Never imply that extreme winners prove a repeatable way to beat negative-expectation games.
- Pair any top-winner profile with its across-world result distribution.
- Use neutral language rather than celebratory casino copy.
- Provide a concise explanation of house edge, volatility, and expected value.
- Include links to locally appropriate gambling-harm support resources on public pages where gambling content is prominent.
- Avoid autoplay audio, urgent countdowns, loss-disguised-as-win effects, or dark patterns.

### 18.4 Audience safeguards

- Do not market the exhibit to minors.
- Avoid child-oriented visuals, mascots, or reward systems.
- Consider a content notice before the live dashboard.
- Ensure accessibility: reduced-motion mode, colour-independent chart encoding, screen-reader labels, and text summaries.

### 18.5 Research ethics

- No real-person behavioural data are required.
- Synthetic personas must not mimic identifiable individuals.
- If future versions collect visitor data or involve human participants, they require a separate privacy, consent, and ethics protocol.
- Do not make diagnostic claims about gambling disorder from synthetic agents.
- Clearly separate model assumptions from empirical evidence about human behaviour.

### 18.6 Security boundaries

- Public infrastructure is read-only.
- Administrative controls require strong authentication and audit logs.
- Seeds for active visible worlds are protected until scheduled reveal.
- Rate-limit public APIs and cap export sizes.
- Validate all configuration and event inputs.
- Keep simulation workers isolated from public request paths.
- Back up manifests, ledgers, checkpoints, and hashes.

---

## 19. Limitations

The experiment must publish these limitations prominently:

1. Synthetic agents are simplified behavioural models, not people.
2. Results depend on the chosen policies, game rules, stake limits, and time horizon.
3. A six-month simulation does not represent a universal human gambling trajectory.
4. Replenishing bankrolls is an experimental device, not a claim about real income cycles.
5. “Bankroll month” is an allocation episode and is distinct from calendar month.
6. Expected value can be calculated exactly for many games, but behavioural attribution is more model-dependent.
7. A visible extreme winner can occur in a valid negative-expectation system.
8. Replication reduces overinterpretation but does not make the synthetic behaviour empirically true.
9. Rare jackpots may be poorly estimated even with thousands of worlds.
10. The platform demonstrates mathematical and modelled behavioural mechanisms; it does not estimate the prevalence of gambling harm in a real population.

---

## 20. Quality assurance and acceptance criteria

### 20.1 Engine correctness

- All ten games pass exact rule and payout tests.
- Large-sample simulations converge to the implemented theoretical returns within preregistered tolerances.
- The same config and seed reproduce identical event hashes regardless of worker count.
- Invalid wagers cannot enter the ledger.
- Bankroll arithmetic is exact in integer cents.
- Reset events and the six-allocation cap behave correctly at boundary conditions.

### 20.2 Data integrity

- Every accepted wager has exactly one settlement.
- Aggregate casino GGR reconciles to aggregate player wager P&L.
- Allocation injections never appear as winnings.
- Current bankroll plus cumulative net flows reconcile for every player.
- Daily and monthly checkpoint hashes replay successfully.

### 20.3 Dashboard correctness

- All percentages display denominators.
- Player rankings use lifetime allocation-adjusted P&L.
- Actual and theoretical RTP are labelled distinctly.
- Example or placeholder numbers cannot appear as live data.
- Dashboard timestamps identify simulated time and processing freshness.
- Filters preserve totals and do not silently exclude capped players.

### 20.4 Reproducibility

- An independent clean environment can replay a sampled world from published inputs.
- Replayed final-state and ledger hashes match.
- A sample of replication-world summaries can be regenerated from their seeds.
- The methods page identifies the exact code and configuration version.

### 20.5 Safety

- No path accepts payment or creates redeemable value.
- No public interaction can influence a wager.
- No gambling affiliate or operator promotion is present.
- Winner displays include context and replication-world outcomes.
- The site passes an accessibility review and supports reduced motion.

---

## 21. Delivery phases

### Phase 1 — Protocol and mathematics

- Freeze definitions, cohort ranges, bankroll logic, and hypotheses.
- Implement and independently validate all game engines.
- Create the player-policy generator and manifest format.
- Produce a preregistration-style analysis plan.

### Phase 2 — Deterministic simulation core

- Implement world orchestration and separated RNG streams.
- Add bankroll, session, ruin, and reset state machines.
- Build the immutable event ledger and deterministic replay.
- Run small-world correctness and performance tests.

### Phase 3 — Visible-world dashboard

- Build global, distribution, player, cohort, game, methods, and safety views.
- Add real-time aggregates and checkpoint status.
- Conduct accessibility and responsible-design reviews.

### Phase 4 — Replication laboratory

- Run 1,000 validation worlds.
- Add paired policy summaries and held-out-seed analysis.
- Scale toward 10,000 worlds after storage and compute checks.
- Publish replication uncertainty on player and cohort pages.

### Phase 5 — Public launch and audit

- Publish the seed commitment and frozen protocol.
- Start the live visible world.
- Monitor reconciliation, not outcomes.
- Reveal the seed after completion.
- Release the reproducibility bundle and final report.

---

## 22. Minimum viable release

The minimum credible public release includes:

- all 1,000 player policies;
- all ten games;
- exact R10,000 reset logic and six-allocation cap;
- immutable visible-world wager ledger;
- global dashboard, cohort comparison, and player pages;
- actual versus theoretical return;
- expected versus observed player P&L;
- at least 1,000 replication worlds;
- public methods, limitations, safety statement, and data dictionary;
- seed commitment before launch and seed reveal after completion;
- downloadable configuration and aggregate results.

A prototype that lacks replication, clear allocation-adjusted P&L, or reproducibility should not be presented as the completed GreyScienx experiment.

---

## 23. Example public interpretation

The central public lesson is not that every gambler loses in every period. The simulation should make a subtler fact visible:

> A negative-expectation system can produce striking individual winners while the aggregate distribution continues to favour the house.

In one visible world, Player P0023 might turn R10,000 into R607,000. That observation is real within the simulation, but it is incomplete. The player's wager-specific expected result may still be negative, and the identical policy may lose in most replication worlds.

Likewise, a player who loses faster than expected is not proof that the game is unfair. Short-run outcomes vary around expectation, especially in high-volatility games.

The experiment therefore keeps three views together:

1. **The casino aggregate:** Does realised return converge toward the implemented mathematics?
2. **The player distribution:** How unequal and volatile are individual experiences?
3. **The replication distribution:** Does a seemingly successful policy remain successful under new random paths?

---

## 24. Final GreyScienx framing

The Virtual Casino should be presented as a live, inspectable statistical economy:

- the rules are public;
- the players are synthetic;
- the money is fictional;
- the policies are frozen;
- every wager is auditable;
- the random paths are reproducible;
- the visible winner is compared with thousands of alternate worlds;
- and the public sees the entire distribution rather than a curated success story.

GreyScienx does not need to tell viewers merely that “the house always wins.” It can show how house advantage emerges in aggregate, why some players remain ahead for surprisingly long periods, how volatility creates dramatic exceptions, and why a lucky realised path is not the same thing as a repeatable edge.

> **GreyScienx principle:** expose the assumptions, simulate them transparently, preserve the full distribution, and let the numbers accumulate in public.

