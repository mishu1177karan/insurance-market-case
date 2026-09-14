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
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, WebSearch, WebFetch, Task
---

# Insurance Market Case — Workflow

You are generating a news brief for people who track the insurance industry.
Output is **HTML and PDF only** — no slide deck, no LaTeX. The HTML is the
canonical version (styled, readable in a browser); the PDF is rendered from
that same HTML so the two never drift apart.

**Time budget**: daily brief under 3 minutes; weekly roundup under 5 minutes
(the review gate in Steps 6-7 adds another 30-60s on top of that).

**Review policy**: ship after the first critic pass if the score is ≥80 and
no factual check scored below half — don't pause for confirmation. If the
critic BLOCKs, run the auto-revise loop (Step 7) rather than asking the user
what to do; only surface residual BLOCK items after 3 rounds.

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

### Emit the case audit (`{slug}_case_audit.md`)

The `insurance-case-critic` (Step 6) is read-only and cannot run your
scripts, open the chart PNG, or render the PDF — it relies entirely on this
audit. Write it into the same output folder as
`{YYYY-MM-DD}_{segment_slug}_case_audit.md`, `encoding='utf-8'`. Record:

- **Event chosen** — one line, plus 2-3 source URLs with their publish dates.
- **Segment + slug** — e.g. "Health Insurance — `health_insurance`".
- **Cadence** — daily or weekly.
- **yfinance metrics** — a small table (ticker, name, current value, period %
  change, as-of date). These are the raw numbers behind the Key Numbers
  table and the chart.
- **Numbers placed in the Key Numbers table** — the exact values you wrote
  into the HTML, so the critic can compare them to the yfinance metrics.
- **Chart content description** — one line naming the series plotted, the
  window, and what the annotation marks. The critic can't open the PNG, so
  this is its only way to verify the chart caption against the audit.
- **Proxy-ticker disclosure** — if the segment used a proxy (cyber →
  `CIBR`, cat/climate → P&C/reinsurance names), note it here and confirm the
  HTML says so explicitly too.
- **Historical parallel** — the past event you cited and its date.
- **Segment fit** — which row of `references/insurance_topic_map.md` you
  matched to, and why (so the critic can check the tickers/keywords/parallel
  actually belong to that segment, not a different one).
- **Secondary stories** (weekly only) — for each: headline, 1-sentence
  summary, source URL, publish date.
- **Render status** — HTML written successfully; PDF render method used
  (weasyprint / headless browser / failed) and outcome.

Do **not** report to the user yet — proceed to Step 6 (review gate). The
brief ships only after the critic signs off (or after the Step 7 revise
loop).

## Step 6: Review gate (critic)

Dispatch the **insurance-case-critic** via the Task tool. Point it at:
- the generated `.html`, and
- the `{slug}_case_audit.md` you just wrote.

It also reads `references/insurance_topic_map.md` itself. The critic
returns a scored **PASS/BLOCK** report as its message — it checks factual
accuracy (event veracity, direction/magnitude, dates, internal consistency)
and fit/quality (segment fit, proxy-ticker disclosure, prose/secondary-story
quality, render status). It has no Write/Edit/Bash tools, so it cannot touch
the brief — it only reports.

**Persist the report** to the same output folder as
`{slug}_critic.md` (overwrite in place each round; the report records the
round number).

- **On PASS:** go to Step 7's terminal report (skip the revise loop).
- **On BLOCK:** go to Step 7's revise loop.

## Step 7: Auto-revise loop

For each **BLOCK** item in the critic report, apply the minimal fix in place:

