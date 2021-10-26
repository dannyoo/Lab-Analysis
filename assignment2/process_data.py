from collections import defaultdict
import pandas as pd
import numpy as np
import scipy.stats as st
import math

class Plate:
    def __init__(self, filename, metric):
        self.filename = filename
        self.metric = metric
        self.log_metric = self.metric
        self.dictionary_map = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}

        self.__import()
        self.__pivot()
        self.__clean()

    def __import(self):
        self.plate = pd.read_csv(self.filename)

    def __pivot(self):
        self.raw_data = self.plate.melt(id_vars="well_row", var_name="well_column", value_name=self.metric)

    def __clean(self):
        data = self.raw_data.copy()
        data.dropna()
        data["well"] = data.well_row + data.well_column
        data["well_column"] = data["well_column"].astype(int) - 1
        data["well_row"] = data["well_row"].map(self.dictionary_map)

        data = data[["well", "well_row", "well_column", self.metric]]
        self.data = data  

    def logTransform(self):
        self.data[self.log_metric] = np.log(self.data[self.metric])

class LayoutPlate(Plate):
    def __init__(self, filename, metric):
        super().__init__(filename, metric)
        self.__process()

    def __process(self):
        data = self.data
        data["contents"]= np.where(data[self.metric] == "Empty", "Empty", "Treatment")
        data["contents"]= np.where(data[self.metric] == "\"+\"", "Positive", data["contents"])
        data["contents"]= np.where(data[self.metric] == "\"-\"", "Negative", data["contents"])

        data[self.metric]= np.where(data[self.metric].isin(["Empty", "\"+\"", "\"-\""]), 0, data[self.metric])
        data[self.metric] = data[self.metric].astype(float)


        metric_list = data[data.contents == "Treatment"][self.metric].unique().tolist()
        metric_list.sort(reverse=True)
        i = 1
        metric_map = defaultdict()
        metric_map[0.0] = 0
        for elem in metric_list:
            metric_map[elem] = i
            i+=1
        data[self.metric+"_rank"] = data[self.metric].map(metric_map)

class CellData():
    def __init__(self, filename, layout_plate):
        self.filename = filename
        self.layout_plate = layout_plate
        self.rename_dict = {"Well": "well", "Field": "field", "CellNumber": "cell", "ObjectAvgIntenCh1": "h_intensity", "AvgIntenCh3": "pi_intensity"}

        self.__import()
        self.__clean()
        self.__joinGroup()

    def __import(self):
        self.raw_data = pd.read_csv(self.filename)

    def __clean(self):
        data = self.raw_data.copy()
        data.dropna()
        data = data.rename(columns=self.rename_dict)

        self.data = data[["well", "cell", "field", "h_intensity", "pi_intensity"]]  

    def __joinGroup(self):
        data = self.data
        data = pd.merge(self.layout_plate.data, data, on="well")
        self.data = data

    def wellCounts(self):
        count = self.data.copy()
        count = count.groupby(["well", "well_row", "well_column", "contents", "dilution"])['cell'].count().reset_index()
        return count

    def fieldCounts(self):
        count = self.data.copy()
        count = count.groupby(["well", "well_row", "well_column", "field", "contents", "dilution"])['cell'].count().reset_index()
        return count
    
    def getThreshold(self):
        # sets the threshold to be the integer directly above the upperbound
        # of the 95% confidence interval of the negative control
        df = self.data.copy()
        df_pos_pi = df[df["contents"] == "Positive"]["pi_intensity"]
        df_neg_pi = df[df["contents"] == "Negative"]["pi_intensity"]
        neg_95_confInt = st.t.interval(0.95, len(df_neg_pi)-1, loc=np.mean(df_neg_pi), scale=st.sem(df_neg_pi))
        threshold = math.ceil(neg_95_confInt[1])
        # print(threshold)
        # print(len(df_pos_pi[df_pos_pi > threshold])/len(df_pos_pi))
        cutoff_ttest = st.ttest_1samp(df_pos_pi, threshold)
        # set the p value low so we are more sure that the threshold is good
        if(cutoff_ttest.pvalue >= 0.005):
            raise Exception("too much overlap between negative and postive controls' intensities in", self.filename)
        return threshold

    def ld_ratio(self):
        threshold = self.getThreshold()
        df = self.data.copy() # think of it as w2_df
        wells_df = self.wellCounts()
        default = ['alive' for x in range(len(df))]
        df['State'] = default
        df.loc[(df['pi_intensity'] >= threshold), 'State'] = 'dead'
        #create new rows
        wells = wells_df.well.unique()
        wells_df['alive_count'] = [0 for x in range(len(wells_df))]
        wells_df['dead_count']= [0 for x in range(len(wells_df))]
        wells_df['ld_ratio']= [0 for x in range(len(wells_df))]
        # insert data
        for x in wells:
            value_counts = df.loc[(df['well'] == x), 'State'].value_counts()
            alive_count = 0
            dead_count = 0
            ratio = 0
            try:
                alive_count= value_counts.alive
            except:
                print("zero living cells for ", x)

            try:
                dead_count= value_counts.dead
            except:
                print("zero dead cells for ", x)

            try:
                ratio = dead_count/alive_count
            except:
                print("nothing was living")

            wells_df.loc[(wells_df['well'] == x),'alive_count'] = alive_count
            wells_df.loc[(wells_df['well'] == x),'dead_count'] = dead_count
            wells_df.loc[(wells_df['well'] == x),'ld_ratio'] = ratio
        return wells_df
