import pandas as pd
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)

columnNames = ["nu", "unc", "unc2", "n1'", "n2'", "n3'", "n4'", "n5'", "n6'", 
    "J'", "Ka'", "Kc'", "inv'", "n1\"", "n2\"", "n3\"", "n4\"", "n5\"", "n6\"", 
    "J\"", "Ka\"", "Kc\"", "inv\"", "Source"]
# transitionsDeHe = pd.read_csv("75DeHe-MARVEL.txt", delim_whitespace=True, names=columnNames)
transitionsDeHe = pd.read_csv("75DeHe-MARVEL-SymmetryAssigned.txt", delim_whitespace=True, names=columnNames)
transitionsCaDiFuTa = pd.read_csv("../22CaDiFuTa/22CaDiFuTa-MARVEL.txt", delim_whitespace=True, names=columnNames)
print(transitionsDeHe.to_string(index=False))
def generateTag(row):
    row["Tag"] = (str(row["J'"]) + "-" + str(row["Ka'"]) + "-" + str(row["Kc'"]) 
            + "-" + row["inv'"] + "-" + str(row["J\""]) + "-" + str(row["Ka\""]) 
            + "-" + str(row["Kc\""]) + "-" + row["inv\""] 
    )
    return row

transitionsDeHe = transitionsDeHe.parallel_apply(lambda x:generateTag(x), result_type="expand", axis=1)
transitionsCaDiFuTa = transitionsCaDiFuTa.parallel_apply(lambda x:generateTag(x), result_type="expand", axis=1)

transitionsDeHe["nu"] = transitionsDeHe["nu"]*1e6/29979245800 # Make sure units of sources are consistent for the check
def compareEnergies(row, transitionsToCompareAgainst):
    row["Error"] = False 
    transitionsToCompareAgainst = transitionsToCompareAgainst[transitionsToCompareAgainst["Tag"] == row["Tag"]]
    if len(transitionsToCompareAgainst) == 1:
        transitionsToCompareAgainst = transitionsToCompareAgainst.squeeze()
        row["Diff"] = abs(transitionsToCompareAgainst["nu"] - row["nu"])
        row["Match"] = transitionsToCompareAgainst["nu"]
        if row["Diff"] > 0.000001:
            row["Error"] = True
    else:
        row["Diff"] = -1000
        row["Match"] = -1
        row["Error"] = True
    return row

transitionsDeHe = transitionsDeHe.parallel_apply(lambda x:compareEnergies(x, transitionsCaDiFuTa), result_type="expand", axis=1)
print(transitionsDeHe[["Diff", "Error", "Tag", "Source", "nu"]].to_string(index=False, header=False))
print(len(transitionsDeHe[transitionsDeHe["Error"]]))
print(transitionsDeHe[transitionsDeHe["Error"]][["Diff", "Error", "Tag", "Source", "nu", "Match"]].to_string(index=False, header=False))