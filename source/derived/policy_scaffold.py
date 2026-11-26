"""Reconstruct the historical author-coded policy scaffold from prepared UCR data.

Policy adoption years below are the first flagged years in the archived
1991–1999 panel, not independently verified legal enactment dates.
"""
import sys
from pathlib import Path
import pandas as pd

FIRST_FLAGGED = {
    "Arkansas": 1995, "California": 1994, "Colorado": 1994,
    "Connecticut": 1994, "Delaware": 1991, "Florida": 1995,
    "Georgia": 1994, "Indiana": 1994, "Kansas": 1994,
    "Louisiana": 1994, "Maryland": 1993, "Montana": 1995,
    "Nevada": 1995, "New Jersey": 1995, "New Mexico": 1994,
    "New York": 1991, "North Carolina": 1994, "North Dakota": 1995,
    "Pennsylvania": 1995, "South Carolina": 1995, "Tennessee": 1994,
    "Texas": 1991, "Utah": 1995, "Vermont": 1995, "Virginia": 1994,
    "Washington": 1993, "Wisconsin": 1994,
}


def main():
    arrests, output = map(Path, sys.argv[1:])
    data = pd.read_csv(arrests)
    data = data.loc[data.YEAR.between(1991, 1999) & data.STATE.ne("District of Columbia"),
                    ["STATE", "YEAR", "POP"]].rename(columns={"STATE": "State", "YEAR": "Year"})
    if len(data) != 450 or data.State.nunique() != 50 or data.duplicated(["State", "Year"]).any():
        raise ValueError("Expected archived 50-state, 1991–1999 panel (450 unique rows).")
    data["Pre/Post 1994"] = data.Year.ge(1994).astype(int)
    data["3 Strikes Law?"] = data.Year.ge(data.State.map(FIRST_FLAGGED).fillna(10000)).astype(int)
    for column in ["Arrest Rate per 100,000", "Corrections Normalized",
                   "Total Corrections Spending", "Incarcerated Normalized",
                   "Total People Incarcerated"]:
        data[column] = 0
    output.parent.mkdir(parents=True, exist_ok=True)
    data.sort_values(["State", "Year"]).to_excel(output, index=False)


if __name__ == "__main__":
    main()
