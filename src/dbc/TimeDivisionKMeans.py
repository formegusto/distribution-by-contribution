import math as mt


class TimeDivisionKMeans:
    def __init__(self, df, size=3):
        self.df = df
        self.size = size
        self.setK()

    def setK(self):
        households_cnt = len(self.df.columns)
        self.K = round(mt.sqrt(households_cnt / 2))

    def init_setting(self):
        print("init_setting func start")
        self.division_round = 0
        self.round = 0

        print("init_setting func end")
