import math as mt
import pandas as pd
import numpy as np
import random as ran
from sklearn.metrics.pairwise import euclidean_distances as euc


def tss(mean_pattern, df):
    A = np.expand_dims(mean_pattern.values, axis=0)
    tss = 0
    for col in df:
        B = np.expand_dims(df[col].values, axis=0)
        tss += euc(
            B,
            A
        )[0][0] ** 2
    return tss


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

        tss_list = np.array([])
        for division_df in self.division_df:
            mean_pattern = division_df.mean(axis=1)
            tss_list = np.append(tss_list, tss(mean_pattern, division_df))

        self.tss_list = tss_list

    def run(self, early_stop_cnt=3):
        households_cluster = pd.DataFrame(columns=self.df.columns)
        cluster_info = list()

        for division_round in range(0, self.division_size):
            ecv_check = 0
            _round = 0
            _early_stop_cnt = 0

            prev_clusters = None
            clusters = np.zeros(self.households_size)
            K_pattern = np.array([])
            except_K = np.array([])

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
                                ~(False if len(K_pattern) == 0 else (K_pattern == pattern).any()) and \
                        (_K not in except_K):
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

                # wss 계산
                wss = 0
                for idx, cluster in enumerate(clusters):
                    cluster_pattern = np.expand_dims(
                        K_pattern[int(cluster)], axis=0)
                    pattern = np.expand_dims(now_df.iloc[idx].values, axis=0)
                    wss += euc(pattern, cluster_pattern)[0][0] ** 2

                ecv = (1 - (wss / self.tss_list[division_round])) * 100

                if (clusters == prev_clusters).all():
                    _early_stop_cnt += 1
                else:
                    _early_stop_cnt = 0

                if _early_stop_cnt >= early_stop_cnt:
                    if (ecv_check < 20) & (ecv <= 80):
                        # 제일 적게 가지고 있는 K는 다음 턴에서 제외 시키기
                        cluster_cnt = np.array([])
                        for _ in range(0, len(K_pattern)):
                            cluster_cnt = np.append(
                                cluster_cnt, len(np.where(clusters == _)[0]))

                        except_K = np.append(
                            except_K,
                            init_K[cluster_cnt.argmin()]
                        )

                        ecv_check += 1
                        _early_stop_cnt = 0
                        _round = 0
                        continue
                    total_kwh = K_pattern.sum()
                    K_kwh = K_pattern.sum(axis=1)
                    if (((division_round + 1) % 10) == 0) or \
                            ((division_round + 1) == self.division_size):
                        print("{} / {} ==> {}".format(division_round +
                                                      1, self.division_size, ecv))
                    contributions = np.round(K_kwh / total_kwh * 100)
                    households_cluster.loc[division_round] = clusters

                    cluster_info.append([K_pattern, contributions])

                    ecv_check = 0

                    break

                prev_clusters = clusters
                _round += 1

        self.hc = households_cluster.copy()
        self.ci = cluster_info.copy()

        return (households_cluster, cluster_info)
