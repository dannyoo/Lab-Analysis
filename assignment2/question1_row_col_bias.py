# %%
from process_data import LayoutPlate, CellData
import pandas as pd
from row_bias import *
from column_bias import *

pd.options.mode.chained_assignment = None
# %%
# import layouts
group1 = LayoutPlate("../ld50_data/plate_layout1.csv", "dilution")
group2 = LayoutPlate("../ld50_data/plate_layout2.csv", "dilution")
group3 = LayoutPlate("../ld50_data/plate_layout3.csv", "dilution")

# %%

# cell line: continuous; group: 1
continuous1 = CellData("../ld50_data/continuous_group1.txt", group1)
c1_wellCounts = continuous1.wellCounts()

# cell line: continuous; group: 2
continuous2 = CellData("../ld50_data/continuous_group2.txt", group2)
c2_wellCounts = continuous2.wellCounts()

# cell line: wildtype; group: 3
wildtype3 = CellData("../ld50_data/wildtype_group2.txt", group3)
w3_wellCounts = wildtype3.wellCounts()

# cell line: blast; group: 3
blast3 = CellData("../ld50_data/blast_group3.txt", group3)
b3_wellCounts = blast3.wellCounts()
# %%

# %%
all_wellCounts = [c1_wellCounts, c2_wellCounts, w3_wellCounts, b3_wellCounts]
name = ["countinuous1", "continuous2", "wildtype", "blast"]
for idx in range(len(all_wellCounts)):
    print("\n")
    print("now analyzing row bias of", name[idx])
    r_b = row_bias(all_wellCounts[idx], "cell")
    print("now analyzing column bias of", name[idx])
    c_b = column_bias(all_wellCounts[idx], "cell", name[idx])
    if (not r_b and not c_b):
        print("no row or column bias")

# %%
