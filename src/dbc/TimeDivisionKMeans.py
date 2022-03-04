import math as mt


class TimeDivisionKMeans:
    def __init__(self, df):
        self.df = df
        self.setK()

    def setK(self):
        households_cnt = len(self.df.columns)

        print("-----[setK info]-----")

        print("data length : {}".format(households_cnt))
        self.K = mt.ceil(mt.sqrt(households_cnt / 2))
        print("K is {}".format(self.K))

        print("---------------------")
