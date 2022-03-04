import pandas as pd
import numpy as np


def dimension_reduction(df, merging_size=4):
    date_list = df.index[::merging_size]

    # merging ( = dimension_reduction )
    _values = df.values\
        .reshape(-1, 4, len(df.columns)).sum(axis=1)
    _values = np.round(_values * 1000) / 1000
    dr_df = pd.DataFrame(_values, index=date_list, columns=df.columns)

    return dr_df
