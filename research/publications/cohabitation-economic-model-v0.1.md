# Cohabitation Economic Model (CEM), version 0.1

## Research question

What are the microeconomic and macroeconomic effects when two adults who would otherwise maintain separate one-person households consolidate into one two-adult household?

This version models cohabitation as a household-production and resource-sharing arrangement. Romantic utility may be added later, but it is set to zero here so that it does not mechanically manufacture an economic benefit.

## 1. Units, states, and timing

Individuals are indexed by \(i\in\{A,B\}\), expenditure categories by \(k\), and periods by \(t\).

The household state is

\[
z_t\in\{S,C\},
\]

where \(S\) means that A and B live in separate one-person households and \(C\) means that they cohabit.

The clean baseline comparison holds constant:

- the same two adults;
- their wages and employment states in the first period;
- the prices they face;
- the quality of consumption services, unless a quality adjustment is explicitly introduced;
- no children or additional household members;
- no intrinsic romantic or companionship benefit.

These restrictions are relaxed in later layers of the model.

## 2. Consumption technology and the direct cohabitation dividend

Let \(e_k=p_k q_k\) be the expenditure required for one person living alone to obtain a reference quantity and quality of service in category \(k\).

For two separate households:

\[
E_k^S=2e_k.
\]

For a two-person cohabiting household:

\[
E_k^C=e_k\,2^{\theta_k}\chi_k,
\qquad 0\leq\theta_k\leq1.
\]

The parameters have distinct meanings:

- \(\theta_k=0\): the category is a pure household public good; one unit serves both adults.
- \(\theta_k=1\): the category is fully private or rival; two adults cost twice as much as one.
- \(0<\theta_k<1\): partial sharing or economies of scale.
- \(\chi_k\): quality and behavioural adjustment after moving together. A larger dwelling, more meals out, or better internet can make \(\chi_k>1\); economising can make \(\chi_k<1\).

The category-level direct dividend is

\[
D_k=E_k^S-E_k^C
=e_k\left(2-2^{\theta_k}\chi_k\right).
\]

Sharing generates a positive saving in category \(k\) exactly when

\[
\chi_k<2^{1-\theta_k}.
\]

The gross direct cohabitation dividend is

\[
D^{\text{direct}}=\sum_k D_k.
\]

For equal quality, \(\chi_k=1\), the proportional saving relative to the cost of two separate households is

\[
s_k=\frac{2-2^{\theta_k}}{2}=1-2^{\theta_k-1}.
\]

| Scale exponent \(\theta_k\) | Interpretation | Implied saving |
|---:|---|---:|
| 0.0 | Purely shared | 50.0% |
| 0.3 | Strong sharing | 38.4% |
| 0.5 | Square-root scaling | 29.3% |
| 0.7 | Moderate sharing | 18.8% |
| 1.0 | Fully private | 0.0% |

The table contains model implications, not empirical estimates.

### Useful category decomposition

The model should estimate a different \(\theta_k\) for each category:

\[
k\in\{\text{housing, utility base charges, utility usage, internet, food, transport, durables, insurance, private goods}\}.
\]

Housing, internet, appliances, and utility connection charges should normally have lower scale exponents than clothing, personal care, individual transport, or other private consumption. These signs should be tested rather than imposed during estimation.

## 3. Disposable income and the fiscal-status wedge

Let gross income be

\[
Y_t^g=w_{At}n_{At}+w_{Bt}n_{Bt}+y_t^{\text{other}},
\]

where \(w_i\) is the wage and \(n_i\) paid work. Returns on the beginning-of-period asset stock enter the intertemporal budget below, rather than being counted twice as flow income.

Disposable income in household state \(z\) is

\[
Y_t^d(z)=Y_t^g-T_t(z)+B_t(z),
\]

where \(T\) denotes taxes and mandatory contributions and \(B\) denotes grants, rebates, or other transfers.

The fiscal-status wedge created by consolidation is

\[
\Omega_t=
Y_t^d(C)-\left[Y_{At}^d(S)+Y_{Bt}^d(S)\right].
\]

It can be positive or negative. A means test based on combined resources can make \(\Omega<0\); a household rebate or tax advantage can make it positive. No sign is assumed.

