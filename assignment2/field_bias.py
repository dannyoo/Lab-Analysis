'''
row_bias checks if there exists row bias among all the rows. Row bias
is indicated by a significant p-value resulting from a one-way ANOVA
f-test conducted on the metrics (e.g. absorbance) between rows. 

If the ANOVA indicates the presence of row bias, a t-test is conducted
between every pair of rows to find the actual source(s) of bias. 

input: called by get_treatment. See get_treatment for more information.
        data_file: plate data file directory (e.g. treatment_430.csv)
        data_metric: give a name (String) to what is measured (e.g. "absorbance")
        layout_file: plate layout file directory (e.g. plate_layout1.csv)

output: bias_flag, a boolean value showing whether or not there is
        any column bias detected. If the value is True, then the two
        columns that are significantly different will be printed out.

contact Adi for questions or bugs        
'''
import numpy as np
from scipy import stats as st

def field_bias(plate_data, data_metric):
    # filter out only venom treated wells
        #tonly means treatment only
    tonly = plate_data[plate_data['contents'] == 'Treatment']

    # Debugging:
    # print(tonly.head())

    # checking row bias
    bias_flag = False # whether there is bias

    # Debugging:
    # field_vals = [float(i) for i in range(1, 26)]
    # field_data = [tonly[tonly['field'] == f] for f in field_vals]
    # populations = [field_data[i][data_metric] for i in range(25)]

    # doing the one-way ANOVA test between all rows
    field_cell_counts = tonly.groupby('field')['cell'].apply(list)
    _, pvalue = st.f_oneway(*field_cell_counts)

    # Debugging: 
    # print(pvalue)

    if pvalue < 0.05:
        bias_flag = True

        # pick 10 random wells
        # Get average cell counts in top, bottom, left, right, and middle
        # Display results. For each of the 10 random wells, write which region had most cells

        
    
    if (not bias_flag): # if flag is still False
        print("no row bias detected")
    return bias_flag