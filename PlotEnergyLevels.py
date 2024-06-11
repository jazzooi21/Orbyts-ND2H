import matplotlib.pyplot as plt
import pandas as pd 

marvelColumns = ["nu1", "nu2", "nu3a", "nu3b", "nu4a", "nu4b", "J", "Ka", "Kc", "inv", "E", "Uncertainty", "transitions"]

marveleEnergies = pd.read_csv("MarvelEnergyLevels.txt", delim_whitespace=True, names=marvelColumns)

plt.plot(marveleEnergies["J"], marveleEnergies["E"], "b.")
plt.show()