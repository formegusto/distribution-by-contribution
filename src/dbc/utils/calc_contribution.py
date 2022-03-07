import pandas as pd


def calc_contribution(hc, ci, df):
    _hc = hc.copy()
    _test = list()

    for col in _hc:
        _hc_info = _hc[col].copy()
        _hc_pattern = df[col].copy()

        contributions = list()
        for division_round, _ in enumerate(_hc_info):
            cont = ci[division_round][1][int(_)]
            _c_pattern = ci[division_round][0][int(_)]
            _h_pattern = _hc_pattern[division_round]

            if _c_pattern.sum() <= _h_pattern.sum():
                contributions.append(
                    cont
                )
            else:
                contributions.append(
                    round(cont / 2)
                )
        _test.append(contributions.copy())

    contribution_df = pd.DataFrame(_test).T
    contribution_df.columns = hc.columns

    return contribution_df.round()
