"""Recover archived data preparation from original research notebooks.

The UCR denominator is the historical sum of POP over offense rows, not
a unique state population. This is intentional for archive comparability.
"""
import argparse
from pathlib import Path
import pandas as pd

# Original annual notebooks: study IDs and positional trims.
UCR = {
    1989: (23339, 0, 0), 1990: (23341, 1, 1),
    1991: (23343, 0, 1), 1992: (23345, 0, 1),
    1993: (23347, 0, 1), 1994: (23361, 0, 1),
    1995: (23362, 0, 1), 1996: (23363, 0, 2),
    1997: (23364, 1, 2), 1998: (23365, 0, 1),
    1999: (23366, 0, 2),
}
AGES = "0_9 10_12 13_14 15 16 17 18 19 20 21 22 23 24 25_29 30_34 35_39 40_44 45_49 50_54 55_59 60_64 65".split()
AGE_COLS = [sex + age for sex in ("M", "F") for age in AGES]


def arrests(raw):
    annual = []
    for year, (study, start, tail) in UCR.items():
        df = pd.read_stata(raw / f"{study}-0001-Data.dta")
        df = df.iloc[start: -tail if tail else None].copy()
        df["total_arrests"] = (df[AGE_COLS].replace(999998, float("nan"))
                               .apply(pd.to_numeric, errors="coerce")
                               .fillna(0).sum(axis=1))
        if "YEAR" not in df:
            df["YEAR"] = year
        df["POP"] = pd.to_numeric(df["POP"], errors="raise")
        annual.append(df.groupby(["STATE", "YEAR"], observed=True, as_index=False)
                      [["total_arrests", "POP"]].sum())
    result = pd.concat(annual, ignore_index=True).sort_values(["STATE", "YEAR"])
    result["Arrest Rate per 100,000"] = result["total_arrests"] / result["POP"] * 100000
    return result


def incarceration(raw):
    # Historical Jail_Pop notebook counts records, not unique persons.
    df = pd.read_stata(raw / "38048-0003-Data.dta")
    df["STATE"] = df["STATE"].str.strip()
    df = df[df["RPTYEAR"].between(1991, 2019)]
    return (df.groupby(["STATE", "RPTYEAR"], observed=True).size()
            .reset_index(name="Total People Incarcerated")
            .rename(columns={"RPTYEAR": "Year"}))


def spending(raw):
    df = pd.read_excel(raw / "State-Exp-Report-Data.xlsm",
                       sheet_name="STATE EXP REPORT DATA")
    return (df.rename(columns={"Unnamed: 1": "State", "CORR_TOT": "Total Corrections Spending"})
            [["YEAR", "State", "Total Corrections Spending"]])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--only", choices=["arrests", "incarceration", "spending", "all"], default="all")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for key, fn, filename in [
        ("arrests", arrests, "arrest_rates.csv"),
        ("incarceration", incarceration, "incarceration_counts.csv"),
        ("spending", spending, "corrections_spending.csv"),
    ]:
        if args.only in (key, "all"):
            fn(args.raw).to_csv(args.output / filename, index=False)


if __name__ == "__main__":
    main()
