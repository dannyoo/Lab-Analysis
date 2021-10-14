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

        data[self.metric]= np.where(data[self.metric].isin(["Empty", "\"+\"", "\"-\""]), np.nan, data[self.metric])
        data[self.metric] = data[self.metric].astype(float)