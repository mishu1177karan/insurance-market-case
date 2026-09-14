# Case Audit — 2026-09-14 Reinsurance (Weekly)

## Event chosen
KBW said reinsurance executives it met with at the 2026 Rendez-Vous de Septembre expect property-catastrophe excess-of-loss reinsurance rates to fall at least 10% at the January 1, 2027 renewals, extending the softening cycle from Jan and June 2026.

Sources:
- Reinsurance News, "Property cat XoL reinsurance rates expected to fall by at least 10% at 1.1 2027, reports KBW," Sept 11, 2026 — https://www.reinsurancene.ws/property-cat-xol-reinsurance-rates-expected-to-fall-by-at-least-10-at-1-1-2027-reports-kbw/
- Business Insurance, "Property cat reinsurance rates projected to fall at least 10%," Sept 2026 — https://www.businessinsurance.com/property-cat-reinsurance-rates-projected-to-fall-at-least-10/

## Segment + slug
Reinsurance — `reinsurance`.

## Cadence
Weekly.

## yfinance metrics (via Yahoo v8 chart API, as-of 2026-09-14)

| Ticker | Name | Current | 1W chg | 1M chg | 3M chg |
|--------|------|---------|--------|--------|--------|
| EG | Everest Group | $379.76 | -0.29% | +2.61% | +12.44% |
| RGA | Reinsurance Group of America | $249.07 | -1.66% | -0.15% | +18.92% |
| RNR | RenaissanceRe | $330.36 | -0.01% | +2.16% | +9.89% |
| SPNT | SiriusPoint | $24.63 | +0.61% | +3.84% | +5.80% |
| KIE | SPDR S&P Insurance ETF (benchmark) | $63.21 | -1.09% | -1.63% | +7.51% |

Note: the topic map originally listed Everest Group's ticker as `RE` — that
ticker 404'd against the Yahoo v8 API. Confirmed via web search that Everest
Group, Ltd. trades as `EG` on NYSE (it uses the same symbol it held before
its 2023 rename from Everest Re Group). Fixed in
`references/insurance_topic_map.md` before pulling data; all five tickers
resolved successfully afterward.

## Numbers placed in the Key Numbers table
- Everest Group (EG): $379.76, -0.3% (1W) — matches above.
- Reinsurance Group of America (RGA): $249.07, -1.7% (1W) — matches above.
- RenaissanceRe (RNR): $330.36, -0.0% (1W) — matches above (actual -0.0076%, rounds to -0.0%/flat).
- SiriusPoint (SPNT): $24.63, +0.6% (1W) — matches above.
- KIE: $63.21, -1.1% (1W) — matches above.

## Chart content description
Everest Group, Reinsurance Group of America, RenaissanceRe, and SiriusPoint (solid lines) plus KIE (dashed line, benchmark), daily closes normalized to 100 at the start of the trailing 3-month window ending 2026-09-14. Vertical dashed line at 2026-09-11 marks the KBW rate-outlook report. Y-axis upper bound set to ≥1.10x the max normalized series value per the skill's chart-readability rule.

## Proxy-ticker disclosure
Not applicable — Reinsurance has direct pure-play public tickers (EG, RGA, RNR, SPNT); no proxy used.

## Historical parallel
The 2017 hurricane season (Harvey, Irma, Maria) hardened the reinsurance market for years afterward — cited in `insurance_topic_map.md`'s Reinsurance row. Framed here as the mirror-image mechanism: two years of below-average catastrophe losses (Swiss Re: $42B H1 2026 insured cat losses, lowest H1 since 2020) let capital rebuild and rates soften, versus 2017's heavy losses that hardened rates.

## Segment fit
Matched to the "Reinsurance" row in `references/insurance_topic_map.md`. Tickers (EG [corrected from RE], RGA, RNR, SPNT, KIE) match that row's list. News keywords used (reinsurance rates, treaty renewal, hard market, soft market, January renewals) are from that row's keyword list. Historical parallel (2017 hurricane season hardening the market) is that row's listed parallel.

## Secondary stories (weekly) — ROUND 2, corrected per critic round-1 BLOCK

1. **Property & Casualty** — Triple-I/Milliman project US P&C insurers' underlying growth falling to -3.7% in H1 2026 vs +1.6% in 2025. Source: Insurance Journal, **May 21, 2026** (corrected from round 1's wrong "Sept 2026" label) — https://www.insurancejournal.com/news/national/2026/05/21/870937.htm. Staleness now explicitly disclosed in the HTML text.
2. **Reinsurance / ILS** (replaces round 1's duplicate Cat & Climate item) — Non-life alternative reinsurance capital grew 9% in H1 2026 to a record $147B per Gallagher Re; cat bond issuance hit a record ~$18B for the half. This is a distinct angle from the top story's $42B loss figure (round 1 duplicated that figure verbatim, which the critic flagged). Source: Artemis.bm, **Sept 1, 2026** — https://www.artemis.bm/news/alternative-capital-rose-9-in-h126-to-record-147bn-gallagher-re/
3. **InsurTech / Auto** — Clearcover launched a new Florida auto insurance product plus a "26 for '26" agent incentive program (runs May-Dec 2026). Source: FinTech Global, **April 30, 2026** (corrected from round 1's generic, undated Insurance Journal tag-page link) — https://fintech.global/2026/04/30/clearcover-launches-flexible-auto-insurance-in-florida/
4. **Regulation** — FSB consultation on "Sound Practices for Responsible Adoption of AI." Round 1 incorrectly claimed the comment period "remains open"; corrected to state the comment period closed **July 22, 2026** and a final report is due **October 2026**. Source: FSB directly (corrected from round 1's indirect One Inc citation), published June 10, 2026 — https://www.fsb.org/2026/06/fsb-consults-on-sound-practices-for-the-responsible-adoption-of-artificial-intelligence-ai/

All four items now carry their real, verified publish dates disclosed in the HTML text itself (not just this audit), matching the pattern the critic praised in round 1's FSB item.

## Render status
HTML written successfully to `2026-09-14_reinsurance.html` (round 2, corrected). PDF re-rendered via headless browser fallback (Microsoft Edge `--headless --print-to-pdf`) after the HTML fixes — confirmed present at `2026-09-14_reinsurance.pdf` (260,170 bytes).
