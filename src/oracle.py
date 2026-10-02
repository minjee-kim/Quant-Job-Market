# Print published research by firm.
# Usage: python src/oracle.py

from pathlib import Path

import pandas as pd


def main():
    root = Path(__file__).resolve().parents[1]
    docs = pd.read_csv(root / "data" / "raw" / "documents.csv", parse_dates=["date"])
    docs = docs.sort_values(["firm", "date"])

    for firm, block in docs.groupby("firm", sort=True):
        print(firm)
        themes = ", ".join(block["theme"].drop_duplicates())
        print(f"  themes: {themes}")
        for row in block.itertuples(index=False):
            print(f"  {row.date.date()}  {row.theme}: {row.title}")
        print()


if __name__ == "__main__":
    main()
