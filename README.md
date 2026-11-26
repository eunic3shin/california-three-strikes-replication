# Pointing to the Price of Punishment: California's Three Strikes Law on Incarceration Outcomes

This replication code and manuscript source accompanies [Eunice Shin’s working paper](https://doi.org/10.5281/zenodo.24553443). The preferred manuscript citation is in [CITATION.cff](CITATION.cff).

## Running the analysis

Install Python 3.11–3.13, uv, and R with `Rscript` on your PATH. The R scripts use base R. Place the archived analysis inputs described in [Data availability](DATA_AVAILABILITY.md) under `data/`, then run from the repository root:

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

The manuscript uses archived publication figures; synthetic-control re-estimation is not implemented. The DOI identifies the paper, not this code version.

## Starting from raw provider downloads

See the [complete acquisition and preparation workflow](DATA_AVAILABILITY.md). The reconstructed pipeline is not yet verified against the archived numerical outputs. To compile with newly drawn figures rather than separately obtained publication PNGs, use `uv run --locked scons manuscript FIGURES=redrawn` after completing preparation and figure redraws.
