import os
import sys

env = Environment(ENV=os.environ, PYTHON=sys.executable)
rscript = env.WhereIs("Rscript")
if not rscript:
    print("Rscript is required. Install R and add Rscript to PATH.")
    Exit(1)

incarceration_did = env.Command(
    "output/tables/incarceration_did.csv",
    ["source/analysis/incarceration_did.py", "data/incarceration_counts.csv", "uv.lock"],
    '"$PYTHON" "${SOURCES[0]}" "${SOURCES[1]}" "$TARGET"',
)
incarceration_ols = env.Command(
    "output/tables/incarceration_ols.csv",
    ["source/analysis/incarceration_ols.R", "data/incarceration_counts.csv"],
    '"$RSCRIPT" --vanilla "${SOURCES[0]}" "${SOURCES[1]}" "$TARGET"',
    RSCRIPT=rscript,
)
arrests_did = env.Command(
    "output/tables/arrests_did.csv",
    ["source/analysis/arrests_did.py", "data/arrest_rates.csv", "uv.lock"],
    '"$PYTHON" "${SOURCES[0]}" "${SOURCES[1]}" "$TARGET"',
)
report = env.Command(
    "output/california_1994_law_diagnostic.pdf",
    ["source/report/regression_tables.py", incarceration_did, incarceration_ols, arrests_did, "uv.lock"],
    '"$PYTHON" "${SOURCES[0]}" "${SOURCES[1]}" "${SOURCES[2]}" "${SOURCES[3]}" "$TARGET"',
)
panel = env.Command(
    "output/derived/state_year_panel.csv",
    [
        "source/derived/state_year_panel.py",
        "data/States_3_Strikes.xlsx",
        "data/arrest_rates.csv",
        "data/corrections_spending.csv",
        "data/incarceration_counts.csv",
        "uv.lock",
    ],
    '"$PYTHON" "${SOURCES[0]}" "${SOURCES[1]}" "${SOURCES[2]}" "${SOURCES[3]}" "${SOURCES[4]}" "$TARGET"',
)
spending_did = env.Command(
    "output/tables/spending_did.csv",
    ["source/analysis/spending_did.py", "data/corrections_spending.csv", "uv.lock"],
    '"$PYTHON" "${SOURCES[0]}" "${SOURCES[1]}" "$TARGET"',
)
paper = env.Command(
    "output/california_1994_law.pdf",
    ["source/report/paper_table.py", incarceration_did, spending_did, arrests_did, "uv.lock"],
    '"$PYTHON" "${SOURCES[0]}" "${SOURCES[1]}" "${SOURCES[2]}" "${SOURCES[3]}" "$TARGET"',
)
Default(paper, panel)

manuscript_figures = [
    f"data/published-figures/{name}.png"
    for name in (
        "TotalCorrSpend", "corrections", "Incarcerated",
        "TreatIncarcerated", "ArrestsCAvsSynth", "Placebo",
    )
]
manuscript = env.Command(
    "output/california_1994_law_manuscript.pdf",
    [
        "source/manuscript/build.py", "source/manuscript/main.tex",
        "source/manuscript/Bibliography.bib",
        incarceration_did, spending_did, arrests_did, *manuscript_figures,
    ],
    '"$PYTHON" "${SOURCES[0]}" "${SOURCES[1]}" "${SOURCES[2]}" "${SOURCES[3]}" "${SOURCES[4]}" "${SOURCES[5]}" "$TARGET" ${SOURCES[6:]}',
)
Alias("manuscript", manuscript)
