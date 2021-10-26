## Just an fork of the analysis showing how to do the notebook in vs code on a python file.

# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np

cells = pd.read_csv('data.csv')
cells.head()


# %%
pi = cells[['Well','ObjectAvgIntenCh1', 'AvgIntenCh3']].copy()
pi = pi.rename(columns={"Well": "Well",
                        "ObjectAvgIntenCh1": "h_intensity",
                        "AvgIntenCh3": "pi_intensity"})
pi.head()


# %%
negativeControl = pi.loc[(pi['Well'] == 'B11') |(pi['Well'] == 'C11')| (pi['Well'] == 'D11') | (pi['Well'] == 'E2') | (pi['Well'] == 'F2') | (pi['Well'] == 'G2')]
negativeControl.std()
threshold = 3*negativeControl.pi_intensity.std()
print(threshold)


# %%
positiveControl = cells.loc[(cells['Well']=='B2') | (cells['Well']=='C2')| (cells['Well']=='D2')|(cells['Well']=='E11') |(cells['Well']=='F11')|(cells['Well']=='G11')]
pos_ctrl_int_pi = positiveControl['AvgIntenCh3']


# %%
import scipy.stats as st
threshold_ttest = st.ttest_1samp(pos_ctrl_int_pi, threshold)
if(threshold_ttest.pvalue > 0.05):
    raise Exception("too much overlap between negative and postive controls' intensities")


# %%
default = ['alive' for x in range(len(pi))]
pi['State'] = default
pi.loc[(pi['pi_intensity'] >= threshold), 'State'] = 'dead'
pi.head()


