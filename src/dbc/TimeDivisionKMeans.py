import math as mt
import pandas as pd
import numpy as np
import random as ran
from sklearn.metrics.pairwise import euclidean_distances as euc


class TimeDivisionKMeans:
    def __init__(self, df, size=3):
        self.df = df
        self.size = size
        self.setK()
        self.init_setting()

    def setK(self):
        households_cnt = len(self.df.columns)
        self.K = round(mt.sqrt(households_cnt / 2))

    def init_setting(self):
        self.households_size = len(self.df.columns)
        self.total_size = len(self.df)
        self.division_size = round(self.total_size / self.size)
        self.division_df = [self.df[_:_ + self.size]
                            for _ in range(0, self.total_size, self.size)]

    def run(self, early_stop_cnt=3):
        households_cluster = pd.DataFrame(columns=self.df.columns)
        cluster_info = list()

        for division_round in range(0, self.division_size):
            _round = 0
            _early_stop_cnt = 0
            prev_clusters = None
            clusters = np.zeros(self.households_size)
            K_pattern = np.array([])

            while True:
                # 초기 K 선정
                if _round == 0:
                    init_K = np.array([])
                    K_pattern = np.array([])

                    now_df = self.division_df[division_round].copy().T
                    idxes = now_df.index

                    while len(init_K) < self.K:
                        _K = ran.randint(0, self.households_size - 1)
                        idx = idxes[int(_K)]
                        pattern = now_df.loc[idx].values

                        if (_K not in init_K) and \
                                ~(False if len(K_pattern) == 0 else (K_pattern == pattern).any()):
                            init_K = np.append(init_K, _K)
                            K_pattern = np.append(
                                K_pattern,
                                pattern
                            )

                            K_pattern = K_pattern.reshape(-1, self.size)

                else:
                    next_round_K_pattern = np.array([])

                    for idx in range(0, self.K):
                        next_round_K_pattern = np.append(
                            next_round_K_pattern,
                            (np.round(
                                now_df[clusters == idx].mean() * 1000) / 1000)
                        )
                    next_round_K_pattern = next_round_K_pattern.reshape(
                        -1, self.size)
                    K_pattern = next_round_K_pattern

                clusters = np.array([])

                for idx in now_df.index:
                    try:
                        test = now_df.loc[idx].values
                        test = np.expand_dims(test, axis=0)
                        cluster = euc(test, K_pattern).argmin()
                        clusters = np.append(clusters, cluster)
                    except:
                        print("# Error\ndivision 지점 {}".format(division_round))
                        print(init_K)
                        print(K_pattern)
                        print(prev_clusters)
                        print(test, K_pattern)
                        return

                if (clusters == prev_clusters).all():
                    _early_stop_cnt += 1
                else:
                    _early_stop_cnt = 0

                if _early_stop_cnt >= 3:
                    total_kwh = K_pattern.sum()
                    K_kwh = K_pattern.sum(axis=1)

                    contributions = np.round(K_kwh / total_kwh * 100)

                    households_cluster.loc[division_round] = clusters
                    cluster_info.append([K_pattern, contributions])

                    break

                prev_clusters = clusters
                _round += 1

        self.hc = households_cluster.copy()
        self.ci = cluster_info.copy()

        return (households_cluster, cluster_info)
