# %%
from plate import Plate, LayoutPlate
import pandas as pd

pd.options.mode.chained_assignment = None

# %%
# load data into plates

# layouts for each group
group1 = LayoutPlate("../ld50_data/plate_layout1.csv", "dilution")
group2 = LayoutPlate("../ld50_data/plate_layout2.csv", "dilution")
group3 = LayoutPlate("../ld50_data/plate_layout3.csv", "dilution")

# treatment test over three wavelength; 430, 600, 630
treatment430 = Plate("../ld50_data/treatment_430.csv", "absorbance")
treatment600 = Plate("../ld50_data/treatment_600.csv", "absorbance")
treatment630 = Plate("../ld50_data/treatment_630.csv", "absorbance")

# cellplate test
cellplate = Plate("../ld50_data/cellplate.csv", "absorbance")

# %%

# access raw data
group1.raw_data.head()

# %%

# access the cleaned dataframe
group1.data.head()

# %%

# log transform treatment plate
treatment630.logTransform
treatment630_log = treatment630.data
treatment630_log.head()
# %%

# merge treatment test with plate layout[well, contents]
treatment630_log = pd.merge(treatment630_log, group1.data[["well", "contents"]], on="well")

treatment630_log.head()
