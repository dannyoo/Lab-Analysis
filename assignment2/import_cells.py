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

# cell line: wildtype; group: 2
wildtype2 = CellData("../ld50_data/wildtype_group2.txt", group2)
w2_df = wildtype2.data

# cell line: blast; group: 3
blast3 = CellData("../ld50_data/blast_group3.txt", group3)
b3_df = blast3.data

# %%

# blast cell line group 3 treated cells filter
treated_cells = b3_df[b3_df["contents"] == "Treatment"]
treated_cells.head()

# %%

# counts by well for wildtype
wells_w2 = wildtype2.wellCounts()

# counts by field for wildtype
fields_w2 = wildtype2.fieldCounts()

# %%
