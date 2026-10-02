# ============================================================
# Scrape private-markets quant postings and extract fields
# ============================================================
# Information extraction, not a trained model. Eleven postings
# are too few to fit a classifier. The NLP step is:
#   1. HTML to plain text
#   2. sentence segmentation
#   3. requirement vs responsibility labeling
#   4. lexicon match for skills, degree, years, salary
# Pages that block or return a shell are skipped. The curated
# table already in data/raw/ is not overwritten unless --write.

import argparse
import re
from datetime import date
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


SOURCES = [
    {
        "company": "HarbourVest",
        "role": "Quantitative Researcher Private Equity Secondaries",
        "url": "https://harbourvest.wd5.myworkdayjobs.com/en-US/HVP/job/Quantitative-Researcher--Private-Equity-Secondaries_R2034-4",
    },
    {
        "company": "HarbourVest",
        "role": "Quantitative Researcher Private Equity Co-Investments",
        "url": "https://www.tealhq.com/job/quantitative-researcher-private-equity-co-investments_7ea1a6d798627515d54f8cdeebbd19b7e477e",
    },
    {
        "company": "HarbourVest",
        "role": "Quantitative Researcher Evergreen Portfolio Management",
        "url": "https://www.career.com/job/harbourvest-partners/quantitative-researcher-evergreen-portfolio-management-boston-or-toronto/j202505090215094287593",
    },
    {
        "company": "HarbourVest",
        "role": "VP Quantitative Researcher Infrastructure and Real Assets",
        "url": "https://inforcapital.com/jobs/harbourvest-partners-vice-president-quantitative-researcher-infrastructure-real-assets/",
    },
    {
        "company": "BlackRock",
        "role": "Private Markets Quantitative Modeler VP",
        "url": "https://www.linkedin.com/jobs/view/private-markets-quantitative-modeler-vice-president-at-blackrock-4369211771",
    },
    {
        "company": "Blackstone",
        "role": "VP Data Science Private Equity Secondaries",
        "url": "https://www.efinancialcareers.com/jobs-United_States-NY-New_York-Vice_President_Data_Science_-_Private_Equity_Secondaries.id24631940",
    },
    {
        "company": "Ardian",
        "role": "Data Scientist Analyst Secondaries and Primaries",
        "url": "https://revopscareers.com/job/ardian-data-scientist-analyst-secondaries-primaries-san-francisco-california-united-states/",
    },
    {
        "company": "Selby Jennings",
        "role": "Quantitative Researcher Private Investments",
        "url": "https://www.efinancialcareers.com/jobs-USA-IL-Chicago-Quantitative_Researcher_-_Private_Investments.id23749243",
    },
    {
        "company": "Forge Global",
        "role": "Quantitative Researcher",
        "url": "https://job-boards.greenhouse.io/forgeglobal/jobs/5983120004",
    },
    {
        "company": "PitchBook",
        "role": "Director Quantitative Research",
        "url": "https://www.theladders.com/job/director-quantitative-research-pitchbook-seattle-wa_86210440",
    },
    {
        "company": "AssetMetrix",
        "role": "Quantitative Researcher and Methodology Specialist",
        "url": "https://www.xing.com/jobs/muenchen-quantitative-researcher-methodology-specialist-private-capital-analytics-158001691",
    },
]


SKILLS = [
    "python", "sql", "r", "c++", "matlab",
    "time series", "time-series", "bayesian",
    "machine learning", "nlp", "econometrics",
    "monte carlo", "monte-carlo", "backtesting",
    "nowcasting", "optimization", "statistics",
    "valuation", "forecasting", "pandas", "numpy",
]

REQUIREMENT_CUES = (
    "require", "preferred", "what you bring", "qualification",
    "experience", "degree", "phd", "ph.d", "proficiency", "must",
)
RESPONSIBILITY_CUES = (
    "you will", "responsible", "what you will do", "lead", "support",
    "develop", "conduct", "build",
)


