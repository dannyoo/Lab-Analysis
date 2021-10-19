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
continuous1 = CellData("../ld50_data/continuous_group1.txt")
continuous1.joinGroup(group1)
c1_df = continuous1.data

# cell line: continuous; group: 2
continuous2 = CellData("../ld50_data/continuous_group2.txt")
continuous2.joinGroup(group2)
c2_df = continuous2.data

# cell line: wildtype; group: 2
wildtype2 = CellData("../ld50_data/wildtype_group2.txt")
wildtype2.joinGroup(group2)
w2_df = wildtype2.data

# cell line: blast; group: 3
blast3 = CellData("../ld50_data/blast_group3.txt")
blast3.joinGroup(group3)
b3_df = blast3.data

# %%

# blast cell line group 3 treated cells filter
treated_cells = b3_df[b3_df["contents"] == "Treatment"]
treated_cells.head()
