"""Compare regenerated CSV inputs with authorized archived reference copies.

Usage: uv run --locked python source/verify_inputs.py data /path/to/archive/data
No reference data are downloaded or redistributed.
"""
import argparse
from pathlib import Path
import sys
import numpy as np
import pandas as pd


def compare(actual, expected):
    a, b = pd.read_csv(actual), pd.read_csv(expected)
    if set(a.columns) != set(b.columns) or a.shape != b.shape:
        return False, f"schema/shape mismatch: {a.shape} versus {b.shape}"
    a = a[b.columns]
    # Sort both by all columns; retain duplicates and compare missing values.
    a = a.sort_values(list(b.columns), na_position="first").reset_index(drop=True)
    b = b.sort_values(list(b.columns), na_position="first").reset_index(drop=True)
    failures = []
    for col in b.columns:
        if pd.api.types.is_numeric_dtype(a[col]) and pd.api.types.is_numeric_dtype(b[col]):
            equal = np.isclose(a[col].to_numpy(dtype=float), b[col].to_numpy(dtype=float),
                               rtol=1e-9, atol=1e-10, equal_nan=True)
        else:
            equal = (a[col].fillna("<missing>").astype(str) ==
                     b[col].fillna("<missing>").astype(str)).to_numpy()
        if not equal.all():
            failures.append(f"{col}: {int((~equal).sum())} unequal rows")
    return not failures, "; ".join(failures) or "match within tolerance"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("generated", type=Path)
    parser.add_argument("reference", type=Path)
    parser.add_argument("files", nargs="+", help="CSV basenames to compare")
    args = parser.parse_args()
    failed = False
    for name in args.files:
        try:
            ok, message = compare(args.generated / name, args.reference / name)
        except Exception as exc:
            ok, message = False, str(exc)
        print(f"{name}: {'PASS' if ok else 'FAIL'} — {message}")
        failed |= not ok
    sys.exit(int(failed))


if __name__ == "__main__":
    main()
