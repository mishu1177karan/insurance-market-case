---
name: insurance-market-case
description: >
  Generate an insurance-industry market news brief as an HTML report and a
  matching PDF by searching recent insurance news, pulling live insurer/ETF
  stock data, and connecting it to the relevant insurance segment (P&C, life,
  health, reinsurance, cyber, catastrophe/climate, InsurTech, auto,
  regulation/M&A). Two cadences: a **daily** brief (single top story, past
  24-48h) and a **weekly** roundup (top story plus 3-5 secondary stories,
  past 7 days). TRIGGER when the user says "insurance news", "insurance
  brief", "daily insurance", "weekly insurance", "insurance roundup",
  "/insurance-daily", "/insurance-weekly", or wants an insurance-industry
  news case in HTML/PDF form.
argument-hint: "[daily|weekly] [optional segment override, e.g. 'cyber' or 'reinsurance']"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, WebSearch, WebFetch
---

# Insurance Market Case — Workflow

You are generating a news brief for people who track the insurance industry.
Output is **HTML and PDF only** — no slide deck, no LaTeX. The HTML is the
canonical version (styled, readable in a browser); the PDF is rendered from
that same HTML so the two never drift apart.

**Time budget**: daily brief under 3 minutes; weekly roundup under 5 minutes.

## Step 0: Parse the argument

- `/insurance-daily` or `daily` → daily brief: search the past 24-48 hours,
  one top story.
- `/insurance-weekly` or `weekly` → weekly roundup: search the past 7 days,
  one top story plus 3-5 secondary stories.
- No cadence given → default to **daily**.
- Optional segment override (e.g. `cyber`, `reinsurance`, `health`) forces
  the search toward that row in `references/insurance_topic_map.md`.
  Otherwise auto-detect the segment from whatever story you find.

## Step 1: Search for a teachable/reportable insurance event

Use WebSearch. Run 2-3 queries:

1. **General insurance**: `"insurance industry news" 2026` (daily) or
   `"insurance industry news this week" 2026` (weekly)
2. **Segment-specific** (if the user gave a segment override): use that
   segment's "News keywords" from `references/insurance_topic_map.md`
3. **Regulatory/cat angle** (always include): `insurance regulation OR
   catastrophe OR reinsurance news 2026`

Pick the most reportable event — the one with named companies and
quantifiable numbers (stock move, loss estimate, rate filing, deal size).
For the **weekly** cadence, also shortlist 3-5 secondary stories from the
same search pass; they don't need full data workups, just a headline,
1-sentence summary, and a source link each.

Tell the user which story you picked and which segment it maps to, then
move on — don't wait for confirmation unless the story is ambiguous.

## Step 2: Fetch market data

Match the event to a row in `references/insurance_topic_map.md` and pull
that row's tickers (3-6 of them) plus `KIE` (SPDR S&P Insurance ETF) as the
benchmark if it isn't already in the row.

**Fetching the data — yfinance first, Yahoo v8 API on 429.** Yahoo enforces
per-IP rate limits and `yfinance` reliably returns `429` on repeated calls:

- Try `yfinance.download(ticker, period="3mo", auto_adjust=True)` first.
- On any `429` / `YFRateLimitError` / empty frame, stop retrying yfinance
  and switch to the Yahoo v8 chart API helper below.

```python
import time, requests, pandas as pd
from datetime import datetime, timedelta

def yf_close(ticker, days=95):
    hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    params = {"period1": int((datetime.now() - timedelta(days=days)).timestamp()),
              "period2": int(time.time()), "interval": "1d", "events": "history"}
    r = requests.get(url, params=params, headers=hdr, timeout=30)
    r.raise_for_status()
    res = r.json()["chart"]["result"][0]
    close = res["indicators"]["quote"][0]["close"]
    s = pd.Series(close, index=pd.to_datetime(res["timestamp"], unit="s")).dropna()
    s.name = ticker
    return s
```

Add `time.sleep(1)` between ticker calls. Compute current level and %
change over 1D (daily brief) or 1W (weekly roundup), plus 1M/3M for context.
Save a CSV alongside the report for reproducibility.

**Segments with no clean public ticker** (cyber, catastrophe/climate) use a
proxy per the topic map (`CIBR` for cyber, the P&C/reinsurance names for
cat/climate) — say so explicitly in the report, don't imply it's a direct
measure.

## Step 3: Generate the chart

