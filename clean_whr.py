import pandas as pd

rename_2015_2016 = {
    "Country":"Country","Region":"Region","Happiness Rank":"Rank",
    "Happiness Score":"Happiness_Score","Economy (GDP per Capita)":"GDP_per_Capita",
    "Family":"Social_Support","Health (Life Expectancy)":"Life_Expectancy",
    "Freedom":"Freedom","Trust (Government Corruption)":"Corruption","Generosity":"Generosity",
}

rename_2017 = {
    "Country":"Country","Happiness.Rank":"Rank","Happiness.Score":"Happiness_Score",
    "Economy..GDP.per.Capita.":"GDP_per_Capita","Family":"Social_Support",
    "Health..Life.Expectancy.":"Life_Expectancy","Freedom":"Freedom",
    "Trust..Government.Corruption.":"Corruption","Generosity":"Generosity",
}

rename_2018_2019 = {
    "Country or region":"Country","Overall rank":"Rank","Score":"Happiness_Score",
    "GDP per capita":"GDP_per_Capita","Social support":"Social_Support",
    "Healthy life expectancy":"Life_Expectancy","Freedom to make life choices":"Freedom",
    "Perceptions of corruption":"Corruption","Generosity":"Generosity",
}

CANON = ["Year","Country","Region","Rank","Happiness_Score","GDP_per_Capita",
         "Social_Support","Life_Expectancy","Freedom","Corruption","Generosity"]

def load(path, year, mapping):
    df = pd.read_csv(path)
    df = df.rename(columns=mapping) 
    df["Year"] = year
    return df.reindex(columns=CANON)


df = pd.concat([
    load("2015.csv", 2015, rename_2015_2016),
    load("2016.csv", 2016, rename_2015_2016),
    load("2017.csv", 2017, rename_2017),
    load("2018.csv", 2018, rename_2018_2019),
    load("2019.csv", 2019, rename_2018_2019),
], ignore_index=True)


country_fixes = {
    "North Macedonia":"Macedonia", "Trinidad & Tobago":"Trinidad and Tobago",
    "Taiwan Province of China":"Taiwan", "Hong Kong S.A.R., China":"Hong Kong",
    "North Cyprus":"Northern Cyprus", "Somaliland Region": "Somaliland region",
}
df["Country"] = df["Country"].replace(country_fixes)

region_map = (df.dropna(subset=["Region"])
                .drop_duplicates("Country")
                .set_index("Country")["Region"])
df["Region"] = df["Country"].map(region_map)
df.loc[df.Country == "Gambia", "Region"] = "Sub-Saharan Africa"


years_per_country = df.groupby("Country")["Year"].nunique()
print("Country NOT present in all 5 years:")
print(years_per_country[years_per_country < 5].index.tolist())


df.to_csv("happiness_2015_2019.csv", index=False)

print("rows:", len(df))     
print("years:", sorted(df.Year.unique()))
print(df.isna().sum())
print(df.dtypes)