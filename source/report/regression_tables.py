"""Render the archived regression specifications into one PDF."""

import argparse
import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def render_table(path):
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    cells = [["Term", "Estimate", "Standard error", "p-value", "Observations"]]
    for row in rows:
        cells.append([
            row["term"],
            f'{float(row["estimate"]):,.3f}',
            f'{float(row["standard_error"]):,.3f}',
            f'{float(row["p_value"]):.3g}',
            row["observations"],
        ])
    table = Table(cells, colWidths=[124, 80, 92, 74, 78], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9eef4")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.HexColor("#b3becb")),
    ]))
    return table


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("incarceration_did", type=Path)
    parser.add_argument("incarceration_ols", type=Path)
    parser.add_argument("arrests_did", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()

    title = "California's 1994 Three Strikes Law"
    styles = getSampleStyleSheet()
    story = [Paragraph(title, styles["Title"])]
    for heading, path in [
        ("Incarceration (Python, HC1)", args.incarceration_did),
        ("Incarceration (R, conventional standard errors)", args.incarceration_ols),
        ("Arrest rate per 100,000 (Python, HC1)", args.arrests_did),
    ]:
        story.extend([Paragraph(heading, styles["Heading2"]), render_table(path), Spacer(1, 14)])

    args.output_pdf.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(args.output_pdf), title=title, invariant=1)
    document.build(story)


if __name__ == "__main__":
    main()
