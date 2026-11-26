# Replication notes

The Table 2 scripts preserve the exploratory 1989–2005 window and HC1 specification. Local validation on 2026-11-27 reproduced all three original notebook regressions at displayed precision after restoring the balanced incarceration panel. The printed table still has transcription/inference differences (including the spending constant standard error). The build preserves calculated values. The conventional R fit is available via `uv run --locked scons output/california_1994_law_diagnostic.pdf`.

Table 1 and published figures are retained in the manuscript workflow (figure files must be obtained separately). Synthetic-control re-estimation and upstream raw-data construction are available as separate targets. See [Data availability](../DATA_AVAILABILITY.md) for the archived intermediates required by the included code.

The public repository now includes recovered preprocessing and figure redraw routines. See [data acquisition](../DATA_AVAILABILITY.md) for exact prerequisites, reconstruction assumptions, and remaining validation gaps. The archived analysis scripts are preserved; reconstructed figures must not be assumed identical to publication PNGs.

## Table 1 inference and figure provenance

The historical Table 1 notebook assigned stars by absolute effect size (20, 10, and 5), not p-values. The printed significance legend is therefore not supported by that routine. The recovered redraw exports unstarred Table 1 summary and difference CSVs for comparison. It does not silently replace the printed table. The original arrest placebo plot and the spending placebo diagnostic are distinct; the former is used for the manuscript's Placebo.png. Table 2 uses HC1 regression standard errors as documented above.

## Local regression validation (2026-11-27)

The author ran the raw-data pipeline locally. Arrests and spending matched the saved original HC1 regression output at displayed precision. The initial observed-only NCRP grouping produced 572 observations through 2005. Explicitly reindexing to 51 geographic units by 1991–2005, filling absent record counts with zero, reproduced the original 765 observations, R² 0.708, interaction coefficient approximately 28,800 and HC1 standard error 3,037.572, as well as the remaining displayed regression statistics. The preprocessing now explicitly produces the historical balanced 1991–2019 count panel rather than depending on pandas categorical grouping defaults. The updated committed pipeline still needs a local rerun. Zero-count cells denote no records in the extract, not established zero incarceration; the historical convention is retained for replication, not endorsed as a missing-data correction. Synthetic control numerical equivalence and manuscript compilation remain unverified. The original arrest placebo notebook skipped failed fits; the initial redraw reported failures for Indiana and Rhode Island. These should be reported, not silently treated as successful placebos.
