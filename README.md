# World Happiness Report (2015-2019) — Data cleaning for a Tableau dashboard

A Python pipeline that unifies five years of the World Happiness Report into a
single clean source, later used for an interactive Tableau dashboard.

## The problem
The five yearly files have inconsistent schemas:
- Column names change every year (e.g. social support is "Family" in 2015-2017
  and "Social support" in 2018-2019 — same factor, different name).
- Column order is swapped in 2017.
- The geographic Region is missing from 2017 onwards.
- The same countries are spelled differently across years.

## What the script does
1. **Schema unification** — three renaming dictionaries map every year to one
   canonical schema. Renaming is done by name, not by position, so the swapped
   2017 order causes no misalignment.
2. **Country name alignment** — duplicates (e.g. "North Macedonia"/"Macedonia")
   are unified, otherwise they count as distinct entities and break the trends.
3. **Region reconstruction** — the geographic region is remapped onto the years
   that lack it, starting from the years that include it.

## The two decisions on missing data
The rule: fill only verifiable facts, never estimates.
- **Gambia** — missing Region, filled manually ("Sub-Saharan Africa"): a
  geographic fact, not an estimate.
- **United Arab Emirates** — missing corruption value in 2018: left blank.
  Imputing a missing value means fabricating it, not cleaning it.

## Setup & run
1. Clone the repository: git clone https://github.com/elpidioalessandro/world-happiness-tableau.git
2. Enter the project folder: cd world-happiness-tableau
3. Install the dependency: pip install pandas
4. Download the 5 CSVs from [Kaggle](https://www.kaggle.com/datasets/unsdsn/world-happiness) and place them in the project folder
5. Run the script: python clean_whr.py
The script outputs happiness_2015_2019.csv, the clean source used for the Tableau dashboard.
