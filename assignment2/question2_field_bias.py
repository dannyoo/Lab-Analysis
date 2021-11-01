# %%
from field_bias import field_bias
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
c1_fieldCounts = continuous1.fieldCounts()

# cell line: continuous; group: 2
continuous2 = CellData("../ld50_data/continuous_group2.txt", group2)
c2_fieldCounts = continuous2.fieldCounts()

# cell line: wildtype; group: 3
wildtype3 = CellData("../ld50_data/wildtype_group2.txt", group3)
w3_fieldCounts = wildtype3.fieldCounts()

# cell line: blast; group: 3
blast3 = CellData("../ld50_data/blast_group3.txt", group3)
b3_fieldCounts = blast3.fieldCounts()
# %%

# %%
all_fieldCounts = [c1_fieldCounts, c2_fieldCounts, w3_fieldCounts, b3_fieldCounts]
name = ["countinuous1", "continuous2", "wildtype", "blast"]

for idx in range(len(all_fieldCounts)):
    print("\n")
    print("now analyzing field bias of", name[idx])
    f_b = field_bias(all_fieldCounts[idx], "cell", name[idx])
    if (not f_b):
        print("no field bias")

# f_b = field_bias(all_fieldCounts[0], "cell")
if (not f_b):
    print("no field bias")

# %%
