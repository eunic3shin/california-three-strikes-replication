# Data acquisition and preparation

Download third-party data from the original providers under their access terms. Record the release, download date, and any data-use agreement. The working paper is [available on Zenodo](https://doi.org/10.5281/zenodo.24553443).

## 1. Obtain the upstream data

| Source | Acquisition instructions |
| --- | --- |
| [ICPSR 38048, NCRP selected variables, 1991–2019](https://doi.org/10.3886/ICPSR38048.v1) | Sign in, review access requirements, obtain the applicable Stata data and codebook. The historical archive references 38048-0003-Data.dta; check the corresponding study file and record type before aggregating. |
| [ICPSR 38047, NCRP complete release](https://doi.org/10.3886/ICPSR38047.v1) | This is the study cited in the paper, but the catalog describes coverage of 2000–2019. Do not treat it as an interchangeable substitute for 38048. Exact original release/file selection must be verified. |
| [ICPSR UCR resource guide](https://www.icpsr.umich.edu/sites/nacjd/posts/shared/uniform-crime-reporting-program-resource-guide) | Under Arrests by Age, Sex, and Race, Summarized Yearly, obtain the annual agency files for 1989–1999 (the recovered historical notebooks cover these years). The guide links each year; examples: [1999](https://doi.org/10.3886/ICPSR23366.v1), [2000](https://www.icpsr.umich.edu/web/NACJD/studies/3997), [2005](https://www.icpsr.umich.edu/web/NACJD/studies/4716). Download corresponding codebooks. |
| [NASBO State Expenditure Report](https://www.nasbo.org/reports-data/state-expenditure-report) | Select Download Historical Data; the archived workbook is named State-Exp-Report-Data.xlsm. The paper cites the 1991–2024 edition. Consult the [report archive](https://www.nasbo.org/reports-data/state-expenditure-report/state-expenditure-archives) for the historical edition rather than assuming the latest workbook is identical. |

## 2. Prepare local analysis inputs

Create a local data directory with `mkdir -p data`. The code expects prepared state-year files, not raw provider downloads.

| File under data/ | Required preparation and key fields |
| --- | --- |
| incarceration_counts.csv | Aggregate the appropriate NCRP custody/count records by state and year; STATE, Year, Total People Incarcerated. Verify original inclusion rules and coverage. |
| arrest_rates.csv | Aggregate annual agency arrest counts by state and year, attach the archived population denominator and compute the rate per 100,000; STATE, YEAR, total_arrests, POP, Arrest Rate per 100,000. Avoid double-counting overlapping offense totals. |
| corrections_spending.csv | Extract total corrections expenditure by state and fiscal year from NASBO; State, YEAR, Total Corrections Spending. Confirm units, fund coverage and nominal/real treatment against the archive. |
| States_3_Strikes.xlsx | Author-constructed state-year scaffold containing State, Year, POP, policy indicators, and placeholder columns Arrest Rate per 100,000, Corrections Normalized, Total Corrections Spending, Incarcerated Normalized, Total People Incarcerated. This is not an upstream downloadable dataset. Its original policy coding and population series need to be recovered. |

Use full state names, integer years and matching state-year keys. The three regressions select 1989–2005; the panel script retains years from 1991 onward. The regressions define California as treatment and 1994 onward as post. Do not invent observations for years not covered by a source. The merged panel and historical workbook listed in [archive correspondence](docs/archive-correspondence.md) are reference assets, not additional default-build requirements.

The precise raw aggregation rules, population source, policy scaffold and some release details are not fully recovered. The links above therefore enable independent source acquisition, but do not yet guarantee reconstruction of the exact archived analysis inputs. For matching prepared inputs, consult the author under applicable provider terms.

## 3. Run the analysis

Install uv, Python 3.11–3.13 and R. From the repository root:

```sh
uv run --locked scons
uv run --locked scons output/california_1994_law_diagnostic.pdf
```

The default build generates Table 2 and the merged state-year panel. To compile the manuscript, separately obtain the six original PNGs listed in [archive correspondence](docs/archive-correspondence.md), install LaTeX, latexmk, Biber and biblatex-chicago, and run `uv run --locked scons manuscript`. The paper DOI provides a visual reference, not necessarily the original image files. Synthetic-control re-estimation is now available through the separate redraw target below.

See [replication notes](docs/replication-notes.md) for known numerical differences. No third-party data are bundled. The local data directory is gitignored.

## Recovered preprocessing workflow

Place the original Stata files in data/raw/ using these historical filenames (each study number has its own ICPSR study landing page):

| Year | Study | Filename |
| --- | --- | --- |
| 1989 | [23339](https://www.icpsr.umich.edu/web/NACJD/studies/23339) | 23339-0001-Data.dta |
| 1990 | [23341](https://www.icpsr.umich.edu/web/NACJD/studies/23341) | 23341-0001-Data.dta |
| 1991 | [23343](https://www.icpsr.umich.edu/web/NACJD/studies/23343) | 23343-0001-Data.dta |
| 1992 | [23345](https://www.icpsr.umich.edu/web/NACJD/studies/23345) | 23345-0001-Data.dta |
| 1993 | [23347](https://www.icpsr.umich.edu/web/NACJD/studies/23347) | 23347-0001-Data.dta |
| 1994 | [23361](https://www.icpsr.umich.edu/web/NACJD/studies/23361) | 23361-0001-Data.dta |
| 1995 | [23362](https://www.icpsr.umich.edu/web/NACJD/studies/23362) | 23362-0001-Data.dta |
| 1996 | [23363](https://www.icpsr.umich.edu/web/NACJD/studies/23363) | 23363-0001-Data.dta |
| 1997 | [23364](https://www.icpsr.umich.edu/web/NACJD/studies/23364) | 23364-0001-Data.dta |
| 1998 | [23365](https://www.icpsr.umich.edu/web/NACJD/studies/23365) | 23365-0001-Data.dta |
| 1999 | [23366](https://www.icpsr.umich.edu/web/NACJD/studies/23366) | 23366-0001-Data.dta |
| 1991–2005 analysis | [38048](https://doi.org/10.3886/ICPSR38048.v1) | 38048-0003-Data.dta |

Also place State-Exp-Report-Data.xlsm in data/raw/. The original annual cleaning notebooks cover 1989–1999; the regression code applies an upper bound of 2005 but no additional UCR years are assumed in this reconstruction.

```sh
uv run --locked scons prepare-data
uv run --locked scons
```

The preparation target now reconstructs data/States_3_Strikes.xlsx from the historical policy coding and prepared UCR data. The three Table 2 regressions alone can be run via `uv run --locked scons output/california_1994_law.pdf`.

The [preprocessing script](source/derived/prepare_inputs.py) retains the historical annual row trims, missing-age-count handling, summed POP across offense rows, NCRP record counts, and NASBO CORR_TOT extraction. In particular, the archived POP denominator is not a unique state population, and NCRP record counts need not equal unique persons. These choices are preserved for transparency rather than endorsed as corrected measures. The exact reconstructed intermediate values have not been validated against the archived files.

## Complete reconstructed workflow

Install R packages Synth, readxl and nnls in addition to the base R runtime. The policy scaffold is generated from the archived 50-state, 1991–1999 coding and the UCR state-year keys. These are historical author-coded flags, not independently verified legal enactment dates. All 450 archived policy flags and pre/post indicators match the reconstructed rule, and all 450 population values match the archived UCR aggregate denominator. The raw files have not been reprocessed for numerical validation.

```sh
uv run --locked scons prepare-data
uv run --locked scons
uv run --locked scons redraw-figures
uv run --locked scons manuscript FIGURES=redrawn
```

The last command uses regenerated PNGs rather than archived publication figures. The synthetic-control redraw retains the historical donor selection (including states with any zero policy indicator), and the incarceration redraw uses nonnegative least squares without an intercept, rather than imposing a sum-to-one constraint. Historical missing outcome zeros are used in the synthetic-control figure script. These choices are retained for replication, not presented as improved identification. Table 1 remains the printed manuscript table. The redraw target also exports unstarred reconstructed Table 1 statistics and differences; their numerical correspondence has not been verified. The original Table 1 magnitude-based stars do not represent statistical tests (see replication notes).

## Numerical validation against an authorized reference archive

After preparation, if you have access to the original archived intermediate CSVs, run:

```sh
uv run --locked python source/verify_inputs.py data /path/to/archive/data arrest_rates.csv incarceration_counts.csv corrections_spending.csv
```

The checker compares schemas, row counts, duplicate-preserving sorted rows and numeric values within a stated tolerance. It fails on discrepancies or missing files. Sorting by all columns may make near-tied numeric rows compare out of order; inspect such failures individually. No archived input data are included or requested by this checker. This comparison is not a substitute for validating the final regression estimates or figure outputs.