The first-period cash dividend is therefore

\[
D_t^{\text{cash}}=D_t^{\text{direct}}+\Omega_t-M_t,
\]

where \(M_t\) contains moving, deposits, furnishing, contract cancellation, and other transition costs.

## 4. Household budget and wealth accumulation

Let \(a_t\) be combined net financial wealth at the beginning of period \(t\). The cohabiting household budget evolves as

\[
a_{t+1}=(1+r_t)a_t+Y_t^d(C)-E_t^C-c_{At}-c_{Bt}-M_t,
\]

where \(E_t^C\) contains household-level expenditure and \(c_i\) contains individually assigned consumption not already included in \(E^C\).

The borrowing constraint is

\[
a_{t+1}\geq-\bar b_C(Y_A,Y_B,\text{collateral}).
\]

Two incomes or combined collateral may relax the constraint, so \(\bar b_C\) may exceed the sum of individual borrowing limits. It could also fall if one partner has poor credit or pre-existing debt.

The direct dividend is allocated as

\[
D^{\text{cash}}
=D_C+D_S+D_B,
\]

where the components are additional consumption, saving/investment, and debt repayment. Define shares

\[
\lambda_C+\lambda_S+\lambda_B=1,
\qquad \lambda_j\in[0,1].
\]

The household's financial outcome depends as much on these allocation shares as on the size of the gross dividend.

## 5. Income risk pooling

Let income shocks have variances \(\sigma_A^2,\sigma_B^2\) and correlation \(\rho_{AB}\). Combined income variance is

\[
\operatorname{Var}(Y_A+Y_B)
=\sigma_A^2+\sigma_B^2+2\rho_{AB}\sigma_A\sigma_B.
\]

For equal income variances, \(\sigma_A=\sigma_B=\sigma\), the variance of average income per adult is

\[
\operatorname{Var}\!\left(\frac{Y_A+Y_B}{2}\right)
=\frac{\sigma^2}{2}(1+\rho_{AB}).
\]

Its standard deviation relative to the standard deviation of one person's income is

\[
R_\sigma=\sqrt{\frac{1+\rho_{AB}}{2}}.
\]

When shocks are independent, \(R_\sigma=0.707\). When \(\rho=0.3\), \(R_\sigma=0.806\). When both partners face the identical shock, \(\rho=1\), there is no diversification gain.

With CRRA utility,

\[
u(c)=\frac{c^{1-\gamma}-1}{1-\gamma},
\]

define each person's certainty-equivalent consumption as

\[
CE_i(z)=u^{-1}\left(\mathbb E[u(c_i(z))]\right).
\]

The monetised insurance dividend is

\[
D^{\text{risk}}=\sum_i\left[CE_i(C)-CE_i(S)\right].
\]

This captures the value of smoother consumption, not merely average income.

## 6. Time allocation and household production

Each adult has a time constraint

\[
1=n_i+\tau_i+\ell_i,
\]

where \(n_i\) is paid work, \(\tau_i\) unpaid household work, and \(\ell_i\) leisure.

Household services are produced by

\[
G=A_G\left[a_A\tau_A^{\rho_G}+a_B\tau_B^{\rho_G}\right]^{\gamma_G/\rho_G}K_G^{\delta_G},
\]

where \(a_i\) is household-task productivity, \(K_G\) household capital such as appliances, and the curvature parameters determine substitutability and returns to household work.

The time dividend can arise from shared fixed tasks, specialisation, and shared household capital. Value unpaid time at an explicit shadow wage \(v_i\):

\[
D^{\text{time}}
=\sum_i v_i\left(\tau_i^S-\tau_i^C\right)
+V(G^C-G^S).
\]

A household-level time saving is not enough to establish equal individual benefit. Report

\[
\Delta\tau_A,\quad \Delta\tau_B,
\quad\text{and}\quad
\frac{\tau_A}{\tau_A+\tau_B}
\]

separately.

## 7. Preferences, privacy, crowding, and bargaining

A parsimonious period utility function is

