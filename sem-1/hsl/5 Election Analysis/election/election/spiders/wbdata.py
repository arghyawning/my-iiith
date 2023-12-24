import pandas as pd

# def sorting_dataframe():
df = pd.read_csv(
    "wb2006data.csv",
    names=[
        "Sr",
        "Candidate",
        "Constituency",
        "Party",
        "Criminal Case",
        "Education",
        "Total Assets",
        "Approx Assets",
        "Liabilities",
        "Approx Liabilities",
    ],
    delimiter=",",
)
df["Criminal Case"] = pd.to_numeric(df["Criminal Case"])
df = df.sort_values(by=["Criminal Case"])
df.to_csv("wb2006datasorted.csv", index=False)
