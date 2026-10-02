# Private market trends

This repo was analyzed using Grok.

The figures are frequency counts and a firm-by-category contingency table on 41 hand-coded phrases. No regression, topic model, or classifier was fit. A year trend is not identified: each phrase has one source date.

Language of private-markets quant research: what firms publish, and what they ask for.

First-pass sources are HarbourVest QIS, PitchBook, BlackRock Aladdin / Preqin, and StepStone. Phrases are in `data/raw/research_keywords.csv`. Counts below use that table only.

## Firm by category

HarbourVest writes about decisions. PitchBook writes about methods and multiples. BlackRock and StepStone are split between methods and performance metrics.

![Phrases by firm and category](figures/firm_category.png)

| Firm | Method | Performance metric | Decision use | Data object |
| --- | ---: | ---: | ---: | ---: |
| HarbourVest | 3 | 1 | 6 | 2 |
| PitchBook | 6 | 3 | 0 | 1 |
| BlackRock | 3 | 2 | 1 | 1 |
| StepStone | 2 | 2 | 0 | 0 |

HarbourVest's decision-use phrases are sector weight, timing, public-market comparison, manager selection, portfolio construction, and liquidity. PitchBook's methods are cash-flow forecasting, the Takahashi-Alexander model, Monte Carlo, z-score, manager score, and cash-flow speed.

## Category mix

Methods are the largest class. Market structure is two phrases: J-curve and GP-led secondaries.

![Phrase count by category](figures/category_counts.png)

| Category | Phrases |
| --- | ---: |
| Method | 14 |
| Performance metric | 8 |
| Decision use | 7 |
| Data object | 4 |
| Market structure | 2 |
| Research claim | 2 |
| Job skill | 2 |
| Asset class | 1 |
| Feeder skill | 1 |

## Research language and job language

Five phrases appear only in job text: Bayesian, time series, quantitative equity, Python, and SQL. Four appear in both: nowcasting, Monte Carlo, liquidity management, and GP-led secondaries. The rest are published research.

![Published research vs job-only language](figures/research_vs_job.png)

Python and SQL are in every current posting and are not tied to one firm. Quantitative equity is the HarbourVest feeder requirement. Bayesian and time series are named only on the BlackRock private-markets modeler seat.

## Specific themes

These rows are in `data/raw/theme_keywords.csv`. They are not in the charts above.

The repeated research problem is stale reported value. Firms use different names for it.

| Theme | Where it shows up |
| --- | --- |
| Stale pricing | Godwin (2022) uses secondary transaction prices and finds 75 to 92 percent of reported NAV variation is stale in PE, venture, real estate, and natural resources. MSCI nowcasts through smooth NAVs. privateMetrics anchors valuations to a monthly private-market benchmark so the NAV does not stay stale. AQR calls the same fact volatility laundering. |
| Return smoothing | Couts (2024) on private-equity real estate: autocorrelation comes from assets that are hard to value, not from internal versus external appraisal. Arctos finds post-2020 smoothing is asymmetric, fast write-ups and lagged write-downs. Hamilton Lane treats appraisal values as slower than traded prices. |
| Desmoothing | Hamilton Lane compares observed volatility, statistical desmoothing, and public-market proxies. Observed buyout beta is about 0.4. Their desmoothed beta is a bit above 1. The same de-smoothed series covers private real estate, infrastructure, and natural resources. |
| Private real estate | MSCI's fund index splits core and core-plus from value-added and opportunistic after the 2022 rate rise. Core held up better. StepStone cites a near-zero long-run correlation with the S&P 500. MSCI's Q1 2026 benchmarks have private real estate near a zero quarterly return, behind infrastructure and natural resources. |
| Valuation lag | Ercan, Kaplan, and Strebulaev measure staleness as the share of past quarters with a zero reported return. Staler investments and more frequent markdowns have worse later outcomes. Couts calls unchanged appraisals lame valuations. |
| Daily NAV | MSCI turns LP cash flows and historical valuations into daily private equity and private credit indexes. |

Firms added here: MSCI, Hamilton Lane, Arctos, privateMetrics, Ares, AQR. Ares has a quantitative research head, Avi Turetsky. The public note is about explaining performance, not a published model.

## Not a time trend

Counting phrases by year would repeat the document list, not a shift in research. A trend chart needs the same phrases counted in notes from 2022 through 2026.
