import pandas as pd
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)

columns = ["J'", "Ka'", "Kc'", "J\"", "Ka\"", "Kc\"", "inv'", "inv\"", "nu"]
df = pd.read_csv("88FuDiJo.txt", delim_whitespace=True, names=columns)
df2 = pd.read_csv("88FuDiJoMHz.txt", delim_whitespace=True, names=columns)
df2["nu"] = df2["nu"]*1e6/29979245800
df = pd.concat([df, df2])

df["unc"] =  0.00025
df["unc2"] = 0.00025

inversionMapping = {
    0: "s",
    1: "a"
}

df["inv'"] = df["inv'"].map(inversionMapping)
df["inv\""] = df["inv\""].map(inversionMapping)

for i in range(6):
    df[f"n{i + 1}'"] = 0
    df[f"n{i + 1}\""] = 0

df["Source"] = [f"88FuDiJo.{i + 1}" for i in range(len(df))] 
df = df[["nu", "unc", "unc2", "n1'", "n2'", "n3'", "n4'", "n5'", "n6'", "J'", "Ka'", "Kc'", "inv'",
"n1\"", "n2\"", "n3\"", "n4\"", "n5\"", "n6\"", "J\"", "Ka\"", "Kc\"", "inv\"", "Source"]]


def isEven(value):
    if value%2 == 0:
        return "e"
    else:
        return "o"

# Symmetry mapping from Bunker and Jensen 1998
rotationalSymmetryMap = {
    "ee": "A1",
    "oo": "A2",
    "eo": "B1",
    "oe": "B2"
}

groupMultiplicationTable = {}
groupMultiplicationTable["A1"] = {"A1": "A1", "A2": "A2", "B1": "B1", "B2": "B2"}
groupMultiplicationTable["A2"] = {"A1": "A2", "A2": "A1", "B1": "B2", "B2": "B1"}
groupMultiplicationTable["B1"] = {"A1": "B1", "A2": "B2", "B1": "A1", "B2": "A2"}
groupMultiplicationTable["B2"] = {"A1": "B2", "A2": "B1", "B1": "A2", "B2": "A1"}

symmetrySelectionRules = {
    "A1": "A2",
    "A2": "A1",
    "B1": "B2",
    "B2": "B1"
}

# Symmetry assignments for inversion states
inversionSymmetryMapping = {
    "s": "A1",
    "a": "B1"
}

def checkTransitions(row):
    row["Check"] = False
    if row["J'"] != (row["Ka'"] + row["Kc'"]):
         if row["J'"] != (row["Ka'"] + row["Kc'"] - 1):
             row["Check"] = True
    if row["J\""] != (row["Ka\""] + row["Kc\""]):
         if row["J\""] != (row["Ka\""] + row["Kc\""] - 1):
             row["Check"] = True
    row["Gamma'"] = groupMultiplicationTable[rotationalSymmetryMap[isEven(row["Ka'"]) + isEven(row["Kc'"])]][inversionSymmetryMapping[row["inv'"]]]
    row["Gamma\""] = groupMultiplicationTable[rotationalSymmetryMap[isEven(row["Ka\""]) + isEven(row["Kc\""])]][inversionSymmetryMapping[row["inv\""]]]
    if row["Gamma\""] != symmetrySelectionRules[row["Gamma'"]]:
        row["Check"] = True
    return row

df = df.parallel_apply(lambda x:checkTransitions(x), result_type="expand", axis=1)
print(df[df["Check"]].to_string(index=False, header=False))


df = df[["nu", "unc", "unc2", "n1'", "n2'", "n3'", "n4'", "n5'", "n6'", "J'", "Ka'", "Kc'", "inv'",
"n1\"", "n2\"", "n3\"", "n4\"", "n5\"", "n6\"", "J\"", "Ka\"", "Kc\"", "inv\"", "Source"]]
df = df.sort_values(by=["nu"])
df = df.to_string(header=False, index=False)
marvelFile = "88FuDiJo-MARVEL.txt"
with open(marvelFile, "w+") as FileToWriteTo:
    FileToWriteTo.write(df)