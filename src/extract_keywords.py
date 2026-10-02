# Count private-markets research phrases in a text file.
# The phrase list is data/raw/research_keywords.csv.
# Usage: python src/extract_keywords.py path/to/notes.txt

import sys
from pathlib import Path

import pandas as pd


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python src/extract_keywords.py <text file>")

    root = Path(__file__).resolve().parents[1]
    lexicon = pd.read_csv(root / "data" / "raw" / "research_keywords.csv")
    text = Path(sys.argv[1]).read_text(encoding="utf-8").lower()

    rows = []
    for phrase, category in zip(lexicon["phrase"], lexicon["category"]):
        rows.append({
            "phrase": phrase,
            "category": category,
            "count": text.count(phrase.lower()),
        })

    counts = pd.DataFrame(rows)
    counts = counts[counts["count"] > 0].sort_values("count", ascending=False)
    print(counts.to_string(index=False))


if __name__ == "__main__":
    main()
