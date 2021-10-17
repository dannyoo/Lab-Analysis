'''
column_bias checks if there is column bias based on the two
mirroring replicates. Column bias is indicated by a significant
p value of the two-sample t test conducted on the metrics 
(e.g. absorbance) of the two replicates.
For example, in group1's lay out, B3, C3, D3 and E10, F10, G10
correspond to the same dilution. B-D3 make up the first replicate,
and E-G10 make up the second. The t-test is performed on the absorbance
values of the two replicates.
input: called by get_treatment. See get_treatment for more information.
        data_file: plate data file directory (e.g. treatment_430.csv)
        data_metric: give a name (String) to what is measured (e.g. "absorbance")
        layout_file: plate layout file directory (e.g. plate_layout1.csv)
output: bias_flag, a boolean value showing whether or not there is
        any column bias detected. If the value is True, then the two
        columns that are significantly different will be printed out.
contact Melody for questions or bugs
'''
import numpy as np
from scipy import stats as st
from get_treatment import *

def column_bias(data_file, data_metric, layout_file):
    # filter out only venom treated wells
        #tonly means treatment only
    tonly = get_treatment(data_file, data_metric, layout_file)
    
    # checking column bias
    bias_flag = False # whether there is bias
    dilutions = tonly['dilution'].unique() # get different dilutions
    for item in dilutions:
        # get replicates of one dilution
        all_rep = tonly[tonly['dilution'] == item]

        # group the two replicates by common dilutions
        rep_cols = all_rep['well_column'].unique() # get where replicates are located
            # Checking if the replicate number makes sense
        if (len(rep_cols) > 2):
            raise Exception("Should only have 2 replicates. Detected more replicates.")
        
        rep_1 = all_rep[all_rep['well_column'] == rep_cols[0]]
        rep_2 = all_rep[all_rep['well_column'] == rep_cols[1]]

        # doing t-test between the two replicates
        statistic, pvalue = st.ttest_ind (rep_1['absorbance'], rep_2['absorbance'])
        if(pvalue < 0.05):
            bias_flag = True
            # print(rep_1)
            # print(rep_2)
            print("column", rep_cols[0] + 1, "and column",
            rep_cols[1] + 1, "are significantly different", 
            "\nThe p value is", format(pvalue, '.3f'), 
            "\nThe dilution is", item, 
            "\nindexing of column number starts from 1.")
    
    if (not bias_flag): # if flag is still False
        print("no column bias detected")
    return bias_flag