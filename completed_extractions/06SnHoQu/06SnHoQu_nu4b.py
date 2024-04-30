import pandas as pd

df_raw = pd.read_csv(r"C:\Users\jazzo\Desktop\academics\work\ORBYTS\data\06SnHoQu\06SnHoQu-4nub.csv", dtype = str)


df_output = pd.DataFrame(columns=["nu", "unc1", "unc2", "n1'", "n2'", "n3a'", "n3b'", "n4a'", "n4b'", "J'", "Ka'", "Kc'", "inv'", "n1\"", "n2\"", "n3a\"", "n3b\"", "n4a\"", "n4b\"", "J\"", "Ka\"", "Kc\"", "inv\"", "Source"])


df_output["Source"] = [f"06SnHoQu.{i + 1}" for i in range(len(df_raw))] 

zeros = [0 for i in range(len(df_raw))]
for label in ["n1'", "n2'", "n3a'", "n3b'", "n4a'", "n1\"", "n2\"", "n3a\"", "n3b\"", "n4a\"", "n4b\""]:
    df_output[label] = zeros

ones = [1 for i in range(len(df_raw))]
df_output["n4b'"] = ones

df_output["nu"] = df_raw["nu"]

df_output["inv\""] = df_raw["inv"]
df_output["J\""] = df_raw["J"]
df_output["Ka\""] = df_raw["Ka"]
df_output["Kc\""] = df_raw["Kc"]

df_output["inv'"] = df_raw["inv'"]
df_output["J'"] = df_raw["J"]
df_output["Ka'"] = df_raw["K'a"]
df_output["Kc'"] = df_raw["K'c"]

print(df_output)


uncert = [0.0001 for i in range(len(df_raw))]
df_output["unc1"] = uncert
df_output["unc2"] = uncert

print(df_output)


df_str = df_output.to_string(header=False, index=False)

marvelFile = r"c:\Users\jazzo\Desktop\academics\work\ORBYTS\data\06SnHoQu\06SnHoQu-MARVEL.txt"
with open(marvelFile, "w+") as FileToWriteTo:
    FileToWriteTo.write(df_str)