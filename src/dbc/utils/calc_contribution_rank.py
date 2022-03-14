import pandas as pd
import numpy as np


def rank(cont):
    sort_cont = cont.argsort()
    rank_cont = np.zeros(len(cont))

    for _rank in range(1, len(cont) + 1):
        cont_idx = sort_cont[
            _rank - 1
        ]

        # 동률 처리
        _cont = cont[cont_idx]
        exist_eq_cont = np.where(
            cont == _cont
        )[0]
        if len(exist_eq_cont) >= 2:
            for _exist_cont in exist_eq_cont:
                rank_cont[
                    _exist_cont
                ] = _rank

        if rank_cont[cont_idx] == 0:
            rank_cont[
                cont_idx
            ] = _rank

    return rank_cont


def calc_contribution_rank(hc, ci):
    _hc = hc.copy()
    _test = list()

    for col in _hc:
        _hc_info = _hc[col].copy()

        contributions = list()
        for division_round, _ in enumerate(_hc_info):
            conts = ci[division_round][1]
            cont = rank(conts)[int(_)]

            contributions.append(
                cont
            )

        _test.append(contributions.copy())

    contribution_df = pd.DataFrame(_test).T
    contribution_df.columns = hc.columns

    return contribution_df.round()
