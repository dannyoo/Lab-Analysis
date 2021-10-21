import pandas as pd
import numpy as np

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
    
    def ld_ratio(self, threshold=617.3261022178222):
        # this threshold value assumes what we did here: ./analysis.ipynb
        # I believe the threshold value applies to all dataframes that we get from that machine this semester ;p
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
