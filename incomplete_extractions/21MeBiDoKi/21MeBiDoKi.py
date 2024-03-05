import pandas as pd

fp = r"C:\Users\jazzo\Desktop\academics\work\ORBYTS\data\21MeBiDoKi\nd2h.lin"

with open(fp, 'r') as file:
    # Read the content of the file
    file_content = file.read()
    # Print the content
    #print(file_content)

lines = file_content.split('\n')

# Filter out any lines that start with '!'
filtered_lines = [line for line in lines if not line.startswith('!')]
filtered_lines = [line for line in filtered_lines if line!='']


data_rows = [line.split() for line in filtered_lines]
   
column_names = ["J'", "Ka'", "Kc'", "hyperfine1'", "hyperfine2'", "hyperfine3'", "J\"", "Ka\"", "Kc\"", "hyperfine1\"", "hyperfine2\"", "hyperfine3\"", "nu", "unc"]

df = pd.DataFrame(data_rows, columns=column_names)
df = df.drop_duplicates()
df["temp_label"] = [f"temp.{i + 1}" for i in range(len(df))] 
print(len(df))

df_no_hf = df.drop(["hyperfine1'", "hyperfine2'", "hyperfine3'", "hyperfine1\"", "hyperfine2\"", "hyperfine3\""], axis=1)

#df_str = df_no_hf.to_string(index=False)

#marvelFile = r"c:\Users\jazzo\Desktop\academics\work\ORBYTS\data\21MeBiDoKi\df_removed.txt"
#with open(marvelFile, "w+") as FileToWriteTo:
#    FileToWriteTo.write(df_str)



df_output = pd.DataFrame(columns=["nu", "unc1", "unc2", "n1'", "n2'", "n3'", "n4'", "n5'", "n6'", "J'", "Ka'", "Kc'", "inv'", "n1\"", "n2\"", "n3\"", "n4\"", "n5\"", "n6\"", "J\"", "Ka\"", "Kc\"", "inv\"", "Source"])

zeros = [0 for i in range(len(df_no_hf))]
for label in ["n1'", "n2'", "n3'", "n4'", "n5'", "n6'", "n1\"", "n2\"", "n3\"", "n4\"", "n5\"", "n6\""]:
    df_output[label] = zeros


for label in ["J'", "Ka'", "Kc'", "J\"", "Ka\"", "Kc\"", "nu"]:
    df_output[label] = df_no_hf[label]

df_output["unc1"] = df_no_hf["unc"]
df_output["unc2"] = df_no_hf["unc"]

df_output = df_output.drop_duplicates()

df_output["Source"] = [f"21MeBiDoKi.{i + 1}" for i in range(len(df_output))] 


df_str = df_output.to_string(header=False, index=False)

marvelFile = r"c:\Users\jazzo\Desktop\academics\work\ORBYTS\data\21MeBiDoKi\21MeBiDoKi-MARVEL.txt"
with open(marvelFile, "w+") as FileToWriteTo:
    FileToWriteTo.write(df_str)
