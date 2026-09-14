# insurance-market-case

A Claude Code skill that generates insurance-industry news briefs as an
**HTML report and a matching PDF** — no other formats. Two cadences:

- **Daily brief** — one top story, past 24-48 hours.
- **Weekly roundup** — one top story plus 3-5 secondary stories, past 7 days.

Each report pulls live insurer/ETF stock data (via `yfinance`, falling back
to the Yahoo v8 chart API on rate limits), builds a normalized performance
chart, and frames the event against the relevant insurance segment
(property & casualty, life, health, reinsurance, cyber, catastrophe/climate,
InsurTech, auto, regulation/M&A).

Every brief passes through a read-only review gate (`insurance-case-critic`)
before it ships — see [Review gate](#review-gate) below. Shipped reports are
committed to the repo and listed on the [GitHub Pages archive](#archive) —
this repo doubles as the published output, not just the skill source.

## Install as a Claude Code skill

Copy or clone this repo into your Claude Code skills directory, and copy
the critic into your agents directory:

```
git clone <this-repo-url> ~/.claude/skills/insurance-market-case
cp ~/.claude/skills/insurance-market-case/agents/insurance-case-critic.md ~/.claude/agents/
```

Then in a Claude Code session:

```
/insurance-daily
/insurance-weekly
/insurance-daily cyber        # force a segment
```

## Structure

```
insurance-market-case/
├── SKILL.md                        # the workflow Claude follows
├── index.html                      # GitHub Pages landing page, links every shipped report
├── agents/
│   └── insurance-case-critic.md    # read-only review-gate subagent (copy into ~/.claude/agents/)
├── references/
│   ├── insurance_topic_map.md      # segment -> tickers, keywords, chart type, historical parallels
│   └── report_template.html        # shared HTML template for both cadences
├── scripts/
│   └── html_to_pdf.py              # renders the finished HTML to PDF (weasyprint, else headless Edge/Chrome)
└── reports/
    ├── daily/                      # every shipped daily brief (.html, .pdf, .png, .csv, audit, critic report)
    └── weekly/                     # every shipped weekly roundup
```

## Archive

Reports are committed to the repo (not gitignored) so they build a running
history. **GitHub Pages** is enabled on this repo (main branch, root), so
`index.html` and every report `.html` file render as real webpages —
browse the archive at the Pages URL shown in the repo's "About" section,
rather than viewing raw HTML source in GitHub's file browser. After each
run, the skill (Step 8) adds the new report to `index.html`, commits, and
pushes automatically.

## PDF rendering

`scripts/html_to_pdf.py` tries `weasyprint` first (`pip install weasyprint`
for faster, dependency-free rendering), then falls back to headless
Microsoft Edge or Chrome's `--print-to-pdf`, which needs no extra install on
a normal Windows machine. If neither is available, the skill ships the HTML
alone and tells you to print-to-PDF from a browser.

## Notes on data

- `KIE` (SPDR S&P Insurance ETF) is the standard benchmark across segments.
- Cyber insurance and catastrophe/climate risk have no clean pure-play
  public ticker; the topic map uses documented proxies (`CIBR`, or the P&C/
  reinsurance names) and the report says so explicitly rather than implying
  a direct measurement.

## Review gate

Before a brief ships, the skill writes a `{slug}_case_audit.md` (the raw
data, sourcing, segment-match reasoning, and render status behind the
report) and dispatches `insurance-case-critic` — a read-only subagent
(Read/Grep/Glob/WebSearch/WebFetch only, no Write/Edit/Bash) — to score it
against 8 checks:

| # | Check | Weight |
|---|-------|--------|
| 1 | Event veracity | 15 |
| 2 | Direction/magnitude | 15 |
| 3 | Dates | 10 |
| 4 | Internal consistency (table ↔ chart ↔ audit) | 15 |
| 5 | Segment fit (tickers/keywords/parallel match the claimed segment) | 15 |
| 6 | Proxy-ticker disclosure (cyber/cat-climate) | 10 |
| 7 | Prose / secondary-story quality | 10 |
| 8 | Render status (HTML + PDF both produced) | 10 |

Checks 1-4 are factual checks: a **PASS** needs a total score ≥80 **and**
none of those four scoring below half their max — otherwise it's a
**BLOCK**, and the skill auto-revises (up to 3 rounds) before shipping the
best version and surfacing any residual issues to you.
