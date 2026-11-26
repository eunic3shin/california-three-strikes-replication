"""Reproduce the archived Python arrest-rate regression."""

import argparse
from pathlib import Path

import pandas as pd
import statsmodels.api as sm


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()

    data = pd.read_csv(args.input_csv)
    sample = data.loc[data["YEAR"].between(1989, 2005)].copy()
    sample["arrest_rate_100k"] = sample["total_arrests"] / sample["POP"] * 100_000
    sample["treat"] = sample["STATE"].eq("California").astype(int)
    sample["post"] = sample["YEAR"].ge(1994).astype(int)
    sample["treat_post"] = sample["treat"] * sample["post"]

    design = sm.add_constant(sample[["treat", "post", "treat_post"]])
    fit = sm.OLS(sample["arrest_rate_100k"], design).fit(cov_type="HC1")
    table = pd.DataFrame({
        "estimate": fit.params,
        "standard_error": fit.bse,
        "p_value": fit.pvalues,
        "observations": int(fit.nobs),
        "r_squared": fit.rsquared,
    })
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.output_csv, index_label="term")


if __name__ == "__main__":
    main()
