# Case Audit — 2026-09-14 Health Insurance (Daily)

## Event chosen
Marsh's 2026 National Survey of Employer-Sponsored Health Plans (1,800+ US employers) found total health benefit cost per employee projected to rise 8.2% in 2027 even after planned cost-reduction measures — the steepest increase since 2003 — while KFF's analysis of 276 insurers found ACA marketplace insurers proposing a median 15% premium increase for 2027.

Sources:
- Marsh (BusinessWire), "Employers Expect Health Benefit Costs to Jump 8.2% in 2027," Sept 2, 2026 — https://www.businesswire.com/news/home/20260902423651/en/Employers-Expect-Health-Benefit-Costs-to-Jump-8.2-in-2027-and-the-Impact-Will-Likely-Be-Felt-by-Workers-According-to-Marsh
- KFF, "ACA Marketplace Insurers Are Proposing a Median Premium Increase of About 15% in 2027," Sept 2026 — https://www.kff.org/quick-insights/aca-marketplace-insurers-are-proposing-a-median-premium-increase-of-about-15-in-2027/

## Segment + slug
Health Insurance — `health_insurance`.

## Cadence
Daily.

## yfinance metrics (via Yahoo v8 chart API, as-of 2026-09-14)

| Ticker | Name | Current | 1D chg | 1W chg | 1M chg |
|--------|------|---------|--------|--------|--------|
| UNH | UnitedHealth | $383.82 | +1.25% | -3.36% | -4.46% |
| CI | Cigna | $288.61 | +2.80% | +2.16% | +2.14% |
| HUM | Humana | $414.18 | +1.07% | +3.15% | +6.46% |
| ELV | Elevance Health | $423.60 | +1.16% | +3.95% | +5.81% |
| CVS | CVS Health | $95.63 | +1.02% | -1.15% | -1.57% |

## Numbers placed in the Key Numbers table
- UnitedHealth (UNH): $383.82, +1.2% (1D) — matches above.
- Cigna (CI): $288.61, +2.8% (1D) — matches above.
- Humana (HUM): $414.18, +1.1% (1D) — matches above.
- Elevance Health (ELV): $423.60, +1.2% (1D) — matches above.
- CVS Health (CVS): $95.63, +1.0% (1D) — matches above.

## Chart content description
UnitedHealth, Cigna, Humana, Elevance Health, and CVS Health daily closes, normalized to 100 at the start of the trailing 3-month window (3-month lookback ending 2026-09-14). Vertical dashed line at 2026-09-02 marks the Marsh survey release. Y-axis upper bound set to ≥1.10x the max normalized series value per the skill's chart-readability rule.

## Proxy-ticker disclosure
Not applicable — Health Insurance has direct pure-play public tickers (UNH, CI, HUM, ELV, CVS); no proxy used.

## Historical parallel
ACA passage and rollout (2010-14), when insurers repriced individual-market risk pools amid new coverage mandates — cited in `insurance_topic_map.md`'s Health Insurance row.

## Segment fit
Matched to the "Health Insurance" row in `references/insurance_topic_map.md`. Tickers (UNH, CI, HUM, ELV, CVS) and news keywords (health insurance, premium increase, ACA, Medicare Advantage) are exactly that row's listed tickers/keywords. Historical parallel (ACA rollout) is also that row's listed parallel.

## Secondary stories (weekly only)
N/A — this is a daily brief.

## Render status
HTML written successfully to `2026-09-14_health_insurance.html`. PDF rendered via headless browser fallback (Microsoft Edge `--headless --print-to-pdf`) after an initial bug in `scripts/html_to_pdf.py` (relative output path caused "Access is denied") was found and fixed; PDF confirmed present at `2026-09-14_health_insurance.pdf` (256,158 bytes) after the fix.