| Critic finding | Fix |
|----------------|-----|
| Event mischaracterized / wrong direction (checks #1, #2) | Correct the summary text and/or the Key Numbers table; if a metric itself is wrong, re-run the Step 2 data script for that ticker and update the table + chart |
| Fabricated / out-of-order date (check #3) | Correct or remove the date in the `.html` |
| Table ↔ chart ↔ audit disagree (check #4) | Reconcile to the yfinance metrics (authoritative), update the table and re-make the chart if needed |
| Wrong segment / mismatched tickers or historical parallel (check #5) | Re-match the event to the correct row in `insurance_topic_map.md`; re-pull tickers and re-check the parallel |
| Missing or unclear proxy-ticker disclosure (check #6) | Add an explicit one-sentence disclosure to the HTML (e.g. "CIBR is used as a sentiment proxy; no pure-play public cyber insurer exists") |
| AI-tells in prose, or a secondary story that's thin/duplicate/undated (check #7) | Rewrite the flagged sentence(s); for weekly, replace or properly source the flagged secondary story |
| Missing HTML or PDF (check #8) | Re-run `scripts/html_to_pdf.py` (max 2 attempts); if it still fails, follow the Failure-handling table below |
| **Chart y-axis clipping** | Compute each series' max, raise `ylim` to ≥1.10 × global max; re-render and recompile |
| **Chart annotation overlaps a data line** | Move the annotation to an empty zone; use `ax.annotate(..., arrowprops=dict(arrowstyle="->"))` |
| Missing audit / cannot verify | Re-emit a complete `{slug}_case_audit.md` |

Apply **all** blocking fixes in one pass, then:
1. Update `{slug}_case_audit.md` to reflect the corrected numbers/dates/segment.
2. Re-render the PDF (`scripts/html_to_pdf.py`, max 2 attempts).
3. Re-dispatch the `insurance-case-critic` (round 2).

**Max 3 rounds.** After round 3:
- **PASS** at any round → ship.
- **Still BLOCK after round 3** → ship the best version anyway and surface
  the residual BLOCK items to the user for a human decision.

## Step 8: Update the index and publish

Reports are tracked in git (not gitignored) — this repo is meant to build a
running, browsable archive on GitHub Pages. Once the brief has shipped
(PASS, or ship-on-strike-3):

1. Add an entry to the top of the relevant list (`Daily Briefs` or
   `Weekly Roundups`) in `index.html` at the repo root: headline linking to
   the `.html` report, and a meta line with the date, segment, a link to the
   `.pdf`, and the critic's final score (e.g. "PASS 100/100" or
   "BLOCK (shipped) 74/100").
2. `git add` the new report files (`.html`, `.pdf`, `.png`, `.csv`,
   `_case_audit.md`, `_critic.md`) plus the updated `index.html`.
3. Commit with a short message naming the date and segment (e.g.
   `Add 2026-09-15 health_insurance daily brief`).
4. `git push`.

If `git push` fails (no remote configured, auth issue, merge conflict),
don't force anything — report the failure to the user and leave the commit
local rather than guessing at a fix.

### Terminal report to the user

Report:
- The HTML path and the PDF path (local) and confirmation it was pushed
- One-sentence summary of the top story and which segment it maps to
- For weekly: how many secondary stories were included
- Any proxy-ticker caveats (cyber, cat/climate) if used
- The critic's final score and PASS/BLOCK verdict
- (If shipped on strike-3) the residual BLOCK items, by check number

## Failure handling

| Problem | What to do |
|---------|-----------|
| yfinance rate-limited or empty | Switch to the Yahoo v8 API helper (Step 2). If that also fails, drop the chart and replace it with a text-only "Key Moves" list in the report. |
| No relevant insurance news found | Default to Property & Casualty, pull `KIE` + top holdings, frame as "This Day/Week in Insurance Stocks." |
| PDF render fails (no weasyprint, no browser found) | Ship the HTML only. Tell the user to open it in a browser and print-to-PDF, or install `weasyprint`. |
| Web search times out | Skip the news search, use the most recent data available, frame as a generic market update. |
| Critic still BLOCK after 3 revise rounds | Ship the best version. Surface the residual BLOCK items (by check number) to the user for a human decision — do not loop further. |
| Critic cannot run (Task dispatch fails) | Skip the gate, ship the brief, and note in the terminal report that the review was skipped and the brief is **unreviewed**. |

## Speed tips

- Run news search and data fetch in parallel when possible.
- `period="3mo"` is enough context; don't pull a year of history.
- Keep the weekly roundup's secondary stories to one sentence each — the
  data workup is only for the top story.
