# Insurance Segment-to-Data Map

Reference for the `insurance-market-case` skill. Each row maps an insurance
industry segment to tickers, news keywords, chart type, and historical
parallels. Use this to pick the right data and framing once a news event is
found — segments are picked by matching the event to a row, not chosen ahead
of time (there's no "week" schedule here, unlike a course-topic skill).

---

## Property & Casualty (P&C)

| Field | Value |
|-------|-------|
| **Slug** | `property_casualty` |
| **Tickers** | `TRV` (Travelers), `ALL` (Allstate), `PGR` (Progressive), `CB` (Chubb), `KIE` (SPDR S&P Insurance ETF) |
| **News keywords** | homeowners insurance, property insurance, catastrophe losses, combined ratio, underwriting loss, rate filing, non-renewal, insurer of last resort |
| **Chart type** | Multi-line: insurer stocks + KIE benchmark, normalized to 100 over 3 months |
| **Historical parallels** | Hurricane Katrina (2005), Hurricane Ian (2022), California wildfires (2025) |
| **Key metrics to track** | Combined ratio, catastrophe loss estimates, rate filing approvals/denials |

## Life Insurance

| Field | Value |
|-------|-------|
| **Slug** | `life_insurance` |
| **Tickers** | `MET` (MetLife), `PRU` (Prudential Financial), `LNC` (Lincoln National), `UNM` (Unum), `KIE` (benchmark) |
| **News keywords** | life insurance, mortality, annuities, longevity risk, life settlement, insurance reserves, actuarial |
| **Chart type** | Multi-line: insurer stocks + KIE, normalized to 100 over 3 months |
| **Historical parallels** | 2008 GFC (AIG bailout, capital markets stress on annuity books), COVID-19 mortality spike (2020-21) |
| **Key metrics to track** | Mortality experience vs. pricing assumptions, interest-rate sensitivity of annuity reserves |

## Health Insurance

| Field | Value |
|-------|-------|
| **Slug** | `health_insurance` |
| **Tickers** | `UNH` (UnitedHealth), `CI` (Cigna), `HUM` (Humana), `ELV` (Elevance Health), `CVS` (CVS Health/Aetna) |
| **News keywords** | health insurance, medical loss ratio, ACA, Medicare Advantage, prior authorization, premium increase, utilization rate |
| **Chart type** | Multi-line: payer stocks, normalized to 100 over 3 months |
| **Historical parallels** | ACA passage and rollout (2010-14), COVID-19 utilization swings (2020 low, 2022+ elevated) |
| **Key metrics to track** | Medical loss ratio (MLR), Medicare Advantage enrollment/reimbursement changes |

## Reinsurance

| Field | Value |
|-------|-------|
| **Slug** | `reinsurance` |
| **Tickers** | `EG` (Everest Group), `RGA` (Reinsurance Group of America), `RNR` (RenaissanceRe), `SPNT` (SiriusPoint), `KIE` (benchmark) |
| **News keywords** | reinsurance rates, treaty renewal, retrocession, catastrophe bond, alternative capital, hard market, soft market, January renewals, June/July renewals |
| **Chart type** | Multi-line: reinsurer stocks + KIE, normalized to 100 over 3 months |
| **Historical parallels** | 2017 hurricane season (Harvey/Irma/Maria) hardened the reinsurance market for years; 2022-23 hard market after Hurricane Ian |
| **Key metrics to track** | Renewal rate changes at Jan 1 / mid-year treaty dates, retention levels, alternative capital (ILS) inflows |

## Cyber Insurance

| Field | Value |
|-------|-------|
| **Slug** | `cyber_insurance` |
| **Tickers** | No pure-play public insurer; use `CIBR` (cybersecurity ETF) as a sentiment proxy, plus `KIE` for the broader industry |
| **News keywords** | cyber insurance, ransomware, data breach, cyber policy, silent cyber, systemic cyber risk, war exclusion clause |
| **Chart type** | Line: CIBR vs KIE, normalized to 100 over 3 months (proxy only — note in the report that no direct pure-play ticker exists) |
| **Historical parallels** | NotPetya (2017, "silent cyber" wake-up call), Colonial Pipeline (2021), MOVEit breach (2023) |
| **Key metrics to track** | Reported ransomware claim frequency/severity trends (qualitative — no clean public data series) |

## Catastrophe & Climate Risk

| Field | Value |
|-------|-------|
| **Slug** | `catastrophe_climate` |
| **Tickers** | `KIE`, plus the P&C/reinsurance names above as a proxy (no free, reliable public cat-bond index ticker) |
| **News keywords** | catastrophe bond, insurance-linked securities, climate risk, wildfire risk, flood insurance, FAIR Plan, insurer of last resort, market exit, non-renewal wave |
| **Chart type** | Multi-line: P&C + reinsurance names, normalized to 100, annotated at the event date |
| **Historical parallels** | California FAIR Plan crisis (2023-24), Florida property insurance market crisis (2022-23) |
| **Key metrics to track** | State residual-market (FAIR Plan / Citizens) policy count growth, insurer market-exit announcements |

## InsurTech / Digital Insurance

| Field | Value |
|-------|-------|
| **Slug** | `insurtech` |
| **Tickers** | `LMND` (Lemonade), `ROOT` (Root Inc), `GSHD` (Goosehead Insurance) |
| **News keywords** | insurtech, digital insurance, AI underwriting, embedded insurance, direct-to-consumer insurance, loss ratio improvement, InsurTech funding |
| **Chart type** | Multi-line: insurtech names, normalized to 100 over 3 months |
| **Historical parallels** | Lemonade IPO (2020), Root/Metromile underwriting struggles (2021-22) |
| **Key metrics to track** | Gross loss ratio trend, policy growth vs. underwriting profitability |

## Auto Insurance

| Field | Value |
|-------|-------|
| **Slug** | `auto_insurance` |
| **Tickers** | `PGR` (Progressive), `ALL` (Allstate), `KIE` (benchmark) — Berkshire's GEICO is not separately listed |
| **News keywords** | auto insurance, telematics, claims severity, repair cost inflation, total loss frequency, usage-based insurance, rate increase filing |
| **Chart type** | Multi-line: auto insurer stocks + KIE, normalized to 100 over 3 months |
| **Historical parallels** | Telematics/usage-based pricing rise (2010s), post-COVID claims severity inflation (2022) |
| **Key metrics to track** | Claims frequency vs. severity trend, approved rate increases by state |

## Insurance Regulation & M&A

| Field | Value |
|-------|-------|
| **Slug** | `regulation_ma` |
| **Tickers** | `KIE`, plus the specific companies named in the deal/regulatory action |
| **News keywords** | insurance regulation, NAIC, state insurance commissioner, insurance M&A, merger review, antitrust, rate approval, solvency requirement |
| **Chart type** | Line: acquirer/target stocks around the announcement date, plus KIE for sector context |
| **Historical parallels** | Aon/Willis Towers Watson attempted merger (2020-21, blocked on antitrust grounds) |
| **Key metrics to track** | Deal premium, regulatory approval timeline, KIE reaction as a read on sector consolidation sentiment |

---

## Segment-Matching Notes

There's no fixed weekly schedule here — every run auto-detects the segment
from the news. If a story spans more than one segment (e.g., a hurricane
story touches both P&C and reinsurance), pick the segment where the
**named companies and quantifiable numbers** are richest, and mention the
secondary segment in one sentence.

If no clearly insurance-specific story breaks in the search window, default
to **Property & Casualty** and pull `KIE` plus the top 3-4 insurer stocks by
weight in that ETF, framed as "This Week/Day in Insurance Stocks."
