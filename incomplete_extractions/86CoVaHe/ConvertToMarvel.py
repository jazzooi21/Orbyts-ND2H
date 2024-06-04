import pandas as pd
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)

df = pd.read_csv("86CoVaHe.txt", delim_whitespace=True)

# df["unc"] = df["unc"]*1e6/29979245800 # Convert uncertainty to wavenumber
# df["unc2"] = df["unc"]
df["unc"]  = 0.0002
df["unc2"] = 0.0002

# inversionMapping = {
#     0: "s",
#     1: "a"
# }

# df["inv'"] = df["inv'"].map(inversionMapping)
# df["inv\""] = df["inv\""].map(inversionMapping)

for i in range(6):
    if i != 1:
        df[f"n{i + 1}'"] = 0
        df[f"n{i + 1}\""] = 0

df["Source"] = [f"86CoVaHe.{i + 1}" for i in range(len(df))] 
df = df[["nu", "unc", "unc2", "n1'", "n2'", "n3'", "n4'", "n5'", "n6'", "J'", "Ka'", "Kc'", "inv'",
"n1\"", "n2\"", "n3\"", "n4\"", "n5\"", "n6\"", "J\"", "Ka\"", "Kc\"", "inv\"", "Source"]]

df = df.sort_values(by=["nu"])
df = df.to_string(header=False, index=False)
marvelFile = "86CoVaHe-MARVEL.txt"
with open(marvelFile, "w+") as FileToWriteTo:
    FileToWriteTo.write(df)