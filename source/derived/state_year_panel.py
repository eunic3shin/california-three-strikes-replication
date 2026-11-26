import argparse
from pathlib import Path

import pandas as pd

parser = argparse.ArgumentParser(description="Rebuild the archived Three Strikes state-year panel.")
parser.add_argument("states", type=Path)
parser.add_argument("arrests", type=Path)
parser.add_argument("spending", type=Path)
parser.add_argument("incarceration", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()

# Load main sheet
df = pd.read_excel(args.states)
df["State"] = df["State"].str.strip()
df["Year"] = df["Year"].astype(int)

# Load arrest rate data
arrests = pd.read_csv(args.arrests)
arrests = arrests.rename(columns={"STATE": "State", "YEAR": "Year"})
arrests["State"] = arrests["State"].str.strip()
arrests["Year"] = arrests["Year"].astype(int)

# Load corrections spending data
spending = pd.read_csv(args.spending)
spending = spending.rename(columns={"YEAR": "Year"})
spending["State"] = spending["State"].str.strip()
spending["Year"] = spending["Year"].astype(int)

# Load incarceration counts
incar = pd.read_csv(args.incarceration)
incar = incar.rename(columns={"STATE": "State"})
incar["State"] = incar["State"].str.strip()
incar["Year"] = incar["Year"].astype(int)

# Merge each one by State + Year
df = df.merge(arrests, on=["State", "Year"], how="left")
df = df.merge(spending, on=["State", "Year"], how="left")
df = df.merge(incar, on=["State", "Year"], how="left")

df = df.drop(columns=[
    "Arrest Rate per 100,000_x", 
    "Corrections Normalized", 
    "Total Corrections Spending_x", 
    "Incarcerated Normalized", 
    "Total People Incarcerated_x"
])

df["Corrections Normalized"] = (df["Total Corrections Spending_y"] / df["POP"]) * 100000
df["Incarcerated Normalized"] = (df["Total People Incarcerated_y"] / df["POP"]) * 100000

# Drop 1989–1990 from your dataset before merging or before model runs
df = df[df["Year"] >= 1991]

df= df.rename(columns={"Arrest Rate per 100,000_y":"Arrest Rate per 100,000","Total Corrections Spending_y": "Total Corrections Spending"\
                       ,"Total People Incarcerated_y": "Total People Incarcerated"})

args.output.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(args.output, index=False)
