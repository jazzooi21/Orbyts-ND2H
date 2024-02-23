import pandas as pd
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)

columnNames = ["nu", "unc", "unc2", "n1'", "n2'", "n3'", "n4'", "n5'", "n6'", 
    "J'", "Ka'", "Kc'", "inv'", "n1\"", "n2\"", "n3\"", "n4\"", "n5\"", "n6\"", 
    "J\"", "Ka\"", "Kc\"", "inv\"", "Source"]

transitions = pd.read_csv("75DeHe-MARVEL-OLD.txt", delim_whitespace=True, names=columnNames)

transitions["Rotational Tag"] = (transitions["J'"].astype(str) + "-" + transitions["Ka'"].astype(str) + 
        "-" + transitions["Ka'"].astype(str) + "-" + transitions["J\""].astype(str) + "-" + 
        transitions["Ka\""].astype(str) + "-" + transitions["Kc\""].astype(str))

# Sort transitions in terms of their pairs and then within those pairs by the transition frequency
transitions.sort_values(by=["Rotational Tag", "nu"])

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

# C2V(M) Group multiplication table
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
    "A1": "s",
    "B1": "a"
}

def findPossibleInversionQuantumNumbers(row, isEven, rotationalSymmetryMap, groupMultiplicationTable, symmetrySelectionRules, inversionSymmetryMapping):
    row["GammaRotational'"] = rotationalSymmetryMap[isEven(row["Ka'"]) + isEven(row["Kc'"])]
    row["GammaRotational\""] = rotationalSymmetryMap[isEven(row["Ka\""]) + isEven(row["Kc\""])]
    # First we take the branch with upper inv state a
    row["inv1'"] = "a"
    row["Gamma1'"] = groupMultiplicationTable[row["GammaRotational'"]]["B1"]
    row["Gamma1\""] = symmetrySelectionRules[row["Gamma1'"]] 
    row["Gamma1Inv\""] = groupMultiplicationTable[row["Gamma1\""]][row["GammaRotational\""]]
    row["inv1\""] = inversionSymmetryMapping[row["Gamma1Inv\""]]
    # Repeat assuming branch with upper inv state s
    row["inv2'"] = "s"
    row["Gamma2'"] = groupMultiplicationTable[row["GammaRotational'"]]["A1"]
    row["Gamma2\""] = symmetrySelectionRules[row["Gamma2'"]] 
    row["Gamma2Inv\""] = groupMultiplicationTable[row["Gamma2\""]][row["GammaRotational\""]]
    row["inv2\""] = inversionSymmetryMapping[row["Gamma2Inv\""]]
    # Determine which of the two branches is the upper and lower component
    if row["inv1'"] == row["inv1\""]: 
        # Case for no change in inversion state ie a -> a
        row["invLower'"] = row["inv1'"]
        row["invLower\""] = row["inv1\""]
        row["invUpper'"] = row["inv2'"]
        row["invUpper\""] = row["inv2\""]
    else: 
        # Case for change in inversion state ie a -> s
        row["invUpper'"] = row["inv1'"]
        row["invUpper\""] = row["inv1\""]
        row["invLower'"] = row["inv2'"]
        row["invLower\""] = row["inv2\""]
    return row

transitions = transitions.parallel_apply(lambda x:findPossibleInversionQuantumNumbers(x, isEven, rotationalSymmetryMap, groupMultiplicationTable, symmetrySelectionRules, inversionSymmetryMapping), result_type="expand", axis=1)
print("\n")
print(transitions.head(20).to_string(index=False, header=False))
# transitions.groupby("Rotational Tag")

# Here we just number all transitions in order. Since they are ordered by rotational assignment
# then by frequency. The lower component shall always be even and upper always odd.
transitions["Branch"] = [i for i in range(len(transitions))]
def selectBranch(row, isEven):
    if isEven(row["Branch"]) == "o":
        row["inv'"] = row["invUpper'"]
        row["inv\""] = row["invUpper\""]
    else: 
        row["inv'"] = row["invLower'"]
        row["inv\""] = row["invLower\""]
    return row

transitions = transitions.parallel_apply(lambda x: selectBranch(x, isEven), result_type="expand", axis=1)
transitions = transitions[columnNames]

transitions = transitions.to_string(header=False, index=False)

marvelFile = "75DeHe-MARVEL-SymmetryAssigned.txt"
with open(marvelFile, "w+") as FileToWriteTo:
    FileToWriteTo.write(transitions)



