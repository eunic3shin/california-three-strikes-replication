"""Insert the computed Table 2 and compile the California manuscript."""

import csv
import shutil
import subprocess
import sys
from pathlib import Path


def read_model(path):
    with path.open(newline="") as stream:
        return {row["term"]: row for row in csv.DictReader(stream)}


def fill(template, models):
    rows = []
    for key, label in [
        ("treat", "Treat"), ("post", "Post"),
        ("treat_post", r"Treat $\times$ Post"), ("const", "Constant"),
    ]:
        estimates, errors = [], []
        for i, model in enumerate(models):
            row = model[key]
            p = float(row["p_value"])
            stars = "***" if p < .01 else "**" if p < .05 else "*" if p < .1 else ""
            digits = 2 if i == 2 else 0 if i == 0 and key in ("treat", "treat_post") else 1
            number = f'{float(row["estimate"]):.{digits}f}'
            estimates.append(number + (rf"$^{{{stars}}}$" if stars else ""))
            digits = 2 if i == 2 or (i == 1 and key == "const") else 1
            errors.append(f'({float(row["standard_error"]):.{digits}f})')
        rows.extend([label + " & " + " & ".join(estimates), " & " + " & ".join(errors)])
    rows.extend([
        r"\midrule" + "\n$R^2$ & " + " & ".join(f'{float(m["const"]["r_squared"]):.3f}' for m in models),
        "$N$ & " + " & ".join(m["const"]["observations"] for m in models),
    ])
    start = template.index("\nTreat &", template.index("DID Effect of 1994 Law on Variables"))
    end = template.index(r"\bottomrule", start)
    table = "\n" + "".join(row + r" \\" + "\n" for row in rows)
    text = template[:start] + table + template[end:]
    for column, count, old_r2, old_pct, r2_digits, pct_digits in [
        (0, "765", "0.708", "70.8", 3, 1),
        (1, None, "0.464", "46.4", 3, 1),
        (2, None, "0.005251", "0.53", 6, 2),
    ]:
        stats = models[column]["const"]
        if count:
            text = text.replace(f"There were {count} observations.", f'There were {stats["observations"]} observations.')
        r2 = float(stats["r_squared"])
        text = text.replace(f"of {old_r2},", f"of {r2:.{r2_digits}f},").replace(
            old_pct + r"\%", f"{r2 * 100:.{pct_digits}f}" + r"\%"
        )
    return text


def main():
    template, bib, incarceration, spending, arrests, output, *figures = map(Path, sys.argv[1:])
    latexmk = shutil.which("latexmk")
    if not latexmk or not shutil.which("biber"):
        raise SystemExit("Install a full TeX distribution with latexmk and Biber to build the manuscript.")
    work = output.parent / "latex"
    work.mkdir(parents=True, exist_ok=True)
    source = work / f"{output.stem}.tex"
    text = fill(template.read_text(), [read_model(p) for p in (incarceration, spending, arrests)])
    source.write_text(text)
    shutil.copyfile(bib, work / bib.name)
    for image in figures:
        shutil.copyfile(image, work / image.name)
    subprocess.run([
        latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", source.name,
    ], cwd=work, check=True)
    shutil.copyfile(work / output.name, output)


if __name__ == "__main__":
    main()
