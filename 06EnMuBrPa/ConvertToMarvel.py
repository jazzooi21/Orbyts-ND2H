import pandas as pd
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)

df = pd.read_csv("06EnMuBrPaMhz.txt", delim_whitespace=True)

df["unc"] = df["unc"]*1e6/29979245800 # Convert to wavenumber
df["nu"] = df["nu"]*1e6/29979245800
df["unc2"] = df["unc"]

df2 = pd.read_csv("06EnMuBrPaCM.txt", delim_whitespace=True)
df2["unc"] = abs(df2["unc"])
df2["unc2"] = df2["unc"]
df = pd.concat([df, df2])

inversionMapping = {
    0: "s",
    1: "a",
    2: "s",
    3: "a"
}

df["inv'"] = df["inv'"].map(inversionMapping)
df["inv\""] = df["inv\""].map(inversionMapping)

for i in range(6):
    df[f"n{i + 1}'"] = 0
    df[f"n{i + 1}\""] = 0

df["Source"] = [f"06EnMuBrPa.{i + 1}" for i in range(len(df))] 
df = df[["nu", "unc", "unc2", "n1'", "n2'", "n3'", "n4'", "n5'", "n6'", "J'", "Ka'", "Kc'", "inv'",
"n1\"", "n2\"", "n3\"", "n4\"", "n5\"", "n6\"", "J\"", "Ka\"", "Kc\"", "inv\"", "Source"]]

df = df.sort_values(by=["nu"])
df = df.to_string(header=False, index=False)
marvelFile = "06EnMuBrPa-MARVEL.txt"
with open(marvelFile, "w+") as FileToWriteTo:
    FileToWriteTo.write(df)