def fetch_text(url):
    response = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": "Quant-Job-Market research scrape"},
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(" ", strip=True)


def sentences(text):
    parts = re.split(r"(?<=[.!])\s+|\n+", text)
    return [part.strip() for part in parts if len(part.strip()) > 40]


def label_sentence(sentence):
    lower = sentence.lower()
    if any(cue in lower for cue in REQUIREMENT_CUES):
        return "requirement"
    if any(cue in lower for cue in RESPONSIBILITY_CUES):
        return "responsibility"
    return "other"


def extract_skills(text):
    lower = text.lower()
    found = []
    for skill in SKILLS:
        if skill in lower and skill not in found:
            found.append(skill)
    return found


def extract_degree(text):
    lower = text.lower()
    phd = "phd" in lower or "ph.d" in lower or "ph.d." in lower
    masters = "master" in lower or "m.s" in lower or "ms or" in lower
    bachelors = "bachelor" in lower or "b.a" in lower or "b.s" in lower
    if phd and "required" in lower and "prefer" not in lower[lower.find("phd"):lower.find("phd") + 80]:
        return "PhD required or explicitly invited"
    if phd and (masters or bachelors):
        return "PhD preferred; bachelor's or master's accepted"
    if phd:
        return "PhD mentioned"
    if masters:
        return "master's mentioned"
    if bachelors:
        return "bachelor's mentioned"
    return "not stated"


def extract_years(text):
    hits = re.findall(
        r"(\d+\s*\+?\s*(?:-|to)\s*\d+\s*\+?|\d+\s*\+)\s+years",
        text,
        flags=re.IGNORECASE,
    )
    cleaned = [re.sub(r"\s+", " ", hit).strip() for hit in hits]
    return "; ".join(dict.fromkeys(cleaned)) or "not stated"


def extract_salary(text):
    amounts = re.findall(r"\$\s?([\d,]{3,})", text)
    values = sorted({int(amount.replace(",", "")) for amount in amounts if int(amount.replace(",", "")) >= 50000})
    if len(values) >= 2:
        return f"{values[0]}-{values[-1]}"
    if len(values) == 1:
        return str(values[0])
    return "not published"


def private_markets_stance(text):
    lower = text.lower()
    if "not required" in lower and "private" in lower:
        return "not required"
    if "preferred" in lower and "private" in lower:
        return "preferred"
    if "required" in lower and "private market" in lower:
        return "required"
    return "not stated"


def extract_posting(source):
    text = fetch_text(source["url"])
    labeled = [(label_sentence(sentence), sentence) for sentence in sentences(text)]
    requirements = [sentence for label, sentence in labeled if label == "requirement"]
    return {
        "company": source["company"],
        "role": source["role"],
        "url": source["url"],
        "date_collected": date.today().isoformat(),
        "skills": "; ".join(extract_skills(text)),
        "degree": extract_degree(text),
        "years": extract_years(text),
        "salary": extract_salary(text),
        "private_markets_experience": private_markets_stance(text),
        "n_requirement_sentences": len(requirements),
        "requirement_excerpt": " ".join(requirements[:3])[:500],
        "text_characters": len(text),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write data/raw/private_markets_quant_extracted.csv",
    )
    args = parser.parse_args()

    rows = []
    for source in SOURCES:
        print(source["company"], source["role"])
        try:
            row = extract_posting(source)
        except Exception as exc:
            print("  failed:", type(exc).__name__, exc)
            continue
        print(
            "  skills:", row["skills"] or "none",
            "| years:", row["years"],
            "| chars:", row["text_characters"],
        )
        rows.append(row)

    frame = pd.DataFrame(rows)
    print("\nExtracted rows:", len(frame))
    if args.write and not frame.empty:
        root = Path(__file__).resolve().parents[1]
        output = root / "data" / "raw" / "private_markets_quant_extracted.csv"
        output.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(output, index=False)
        print("Saved", output)


if __name__ == "__main__":
    main()
