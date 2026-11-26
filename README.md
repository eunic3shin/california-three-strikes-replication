# Pointing to the Price of Punishment: California's Three Strikes Law on Incarceration Outcomes

This code-only replication archive accompanies [Eunice Shin’s working paper](https://doi.org/10.5281/zenodo.24553443). The preferred manuscript citation is in [CITATION.cff](CITATION.cff).

## Running the analysis

Install Python 3.11–3.13, uv, and R with `Rscript` on your PATH. The R scripts use base R. Place the archived analysis inputs described in [Data availability](DATA_AVAILABILITY.md) under `data/`, then run from the repository root:

```sh
uv run --locked scons
```

The default build produces `output/california_1994_law.pdf` (three difference-in-differences regressions for Table 2) and `output/derived/state_year_panel.csv`.

The archived data and manuscript assets are excluded. A fresh checkout requires separately acquired inputs to generate results. See the [replication notes](docs/replication-notes.md) for differences from the manuscript and the analyses covered by the code.
