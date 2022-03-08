import pandas as pd
import numpy as np


def calc_contribution(hc, ci, df):
    print("new!")
    _hc = hc.copy()
    _test = list()

    for col in _hc:
        _hc_info = _hc[col].copy()
        _hc_pattern = df[col].copy()

        contributions = list()
        for division_round, _ in enumerate(_hc_info):
            conts = ci[division_round][1]
            cont = conts[int(_)]
            _c_pattern = ci[division_round][0][int(_)]
            _h_pattern = _hc_pattern[division_round]

            if _c_pattern.sum() <= _h_pattern.sum():
                upper_conts = conts[conts > cont]
                if len(upper_conts) == 0:
                    contributions.append(
                        cont
                    )
                else:
                    upper_cont = upper_conts[upper_conts.argsort()][0]

                    _conts = np.arange(upper_cont, cont)
                    _conts_max = len(_conts)

                    _percentage = (_h_pattern.sum() -
                                   _c_pattern.sum()) / _c_pattern.sum()
                    _new_cont_idx = round(_conts_max * _percentage)

                    if _new_cont_idx == _conts_max:
                        contributions.append(
                            cont
                        )
                    else:
                        contributions.append(
                            _conts[_new_cont_idx]
                        )
            else:
                lower_conts = conts[conts < cont]
                if len(lower_conts) == 0:
                    contributions.append(
                        cont
                    )
                else:
                    lower_cont = lower_conts[lower_conts.argsort()][::-1][0]
                    _conts = np.arange(lower_cont, cont)
                    _conts_max = len(_conts)
                    _percentage = _h_pattern.sum() / _c_pattern.sum()

                    _new_cont_idx = round(_conts_max * _percentage)
                    if _new_cont_idx == _conts_max:
                        contributions.append(
                            cont
                        )
                    else:
                        contributions.append(
                            _conts[_new_cont_idx]
                        )

        _test.append(contributions.copy())

    contribution_df = pd.DataFrame(_test).T
    contribution_df.columns = hc.columns

    return contribution_df.round()
