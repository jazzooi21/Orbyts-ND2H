import pandas as pd

df_raw = pd.read_csv(r"completed_extractions\75DeHe\75DeHe.csv", dtype = str)

df_output = pd.DataFrame(columns=["nu", "unc", "unc2", "n1'", "n2'", "n3'", "n4'", "n5'", "n6'", "J'", "Ka'", "Kc'", "inv'", "n1\"", "n2\"", "n3\"", "n4\"", "n5\"", "n6\"", "J\"", "Ka\"", "Kc\"", "inv\"", "Source"])


df_output["Source"] = [f"75DeHe.{i + 1}" for i in range(len(df_raw)*2)] 

zeros = [0 for i in range(len(df_raw)*2)]
for label in ["n1'", "n2'", "n3'", "n4'", "n5'", "n6'", "n1\"", "n2\"", "n3\"", "n4\"", "n5\"", "n6\""]:
    df_output[label] = zeros

J_upper = []
Ka_upper = []
Kc_upper = []
J_lower = []
Ka_lower = []
Kc_lower = []
for i in range(43):
    quant_no_upper = df_raw["upper_state"][i].split(" ")
    J_upper.append(quant_no_upper[0])
    J_upper.append(quant_no_upper[0])
    Ka_upper.append(quant_no_upper[1])
    Ka_upper.append(quant_no_upper[1])
    Kc_upper.append(quant_no_upper[2])
    Kc_upper.append(quant_no_upper[2])
    quant_no_lower = df_raw["lower_state"][i].split(" ")
    J_lower.append(quant_no_lower[0])
    J_lower.append(quant_no_lower[0])
    Ka_lower.append(quant_no_lower[1])
    Ka_lower.append(quant_no_lower[1])
    Kc_lower.append(quant_no_lower[2])
    Kc_lower.append(quant_no_lower[2])
    # doubled to account for two possible pairs of inv quantum numbers.

df_output["J'"] = J_upper
df_output["Ka'"] = Ka_upper
df_output["Kc'"] = Kc_upper

df_output["J\""] = J_lower
df_output["Ka\""] = Ka_lower
df_output["Kc\""] = Kc_lower


nu = []
inv_lower = []
inv_upper = []
for i in range(43):
    nu.append(df_raw["lower_freq"][i])
    inv_lower.append('s')
    inv_upper.append('a')
    nu.append(df_raw["upper_freq"][i])
    inv_lower.append('a')
    inv_upper.append('s')

df_output["nu"] = nu
df_output["inv'"] = inv_lower
df_output["inv\""] = inv_upper


uncert = []

for i in range(43*2):
    if df_output["nu"][i][-2] == '.':
        uncert.append(0.1)
    elif df_output["nu"][i][-2].isdigit():
        uncert.append(0.01)

df_output["unc"] = uncert
df_output["unc2"] = uncert

print(df_output)


df_str = df_output.to_string(header=False, index=False)

marvelFile = r"completed_extractions\75DeHe\75DeHe-MARVEL.txt"
with open(marvelFile, "w+") as FileToWriteTo:
    FileToWriteTo.write(df_str)
