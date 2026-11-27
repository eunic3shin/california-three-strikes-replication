# Pointing to the Price of Punishment: California's Three Strikes Law on Incarceration Outcomes

[![Archived v1.0.0 DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24588356.svg)](https://doi.org/10.5281/zenodo.24588356)

This replication code and manuscript source accompanies [Eunice Shin’s working paper](https://doi.org/10.5281/zenodo.24553443). The preferred manuscript citation is in [CITATION.cff](CITATION.cff).

## Running the analysis

Install Python 3.11–3.13, uv, and R with `Rscript` on your PATH. Additional R package requirements for preprocessing and figure redraws are listed in the data availability guide. Place the archived analysis inputs described in [Data availability](DATA_AVAILABILITY.md) under `data/`, then run from the repository root:

```sh
uv run --locked scons
```

The default build produces `output/california_1994_law.pdf` (three difference-in-differences regressions for Table 2) and `output/derived/state_year_panel.csv`.

The archived datasets and published figure image files are not bundled. A fresh checkout requires separately acquired inputs to generate results. See the [replication notes](docs/replication-notes.md) for differences from the manuscript and the analyses covered by the code.

## Full manuscript build

After obtaining the authorized inputs and published figure files at the paths listed in [archive correspondence](docs/archive-correspondence.md), install a full TeX distribution with `latexmk`, Biber, and `biblatex-chicago`.

```sh
uv run --locked scons manuscript
```

By default the manuscript uses archived publication figures. Synthetic-control re-estimation and figure redraws are available via `redraw-figures`; see the acquisition guide.

## Starting from raw provider downloads

See the [complete acquisition and preparation workflow](DATA_AVAILABILITY.md). The reconstructed pipeline has been execution-tested; see the validation status and replication notes for the scope of numerical checks. To compile with newly drawn figures rather than separately obtained publication PNGs, use `uv run --locked scons manuscript FIGURES=redrawn` after completing preparation and figure redraws.

## Validation status (2026-11-27)

Local macOS execution verified: raw preprocessing, all three original DID regression outputs, Table 1 rounded summary statistics, figure redraws and 22-page manuscript compilation. See replication notes for rounding, missing-record coding, magnitude-based stars, placebo failures and incomplete figure equivalence.

## Cite the replication package

Shin, Eunice (2026). Pointing to the Price of Punishment: California's Three Strikes Law on Incarceration Outcomes: Research replication archive. Version 1.0.0. Zenodo. https://doi.org/10.5281/zenodo.24588356.

The DOI identifies the archived [v1.0.0 release](https://github.com/eunic3shin/california-three-strikes-replication/releases/tag/v1.0.0), not subsequent changes on main. Cite the associated paper separately when discussing research findings.
