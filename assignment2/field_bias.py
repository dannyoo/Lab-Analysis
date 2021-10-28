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

    print("p value = " + str(pvalue))

    if pvalue < 0.05:
        bias_flag = True
        print("Therefore, there is a statistically significant difference between fields.\n")

        # determine which regions within well contain the most cells per field

        wells = ['C3', 'D4', 'E5', 'F6', 'G7', 'F8', 'E9', 'D10']
        top = [21.0, 22.0, 23.0, 24.0, 25.0]
        bottom = [13.0, 14.0, 15.0, 16.0, 17.0]
        left = [17.0, 18.0, 19.0, 20.0, 21.0]
        right = [13.0, 12.0, 11.0, 10.0, 25.0]
        center = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]

        for well in wells:
                well_data = tonly[tonly['well'] == well]

                top_data = well_data[well_data['field'].isin(top)]
                bottom_data = well_data[well_data['field'].isin(bottom)]
                left_data = well_data[well_data['field'].isin(left)]
                right_data = well_data[well_data['field'].isin(right)]
                center_data = well_data[well_data['field'].isin(center)]

                top_avg = top_data['cell'].sum() / 5
                bottom_avg = bottom_data['cell'].sum() / 5
                left_avg = left_data['cell'].sum() / 5
                right_avg = right_data['cell'].sum() / 5
                center_avg = center_data['cell'].sum() / 9

                print("Well: " + well)
                print("Avg cells/field in each region of well:")
                print("\tTop: " + str(top_avg))
                print("\tBottom: " + str(bottom_avg))
                print("\tLeft: " + str(left_avg))
                print("\tRight: " + str(right_avg))
                print("\tCenter: " + str(center_avg) + "\n")


        # Debugging
        # well_data = tonly[tonly['well'] == 'B2']
        # top_data = well_data[well_data['field'] == 21.0]
        # print(top_data)
    
    if (not bias_flag): # if flag is still False
        print("no row bias detected")
    return bias_flag