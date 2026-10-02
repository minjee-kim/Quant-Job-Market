# Private market trends

This repo was analyzed using Grok.

Oracle of research these firms publish. One row per note in `data/raw/documents.csv`. `python src/oracle.py` prints the same list by firm.

Jane Street and Citadel do not publish trading research. Jane Street publishes intern machine-learning notes. Citadel Securities publishes market-structure notes. Citadel the hedge fund is absent because it does not publish a research series.

## By firm

HarbourVest QIS. Investment-level buyout benchmarks, and a NAV nowcast that estimates value before the GP report.

PitchBook. Cash-flow pacing and manager scores. IRR becomes a z-score inside vintage and strategy.

BlackRock Aladdin / Preqin. Peer benchmarks from LP cash flows, then asset-level private credit: leverage, defaults, recoveries.

StepStone. Private-debt allocation with net credit spread and credit stress loss. GP-led secondaries as a liquidity channel.

MSCI. The longest stale-price series. A 2020 nowcast through smooth NAVs, a 2026 daily NAV index, and a private real estate split of core versus value-added and opportunistic.

Hamilton Lane. Desmoothing. Observed buyout beta about 0.4. Desmoothed beta a bit above 1. The same adjustment is applied to real estate, infrastructure, and natural resources.

AQR. Volatility laundering: a smooth mark is not low risk. The 2026 note extends that claim to private credit.

Arctos. Post-2020 smoothing is asymmetric. Write-ups were fast. Write-downs lagged.

privateMetrics. A monthly market valuation anchor so the NAV does not stay stale.

Jane Street. September 2026 intern notes: autoregressive diffusion on US equity events, and LLM memorization on cricket previews. No alpha, no private markets.

Citadel Securities. Scott Rubner market-structure notes. First half of 2026: index concentration, passive ownership, retail flow, leverage, volatility. February 2026: single-stock dispersion and thin depth. No strategy research.

Two Sigma. Venn factor lens for 2024: equity styles, trend, equity short volatility. A public risk report, not a signal note.

## What repeats

Stale pricing is the private-markets theme. MSCI, Hamilton Lane, AQR, Arctos, and privateMetrics are describing the same lag. HarbourVest's nowcast is the product version of that lag.

The public-market shops do not write about that lag. Jane Street writes about generating event data. Citadel Securities writes about who is trading and how concentrated the index is.

## Limit

This is a document list with a theme tag, not a fitted model. A firm with one note is not a trend. MSCI and AQR are the only names here with the same claim restated across years.
