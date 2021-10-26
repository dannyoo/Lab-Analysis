'''
get_treatment filters out and returns well data 
corresponding to venom treatment

input:  data_file: plate data file directory (e.g. treatment_430.csv)
        data_metric: give a name (String) to what is measured (e.g. "absorbance")
        layout_file: plate layout file directory (e.g. plate_layout1.csv)
output: pandas DataFrame object, conatins data_metric of only venom treated wells

notes: layout_metric is always going to be "dilution", so it is not
        set to be a parameter
contact Melody for questions or bugs
'''
from plate import Plate, LayoutPlate
import pandas as pd

def get_treatment(data_file, data_metric, layout_file):
    plate_data = Plate(data_file, data_metric)
    plate_data = plate_data.data # convert to a dataframe object

    # assign the content of each well to wells
    plate_layout = LayoutPlate(layout_file, "dilution")
    plate_data = pd.merge(plate_data, plate_layout.data[["well", "contents", "dilution"]], on="well")
    treatment_only = plate_data[plate_data['contents'] == 'Treatment']
    return treatment_only
