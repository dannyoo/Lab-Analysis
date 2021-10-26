# %%
from process_data import LayoutPlate, CellData
import pandas as pd

pd.options.mode.chained_assignment = None
# %%
# import layouts
group1 = LayoutPlate("../ld50_data/plate_layout1.csv", "dilution")
group2 = LayoutPlate("../ld50_data/plate_layout2.csv", "dilution")
group3 = LayoutPlate("../ld50_data/plate_layout3.csv", "dilution")
# %%

# cell line: continuous; group: 1
continuous1 = CellData("../ld50_data/continuous_group1.txt", group1)
c1_df = continuous1.data

# cell line: continuous; group: 2
continuous2 = CellData("../ld50_data/continuous_group2.txt", group2)
c2_df = continuous2.data

# cell line: wildtype; group: 3
wildtype3 = CellData("../ld50_data/wildtype_group2.txt", group3)
w3_df = wildtype3.data

# cell line: blast; group: 3
blast3 = CellData("../ld50_data/blast_group3.txt", group3)
b3_df = blast3.data

# %%

# blast cell line group 3 treated cells filter
treated_cells = b3_df[b3_df["contents"] == "Treatment"]
treated_cells.head()

# %%

# counts by well for wildtype
wells_w3 = wildtype3.wellCounts()

# counts by field for wildtype
fields_w3 = wildtype3.fieldCounts()

# creates 3 columns dead_count, alive_count, & ld_ratio = dead_count / alive count
ld_w3 = wildtype3.ld_ratio()

# %%
# take a look
# print(wells_w3.head())
# print(fields_w3.head())
# print(ld_w3.head())
#ld_w3["well"]
# %%

#Groups columns of live/death ratio by dilution
# dilution_map = {0.22: 1, 0.044: 2, 0.0088: 3, 0.00176: 4, 0.000352: 5, 0.0000704: 6, 0.0000141: 7, 0.00000282: 8}
# ld_w3["dilution_no"] = ld_w3["dilution"].map(dilution_map)
# ld_w3.head()
# %%

