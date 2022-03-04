import pandas as pd


def calc_contribution(hc, ci):
    _hc = hc.copy()
    _test = list()

    for col in _hc:
        _hc_info = _hc[col].copy()
        contributions = [ci[division_round][1]
                         [int(_)] for division_round, _ in enumerate(_hc_info)]
        _test.append(contributions.copy())

    contribution_df = pd.DataFrame(_test).T
    contribution_df.columns = hc.columns

    return contribution_df
