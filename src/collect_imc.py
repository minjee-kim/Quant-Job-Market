# ============================================================
# Collect current IMC job postings
# ============================================================

import requests
import pandas as pd

from bs4 import BeautifulSoup
from datetime import date
from pathlib import Path


# ------------------------------------------------------------
# 1. Where are the jobs?
# ------------------------------------------------------------

url = "https://boards-api.greenhouse.io/v1/boards/imc/jobs?content=true"


# ------------------------------------------------------------
# 2. Ask the website/API for the data
# ------------------------------------------------------------

response = requests.get(url, timeout=30)

print("HTTP status:", response.status_code)

# Stop the program if the request failed
response.raise_for_status()


# ------------------------------------------------------------
# 3. Convert the JSON response into Python objects
# ------------------------------------------------------------

data = response.json()

print(type(data))
print(data.keys())


# The actual postings are stored in "jobs"
jobs = data["jobs"]

print("Number of jobs:", len(jobs))


# ------------------------------------------------------------
# 4. Look at ONE job first
# ------------------------------------------------------------

first_job = jobs[0]

print(first_job.keys())

print("\nFirst job title:")
print(first_job.get("title"))

print("\nFirst job location:")
print(first_job.get("location"))


# ------------------------------------------------------------
# 5. Turn all jobs into rows
# ------------------------------------------------------------

rows = []

for job in jobs:

    # Job descriptions contain HTML such as <p>, <br>, etc.
    # BeautifulSoup removes those tags and keeps the text.
    html_description = job.get("content", "")

    description = BeautifulSoup(
        html_description,
        "html.parser"
    ).get_text(" ", strip=True)

    rows.append({
        "company": "IMC",
        "title": job.get("title"),
        "location": job.get("location", {}).get("name"),
        "description": description,
        "url": job.get("absolute_url"),
        "date_collected": date.today()
    })


# ------------------------------------------------------------
# 6. Convert rows into a pandas DataFrame
# ------------------------------------------------------------

df = pd.DataFrame(rows)

print("\nFirst cleaned description:")
print(df["description"].iloc[0])

print("\nData dimensions:")
print(df.shape)

print("\nFirst five jobs:")
print(df.head())


# ------------------------------------------------------------
# 7. Save the data
# ------------------------------------------------------------

# Find the root of the GitHub project
project_root = Path(__file__).resolve().parents[1]

output_folder = project_root / "data" / "raw"

# Create the folder if necessary
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / f"imc_jobs_{date.today()}.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nSaved file:")
print(output_file)
