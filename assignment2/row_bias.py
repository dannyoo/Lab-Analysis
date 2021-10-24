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

def row_bias(plate_data, data_metric):
    # filter out only venom treated wells
        #tonly means treatment only
    tonly = plate_data[plate_data['contents'] == 'Treatment']

    # Debugging:
    #print(tonly.head())

    # checking row bias
    bias_flag = False # whether there is bias

    rows = ['B', 'C', 'D', 'E', 'F', 'G']
    row_data = [tonly[tonly['well'].str.contains(r)] for r in rows] # split df by row
    row_b, row_c, row_d, row_e, row_f, row_g = row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5]

    # Debugging:
    #print(row_b.head(), row_c.head(), row_d.head(), row_e.head(), row_f.head(), row_g.head())

    # doing the one-way ANOVA test between all rows
    _, pvalue = st.f_oneway(row_b[data_metric], row_c[data_metric], row_d[data_metric], row_e[data_metric], row_f[data_metric], row_g[data_metric])

    # Debugging: 
    #print(pvalue)
    #pvalue = 0.04

    if pvalue < 0.05:
        bias_flag = True

        # Conduct t-test between every pair of rows, i and j
        for i in range(len(row_data)):
            j = i + 1
            while j < len(row_data):

                row_1 = row_data[i]
                row_2 = row_data[j]
                _, t_pvalue = st.ttest_ind(row_1[data_metric], row_2[data_metric])

                # Debugging:
                # print("row", row_1['well'].values[0][0], "and row", row_2['well'].values[0][0],
                # "\nThe p value is", format(t_pvalue, '.3f'), '\n')
                
                if t_pvalue < 0.05:
                    print("row", row_1['well'].values[0][0], "and row",
                    row_2['well'].values[0][0], "are significantly different", 
                    "\nThe p value is", format(t_pvalue, '.3f'), '\n')

                j += 1
    
    # if (not bias_flag): # if flag is still False
    #     print("no row bias detected")
    return bias_flag