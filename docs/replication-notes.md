# Replication notes

The Table 2 scripts preserve the exploratory 1989–2005 window and HC1 specification. The generated incarceration Treat and Treat × Post estimates, incarceration Post stars, and spending constant standard error differ from the printed table. The build preserves calculated values. The conventional R fit is available via `uv run --locked scons output/california_1994_law_diagnostic.pdf`.

Table 1 and published figures are retained in the manuscript workflow (figure files must be obtained separately). Synthetic-control re-estimation and upstream raw-data construction remain outside the build. See [Data availability](../DATA_AVAILABILITY.md) for the archived intermediates required by the included code.

The public repository now includes recovered preprocessing and figure redraw routines. See [data acquisition](../DATA_AVAILABILITY.md) for exact prerequisites, reconstruction assumptions, and remaining validation gaps. The archived analysis scripts are preserved; reconstructed figures must not be assumed identical to publication PNGs.