\[
u_i=
\alpha_i\ln c_i
+\beta_i\ln h_i
+\gamma_i\ln G
+\eta_i\ln\ell_i
-\psi_i\,\text{Crowding}
-\phi_i\,\text{Conflict}
-\zeta_i\,\text{Dependency}.
\]

These last three terms prevent the model from assuming that resource sharing is free. A suitable crowding measure is

\[
\text{Crowding}=\frac{N_{\text{persons}}}{N_{\text{rooms}}}
\]

or persons per bedroom.

The cohabiting household is modelled as a collective household rather than a single utility-maximising person:

\[
\max_{\mathcal A}
\mu U_A(\mathcal A)+(1-\mu)U_B(\mathcal A),
\qquad 0\leq\mu\leq1,
\]

subject to the household budget, time constraints, and participation constraints

\[
U_i(C)\geq \bar U_i(S),\qquad i\in\{A,B\}.
\]

The Pareto weight \(\mu\) is determined by bargaining power: income, individually owned assets, legal rights, access to accounts, unpaid work, and the credibility of leaving. An alternative empirical implementation uses the Nash product

\[
\max_{\mathcal A}
\left(U_A-\bar U_A\right)^\omega
\left(U_B-\bar U_B\right)^{1-\omega}.
\]

Total surplus being positive is necessary but not sufficient for stable cohabitation. Both participation constraints must hold. This is the mathematical reason a household can appear richer while one member becomes worse off.

## 8. Separation risk and relationship duration

Let \(\delta\) be the per-period probability of dissolution, \(K^{\text{exit}}\) the cost paid upon dissolution, \(M_0\) the initial setup cost, \(\beta\) the discount factor, and \(\pi\) the constant per-period net surplus while cohabiting.

The expected net present value is

\[
NPV_C
=-M_0+
\frac{\pi-\beta\delta K^{\text{exit}}}
{1-\beta(1-\delta)}.
\]

The per-period net surplus is

\[
\pi=
D^{\text{direct}}
+\Omega
+D^{\text{risk}}
+D^{\text{time}}
+D^{\text{capital}}
-D^{\text{crowding}}
-D^{\text{conflict}}
-D^{\text{dependency}}.
\]

The pair consolidates only if the expected allocation makes both people at least as well off as their outside options. Higher moving costs, weaker legal protection, and higher dissolution risk reduce the attractiveness of consolidation even when monthly expenses fall.

## 9. Labour-supply effects

The first-order condition for paid work is schematically

\[
u_{c_i}(1-\tau_i^{m})w_i=u_{\ell_i},
\]

where \(\tau_i^{m}\) is the marginal tax or benefit-withdrawal rate.

Cohabitation changes this condition through:

- lower required expenditure;
- spousal insurance and non-labour resources;
- altered marginal taxes or benefit withdrawal;
- changed unpaid-work obligations;
- relocation and commuting costs;
- the ability to study, search longer for a job, or start a business.

The aggregate sign is deliberately unrestricted:

\[
\Delta n_A+\Delta n_B\gtreqless0.
\]

It must be estimated rather than assumed.

## 10. From two households to the macroeconomy

Let

- \(S_t\) be the number of one-person households;
- \(P_t\) be the number of cohabiting two-adult households;
- \(H_t^O\) be other households;
- \(X_t\) be the number of new consolidations, each formed from two one-person households.

Then

\[
S_{t+1}=S_t-2X_t,
\qquad
P_{t+1}=P_t+X_t,
\]

and total household count changes by

\[
H_{t+1}=H_t-X_t.
\]

If a fraction \(\varphi\) of residents in one-person households pair with one another,

\[
X=\frac{\varphi S}{2}.
\]

The aggregate direct dividend is

\[
\mathcal D=X\,\bar D^{\text{direct}},
\]

where \(\bar D\) is the average dividend per consolidating pair. Heterogeneous versions integrate over income, region, dwelling type, and match characteristics.

## 11. Housing market

Let \(h_1\) be housing services demanded by one single household and \(h_2\) services demanded by one cohabiting pair. The direct demand change from \(X\) consolidations is

\[
\Delta Q_H=X(h_2-2h_1).
\]

If \(h_2<2h_1\), consolidation lowers aggregate housing demand even when the couple chooses a larger dwelling than either individual previously occupied.