Write a short matplotlib script:
- `figsize=(9, 4)`, `dpi=160`, PNG output
- Normalize each series to 100 at its own first valid date (units differ:
  stock price vs. ETF price vs. proxy index) — see the normalization
  snippet below
- Light grid (`alpha=0.3, linestyle='--'`), no title inside the chart
  (the report gives it a caption instead)
- Annotate the event date with a vertical dashed line
- **y-axis must contain all peaks**: set the upper bound to ≥1.10 × the max
  of every normalized series
- Direct-label lines where possible; legend only for 4+ series, placed
  below the axes if there are 5+

```python
for col in df.columns:
    s = df[col].dropna()
    norm_s = s / s.iloc[0] * 100
    ax.plot(norm_s.index, norm_s.values, label=col)
```

Save the PNG into the same output folder as the report (Step 5).

## Step 4: Compose the HTML report

Read `references/report_template.html`. Copy it into the output folder and
fill in every `{{PLACEHOLDER}}`:

| Placeholder | Daily | Weekly |
|-------------|-------|--------|
| `{{REPORT_KICKER}}` | "Insurance Daily Brief" | "Insurance Weekly Roundup" |
| `{{REPORT_TITLE}}` | Short headline (≤70 chars) | Short headline for the top story |
| `{{REPORT_DATE_RANGE}}` | Single date | "Week of {start}–{end}" |
| `{{SEGMENT_NAME}}` | The matched segment | The matched segment for the top story |
| `{{HEADLINE}}` / `{{EVENT_DATE}}` / `{{SUMMARY_PARAGRAPH}}` | Top story, 2-3 sentences | Same |
| `{{METRICS_ROWS}}` | `<tr>` rows built from Step 2 data — use `class="chg-up"` / `class="chg-down"` on the change cell | Same |
| `{{CHART_IMAGE_PATH}}` / `{{CHART_ALT_TEXT}}` / `{{CHART_CAPTION}}` | Relative path to the PNG next to the HTML file | Same |
| `{{HISTORICAL_PARALLEL}}` | From the topic map's row | Same |
| `{{SECONDARY_STORIES}}` | **Delete the whole `<section class="weekly-only">` block** | Fill with `<li>` items: headline, 1 sentence, source link |
| `{{SOURCE_LIST}}` / `{{AS_OF_DATE}}` | Source links + data as-of date | Same |

For the daily cadence, delete the entire `<section class="weekly-only">...
</section>` block rather than leaving it empty — an empty "Also This Week"
header looks broken.

No AI-tells in the prose ("It's worth noting…", "delve into", "robust",
"moreover/furthermore" openers). Concrete claims, not hedging.

## Step 5: Create the output folder and render the PDF

**Output location**: `reports/daily/` or `reports/weekly/` depending on
cadence.

File naming: `{YYYY-MM-DD}_{segment_slug}.html` / `.pdf` / `_chart.png` /
`_data.csv` (weekly files use the Monday of that week as the date). If the
file already exists, append `_v2`, `_v3`, etc.

Render the PDF from the finished HTML with the helper script:

```bash
python scripts/html_to_pdf.py "reports/daily/2026-09-14_property_casualty.html" "reports/daily/2026-09-14_property_casualty.pdf"
```

It tries `weasyprint` first, then falls back to headless Edge/Chrome
`--print-to-pdf` (reliable on any Windows machine with Edge installed, which
is the default). If both fail, report the HTML path and tell the user to
open it and print-to-PDF manually from their browser — don't block on it.

## Terminal report to the user

Report:
- The HTML path and the PDF path
- One-sentence summary of the top story and which segment it maps to
- For weekly: how many secondary stories were included
- Any proxy-ticker caveats (cyber, cat/climate) if used

## Failure handling

| Problem | What to do |
|---------|-----------|
| yfinance rate-limited or empty | Switch to the Yahoo v8 API helper (Step 2). If that also fails, drop the chart and replace it with a text-only "Key Moves" list in the report. |
| No relevant insurance news found | Default to Property & Casualty, pull `KIE` + top holdings, frame as "This Day/Week in Insurance Stocks." |
| PDF render fails (no weasyprint, no browser found) | Ship the HTML only. Tell the user to open it in a browser and print-to-PDF, or install `weasyprint`. |
| Web search times out | Skip the news search, use the most recent data available, frame as a generic market update. |

## Speed tips

- Run news search and data fetch in parallel when possible.
- `period="3mo"` is enough context; don't pull a year of history.
- Keep the weekly roundup's secondary stories to one sentence each — the
  data workup is only for the top story.
