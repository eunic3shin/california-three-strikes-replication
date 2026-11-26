"""Render the California paper's Table 2 from the generated models."""

import csv
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def read_model(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return {row["term"]: row for row in csv.DictReader(stream)}


def main():
    incarceration, spending, arrests, output = map(Path, sys.argv[1:])
    models = [read_model(path) for path in (incarceration, spending, arrests)]
    centered = ParagraphStyle("Centered", fontName="Times-Roman", alignment=1)
    body = ParagraphStyle("Body", fontName="Times-Roman", leading=13)
    rows = [["Variable", "Total Incarcerated", "Corrections Spending", "Arrest Rate / 100k"]]
    for key, label in [
        ("treat", "Treat"), ("post", "Post"),
        ("treat_post", "Treat × Post"), ("const", "Constant"),
    ]:
        estimates, errors = [label], [""]
        for column, model in enumerate(models):
            row = model[key]
            p = float(row["p_value"])
            stars = "***" if p < .01 else "**" if p < .05 else "*" if p < .1 else ""
            digits = 2 if column == 2 else 0 if column == 0 and key in ("treat", "treat_post") else 1
            estimate = f'{float(row["estimate"]):.{digits}f}'
            estimates.append(Paragraph(
                estimate + (f"<super>{stars}</super>" if stars else ""), centered,
            ))
            digits = 2 if column == 2 or (column == 1 and key == "const") else 1
            errors.append(f'({float(row["standard_error"]):.{digits}f})')
        rows.extend([estimates, errors])
    rows.append(["R²", *[f'{float(m["const"]["r_squared"]):.3f}' for m in models]])
    rows.append(["N", *[m["const"]["observations"] for m in models]])

    table = Table(rows, colWidths=[88, 117, 132, 117])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("LINEABOVE", (0, 0), (-1, 0), .8, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), .5, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), .8, colors.black),
    ]))
    output.parent.mkdir(parents=True, exist_ok=True)
    SimpleDocTemplate(str(output), invariant=1).build([
        Paragraph("<b>DID Effect of 1994 Law on Variables</b>", centered),
        Spacer(1, 4), table, Spacer(1, 4),
        Paragraph("Source: Author’s calculations using ICPSR and NASBO data.", centered),
        Spacer(1, 10),
        Paragraph(
            "Table 2: Difference-in-Differences Regression Estimates of 1994 Law on Key Outcomes "
            "(with HC1 Robust Standard Errors)", body,
        ),
    ])


if __name__ == "__main__":
    main()
