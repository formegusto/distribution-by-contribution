import pandas as pd
import datetime as dt


def data_preprocessing(xlsx):
    date_df = xlsx[3:][xlsx.columns[1:6]].copy()
    household_df = xlsx[xlsx.columns[7:]]

    date_list = date_df.apply(
        lambda x: dt.datetime(
            x[1], x[2], x[3], x[4], x[5]
        ), axis=1).values

    household_names = household_df.apply(
        lambda x: "{}-{}-{}".format(
            x[0], x[1], x[2]
        )).values

    df = household_df[3:].copy()
    df.index = date_list
    df.columns = household_names

    return df