For a proportional demand shift \(\Delta\ln D_H\), a local approximation to the rent or house-price response is

\[
\Delta\ln P_H
\approx
\frac{\Delta\ln D_H}
{\varepsilon_S+|\varepsilon_D|},
\]

where \(\varepsilon_S\) and \(\varepsilon_D\) are housing supply and demand elasticities. The effect should be strongest where supply is inelastic.

Housing stock evolves according to

\[
K_{H,t+1}=(1-\delta_H)K_{H,t}+I_{H,t}.
\]

Short-run adjustment occurs through vacancies, rents, crowding, and unit choice; long-run adjustment also occurs through lower construction, conversion, and demolition.

## 12. Aggregate consumption, saving, and GDP

For each rand of direct expenditure released, let \(\lambda_C\) be respent on other current consumption, \(\lambda_S\) saved, and \(\lambda_B\) used to repay debt.

Ignoring price changes, the first-round change in total consumption expenditure is

\[
\Delta C=-\mathcal D+\lambda_C\mathcal D
=-(\lambda_S+\lambda_B)\mathcal D.
\]

Even when \(\lambda_C=1\), the composition of consumption changes away from duplicated housing and household goods.

A deliberately transparent partial-equilibrium GDP decomposition is

\[
\Delta Y
=\Delta C_{\text{domestic}}
+\Delta I_H
+\kappa_S\lambda_S\mathcal D
+\Delta G
+\Delta NX,
\]

where \(\kappa_S\) is the fraction of additional saving that becomes incremental domestic investment within the selected horizon and \(\Delta I_H\) is the change in residential investment. This is a scenario identity, not a claim that saving automatically creates investment one-for-one.

The central measurement result is

\[
\Delta W>0
\quad\text{can coexist with}\quad
\Delta C<0
\quad\text{and}\quad
\Delta GDP<0.
\]

GDP records market production. It does not fully record consumer surplus, shared consumption services, avoided duplication, unpaid household production, privacy, or bargaining outcomes.

## 13. Industry effects

For industry \(j\), define an exposure coefficient \(a_j\) to household formation and an induced-spending coefficient \(b_j\). Its first-round revenue effect is

\[
\Delta R_j=-a_j\mathcal D+b_j\lambda_C\mathcal D.
\]

Likely negative-exposure industries include small-unit rentals, duplicated appliances, furniture, utility connections, and individual household subscriptions. Potential positive-exposure industries include larger dwellings, leisure, restaurants, education, financial products, and childcare. The coefficients, not the verbal categories, determine the result.

Input-output multipliers can later map \(\Delta R_j\) into domestic output, imports, wages, and employment.

## 14. Energy, materials, and emissions

Let household energy or material use scale as

\[
E(n)=E_1n^{\theta_E}\chi_E.
\]

The direct environmental change from \(X\) consolidations is

\[
\Delta E=X\left[E(2)-2E(1)\right].
\]

Operational emissions are

\[
CO_2^{\text{oper}}
=g_eE_{\text{electricity}}
+g_fE_{\text{fuel}},
\]

where \(g_e\) and \(g_f\) are emissions intensities. Total effects should add avoided embodied emissions from dwellings, appliances, and furniture, then subtract emissions produced by respending the dividend:

\[
\Delta CO_2^{\text{total}}
=\Delta CO_2^{\text{oper}}
+\Delta CO_2^{\text{embodied}}
+\Delta CO_2^{\text{respending}}.
\]

The last term prevents the model from treating monetary savings as if they disappear environmentally.

## 15. Government and municipal accounts

Define net public revenue from household state \(z\) as

\[
R_G(z)=T(z)-B(z)+F(z)-SC(z),
\]

where \(F\) is fixed service-charge revenue and \(SC\) is the public cost of delivering services.

The direct fiscal effect of \(X\) consolidations is

\[
\Delta R_G
=X\left[R_G(C)-R_G(S_A)-R_G(S_B)\right].
\]

Fewer connections may reduce service costs but also reduce fixed municipal charges. Combined means tests may reduce benefits while simultaneously hiding deprivation of a low-resource partner. These effects must be reported separately from national GDP.

