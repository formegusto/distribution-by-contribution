import pandas as pd


def remove_anomaly(df, cont_df):
    sum_df = df.sum().round()
    cont_mean_df = cont_df.mean().round()
    anomalies = list()

    for col in df:
        _me = sum_df[col]

        # 1. 총 사용량에서 나보다 높은 가구들만 탐색
        targets = sum_df[sum_df > _me].index
        for t_col in targets:
            _target = sum_df[t_col]
            me_cont = cont_mean_df[col]
            t_cont = cont_mean_df[t_col]

            # 2. 총 사용량이 나보다 높은데도 기여도가 작게 산정된 가구가 있다면,
            if me_cont > t_cont:
                if t_col not in anomalies:
                    anomalies.append(t_col)

    for anomaly in anomalies:
        anomaly_cont = cont_mean_df[anomaly]
        anomaly_kwh = sum_df[anomaly]

        # 3. 현재 기여도 그룹과 다음 기여도 그룹 중에 어디가 더 유사한가?
        now_idx = [_ not in anomalies for _ in df.columns]
        now_cont = sum_df[now_idx][cont_mean_df == anomaly_cont]
        next_cont = sum_df[now_idx][cont_mean_df == (anomaly_cont + 1)]

        # 4. 현재 기여도 그룹의 max 와 다음 기여도 그룹의 min의 오차 계산
        now_err = abs(now_cont.max() - anomaly_kwh)
        next_err = abs(next_cont.min() - anomaly_kwh)

        # 5. 더 가까운 쪽으로 최종 기여도 선정
        if now_err > next_err:
            cont_mean_df[anomaly] += 1

    return pd.DataFrame(cont_mean_df, columns=["contribution"])
