# %%
from matplotlib import pyplot as plt
from process_data import *
from import_cells import *
import numpy as np

# %%
# creates 3 columns dead_count, alive_count, & ld_ratio = dead_count / alive count 
ld_c1 = continuous1.ld_ratio()
ld_c2 = continuous2.ld_ratio()
ld_w3 = wildtype3.ld_ratio()
ld_b3 = blast3.ld_ratio()

# %%
#This is setting each live/dead ratio of a cell type based
#on dilution column to a more managable variable
cellLine = [ld_c1, ld_c2, ld_w3, ld_b3]
name = ["countinuous1", "continuous2", "wildtype", "blast"]
for idx in range(len(cellLine)):
    record = []
    toxin_conc = sorted((cellLine[idx])[(cellLine[idx])["contents"] == "Treatment"]["dilution"].unique())
    for dilution in toxin_conc:
        ld_ratio_at_dil = (cellLine[idx])[(cellLine[idx])["dilution"] == dilution].ld_ratio
        ld_ratio_avg = np.mean(ld_ratio_at_dil)
        record.append(ld_ratio_avg)
    # print(record)
    # print("\n")
    # print(toxin_conc)
    plt.plot(toxin_conc, record)
    
    plt.title('LD50 Curve for ' + name[idx])
    plt.xlabel('Toxin Concentration (mg/mL)')
    plt.ylabel('Cell Death (%)')
    plt.ylim([0,0.6])
    plt.xscale("log")
    plt.tight_layout()
    plt.show()

# %%