## 16. Distribution and poverty measurement

An equivalised-income summary is

\[
Y^{eq}=\frac{Y^d}{n^{\bar\theta}},
\]

where \(\bar\theta\) is a summary scale parameter. This is useful for comparing households but cannot reveal who controls resources.

Report at least four individual outcomes:

\[
c_A,\quad c_B,\quad \ell_A,\quad \ell_B,
\]

plus individual asset ownership, unpaid work, and the utility change relative to living separately. Household-level poverty and individual economic autonomy are different outcomes.

## 17. Cohabitation choice and selection

The probability of consolidation is endogenous:

\[
\Pr(C_{AB}=1)
=\Lambda\left(
\alpha
+\beta_1\widehat{NPV}_{AB}
+\beta_2\text{Compatibility}_{AB}
+\beta_3\frac{Rent}{Income}
+\beta_4\text{EmploymentRisk}
+\beta_5\text{Norms}
+\beta_6\text{HousingAvailability}
\right).
\]

Observed cohabitants therefore cannot simply be compared with observed singles. They differ in expected match quality, income, preferences, age, location, and willingness to share.

A panel event-study specification for outcome \(y_{it}\) is

\[
y_{it}=\alpha_i+\lambda_t+
\sum_{k\neq-1}\beta_k
\mathbf 1[t-T_i=k]
+X_{it}'\gamma+\varepsilon_{it},
\]

where \(T_i\) is the move-in date. Leads test for anticipation and pre-trends; lags trace adjustment. A companion event study around separation tests whether gains reverse and measures exit costs.

The causal estimand should be stated explicitly, for example

\[
ATT_y=\mathbb E[y_i(C)-y_i(S)\mid C_i=1],
\]

the effect for people who actually consolidate, rather than for an imaginary random pair of adults.

## 18. Baseline illustrative household

This accounting example is not a South African estimate.

| Monthly item | Separate households | Cohabiting household | Direct dividend |
|---|---:|---:|---:|
| Housing | R16,000 | R12,000 | R4,000 |
| Utilities and internet | R4,600 | R3,100 | R1,500 |
| Food | R8,000 | R7,000 | R1,000 |
| Transport | R6,000 | R6,000 | R0 |
| Private consumption | R10,000 | R10,000 | R0 |
| **Total** | **R44,600** | **R38,100** | **R6,500** |

With combined after-tax income of R60,000, saving rises mechanically from R15,400 to R21,900 if none of the dividend is respent. The model must then subtract transition costs, the fiscal wedge, crowding, unequal unpaid work, dependency, and expected separation cost before calling this a net welfare gain.

## 19. Illustrative South African scale calculation

Statistics South Africa reported approximately 19.005 million households in 2023, of which 26.5% were one-person households. This implies mechanically

\[
S\approx19.005\text{m}\times0.265=5.036\text{m}.
\]

If, purely as a scenario, 10% of those one-person households formed pairs with one another,

\[
X=\frac{0.10\times5.036\text{m}}{2}
\approx251,800
\]

consolidations would occur and household count would fall by the same number.

At the illustrative dividend of R6,500 per pair per month, the annual direct expenditure released would be

\[
\mathcal D
=251{,}800\times R6{,}500\times12
\approx R19.6\text{ billion}.
\]

This is not a forecast. It assumes that eligible people can be paired, ignores selection and general-equilibrium price changes, and transfers a hypothetical expenditure profile to the entire group. Its purpose is to show how the micro model aggregates.

## 20. Assumption register

Every simulation should disclose the following assumptions:

| ID | Assumption or parameter | Baseline treatment |
|---|---|---|
| A1 | Relevant population | Two adults currently living alone |
| A2 | Children | Excluded initially |
| A3 | Income | Fixed in period 1; endogenous later |
| A4 | Prices | Fixed in micro model; endogenous in macro model |
| A5 | Consumption quality | Explicit \(\chi_k\), never silently held constant |
| A6 | Sharing technology | Category-specific \(\theta_k\) |
| A7 | Income-shock dependence | Explicit \(\rho_{AB}\) |
| A8 | Unpaid work | Valued at explicit shadow wages |
| A9 | Bargaining | Collective model with individual participation constraints |
| A10 | Transfers within household | Not presumed equal or frictionless |
| A11 | Dissolution | Hazard \(\delta\) and exit cost \(K^{exit}\) |
| A12 | Fiscal treatment | Explicit taxes, benefits, and withdrawal rates |
| A13 | Housing response | Short- and long-run supply elasticities |
| A14 | Use of dividend | \(\lambda_C,\lambda_S,\lambda_B\) |
| A15 | Domestic content | Industry-specific import shares |
| A16 | Environmental rebound | Emissions from respending included |
| A17 | Romantic utility | Zero in economic baseline |
| A18 | Selection into cohabitation | Explicitly modelled; no naive causal comparison |

## 21. Primary outputs

For each household type and macro scenario, the model should produce:

1. Gross and net monthly cohabitation dividend.
2. Dividend by expenditure category.
3. Individual equivalent variation for A and B.
4. Saving, debt, and wealth paths.
5. Consumption volatility and hardship probability.
6. Paid work, unpaid work, and leisure by individual.
7. Expected NPV after setup and separation risk.
8. Housing units, rents, vacancies, and construction.
9. Consumption shifts by industry.
10. GDP range under alternative respending and investment assumptions.
11. Government and municipal budget effects.
12. Energy, material, and emissions effects including rebound.
13. Distributional results by income, gender, location, and tenure.

## 22. Testable hypotheses

- **H1:** \(D^{direct}>0\) on average, with housing providing the largest component.
- **H2:** The proportional dividend varies nonlinearly with income because fixed-cost burdens and the ability to share both change with living standards.
- **H3:** Cohabitation reduces consumption volatility when partners' income shocks are imperfectly correlated.
- **H4:** Liquid saving and debt repayment rise after consolidation, conditional on income and pre-trends.
- **H5:** Household-level gains are distributed unequally when bargaining power and unpaid work are unequal.
- **H6:** More consolidation reduces demand for separate small dwellings and duplicated durable goods.
- **H7:** Welfare can rise while current consumption and measured GDP fall.
- **H8:** Residential energy and materials per person fall, but environmental rebound offsets part of the direct saving.
- **H9:** Labour-supply effects are heterogeneous and have no theoretically predetermined aggregate sign.
- **H10:** Separation reverses part of the dividend and creates a discrete housing, liquidity, and transaction-cost shock.

## 23. Calibration sequence

The model should be built in four passes:

1. **Accounting model:** estimate \(e_k,\theta_k,\chi_k,M\), and the monthly direct dividend.
2. **Dynamic household model:** add income shocks, assets, borrowing, labour supply, time use, bargaining, and dissolution.
3. **Partial-equilibrium macro model:** aggregate housing, consumption, public-finance, and environmental effects while holding prices or elasticities explicit.
4. **General-equilibrium extension:** add industry input-output linkages, price changes, residential construction, labour demand, investment, and fiscal feedback.

The first empirical deliverable should be a distribution—not a single mean—of the South African direct dividend:

\[
F\!\left(D^{direct}\mid
\text{income, province, tenure, dwelling type, employment, household composition}
\right).
\]

## References used to motivate the structure

- Statistics South Africa, [General Household Survey 2024](https://www.statssa.gov.za/publications/P0318/P03182024.pdf).
- Statistics South Africa, [The state of South African households in 2023](https://www.statssa.gov.za/?p=17283).
- van Leeuwen et al., [Household Composition and Preferences: A Collective Approach to Household Consumption](https://onlinelibrary.wiley.com/doi/10.1111/roiw.12483).
- De Nardi, Fella, and Paz-Pardo, [Wage Risk and Government and Spousal Insurance](https://www.nber.org/papers/w28294).
- Lee and Painter, [What Happens to Household Formation in a Recession?](https://www.sciencedirect.com/science/article/pii/S0094119013000284).
- Underwood and Zahran, [The Carbon Implications of Declining Household Scale Economies](https://www.sciencedirect.com/science/article/pii/S092180091500213X).
- World Bank, [Poverty Measurement and Analysis](https://documents1.worldbank.org/curated/en/156931468138883186/pdf/2980000182131497813.pdf).
