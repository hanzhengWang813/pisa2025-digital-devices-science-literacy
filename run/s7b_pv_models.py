# -*- coding: utf-8 -*-
"""
s7b_pv_models.py — 按 10 个 Plausible Value 分别估计核心模型 + Rubin 合并
=====================================================================
替代原先「PV1–PV10 逐行求均值」的做法：
  1) 对 PV1..PV10 各自估计同一模型，得 θ_1..θ_M (M=10)
  2) 对每个 PV 用 80 套 Fay-BRR 复制权重估计抽样方差 U_k
  3) Rubin 合并： Q̄ = mean(θ_k)
                 Ū = mean(U_k)                      (组内/抽样方差)
                 B = var(θ_k)                       (组间/插补方差)
                 T = Ū + (1+1/M)·B
                 df = (M-1)·(1 + Ū/((1+1/M)B))²
输出 output/pv_mediation.json
"""
import os, json
import numpy as np, pandas as pd
import common2 as C

OUT = C.OUT
PVS = ["PV%dSCIE" % i for i in range(1, 11)]
M = len(PVS)
COVS = ["ESCS", "female", "ICTHOME"]
X, M1, M2 = "dev_int_z", "h_leisure", "SELFREG"
YM = "science"

SERIAL_Q = ["a1", "a2", "d21", "b1", "b2", "cp", "ctotal",
            "ind1", "ind2", "ind3", "ind_total"]
PAR_Q = ["a1", "a2", "a3", "d1", "d2", "b1", "b2", "b3", "cp", "ctotal",
         "ind_m1a", "ind_m1b", "ind_m2", "ind_m1a_m2", "ind_m1b_m2", "ind_total"]


def _blocks(d, x, meds, ycol, covs, wcol):
    dd = d[[x] + list(meds) + [ycol] + list(covs) + [wcol]].dropna()
    W = dd[wcol].values.astype(float)
    n = len(dd)
    Xs = C.z(dd[x].values)
    Zm = [C.z(dd[m].values) for m in meds]
    covc = [C._col(dd[c].values) for c in covs]
    Y = dd[ycol].values.astype(float)
    one = np.ones(n)
    U1 = np.column_stack([one, Xs] + covc)
    U2 = np.column_stack([one, Xs, Zm[0]] + covc)
    U3 = np.column_stack([one, Xs, Zm[0], Zm[1]] + covc)
    # 中介方程左侧必须与右侧同尺度（均为 z 标准化），否则得到「每标准差 X → 原始单位 M」的
    # 半标准化系数，a1 等值与论文报告的标准化系数不一致
    return dict(n=n, W=W, U1=U1, U2=U2, U3=U3,
                y1=Zm[0], y2=Zm[1], Y=Y)


def est_serial(d, ycol=YM, wcol="W_FSTUWT", x=X, m1=M1, m2=M2, covs=COVS):
    b = _blocks(d, x, [m1, m2], ycol, covs, wcol)
    sw = np.sqrt(b["W"])
    A = C._solve_w(b["U1"] * sw[:, None], b["y1"] * sw)[0]
    B = C._solve_w(b["U2"] * sw[:, None], b["y2"] * sw)[0]
    D = C._solve_w(b["U3"] * sw[:, None], b["Y"] * sw)[0]
    T = C._solve_w(b["U1"] * sw[:, None], b["Y"] * sw)[0]
    a1, a2, d21 = A[1], B[1], B[2]
    cp, b1, b2 = D[1], D[2], D[3]
    ct = T[1]
    i1, i2, i3 = a1 * b1, a2 * b2, a1 * d21 * b2
    return np.array([a1, a2, d21, b1, b2, cp, ct, i1, i2, i3, i1 + i2 + i3])


def est_parallel(d, ycol=YM, wcol="W_FSTUWT", x=X, m1a="h_leisure", m1b="h_learn", m2=M2, covs=COVS):
    b = _blocks(d, x, [m1a, m1b, m2], ycol, covs, wcol)
    sw = np.sqrt(b["W"])
    n = b["n"]
    dd = d[[x, m1a, m1b, m2, ycol] + list(covs) + [wcol]].dropna()
    Xs = C.z(dd[x].values)
    Za, Zb = C.z(dd[m1a].values), C.z(dd[m1b].values)
    Zm = C.z(dd[m2].values)
    covc = [C._col(dd[c].values) for c in covs]
    one = np.ones(n)
    Ua = np.column_stack([one, Xs] + covc)
    Um = np.column_stack([one, Xs, Za, Zb] + covc)
    Uy = np.column_stack([one, Xs, Za, Zb, Zm] + covc)
    # 中介方程的因变量取 z 标准化值（与 Um/Uy 中的 Za/Zb/Zm 同尺度），
    # 这样 a1/a2/a3/d1/d2 才是论文报告的标准化系数
    ya = Za * sw
    yb = Zb * sw
    ym = Zm * sw
    Y = dd[ycol].values.astype(float)
    A = C._solve_w(Ua * sw[:, None], ya)[0]
    Bv = C._solve_w(Ua * sw[:, None], yb)[0]
    Cc = C._solve_w(Um * sw[:, None], ym)[0]
    D = C._solve_w(Uy * sw[:, None], Y * sw)[0]
    T = C._solve_w(Ua * sw[:, None], Y * sw)[0]
    a1, a2 = A[1], Bv[1]
    a3, d1, d2 = Cc[1], Cc[2], Cc[3]
    cp, b1, b2, b3 = D[1], D[2], D[3], D[4]
    ct = T[1]
    e = [a1 * b1, a2 * b2, a3 * b3, a1 * d1 * b3, a2 * d2 * b3]
    return np.array([a1, a2, a3, d1, d2, b1, b2, b3, cp, ct] + e + [sum(e)])


def brr_var(d, est_fn, ycol, repw=None):
    repw = repw or C.REPW
    th = est_fn(d, ycol, "W_FSTUWT")
    reps = []
    for rc in repw:
        try:
            reps.append(est_fn(d, ycol, rc))
        except Exception:
            continue
    reps = np.array(reps)
    return th, C.BRR_FACTOR * np.nansum((reps - th) ** 2, axis=0)


def rubin(theta, u):
    """theta: (M, K) 点估计；u: (M, K) 抽样方差。返回 Q̄, SE, df, t, p, CI。"""
    theta = np.asarray(theta, float); u = np.asarray(u, float)
    Q = np.nanmean(theta, axis=0)
    U = np.nanmean(u, axis=0)
    B = np.nanvar(theta, axis=0, ddof=1)
    T = U + (1 + 1.0 / M) * B
    SE = np.sqrt(np.maximum(T, 1e-30))
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.where(B > 0, (1 + 1.0 / M) * B / np.maximum(U, 1e-30), np.inf)
    df = np.where(np.isfinite(r), (M - 1) * (1 + 1.0 / r) ** 2, 1e6)
    from scipy import stats
    t = Q / SE
    p = 2 * stats.t.sf(np.abs(t), np.maximum(df, 1))
    tcrit = stats.t.ppf(0.975, np.maximum(df, 1))
    return dict(Q=Q, SE=SE, B=B, U=U, df=df, t=t, p=p,
                ci_lo=Q - tcrit * SE, ci_hi=Q + tcrit * SE)


def run():
    df = C.load()                       # analysis.parquet + 派生变量
    pv = C.read_frame(os.path.join(OUT, "pv"))   # 仅含 PV1..PV10，行序与全样本一致
    df = pd.concat([df.reset_index(drop=True), pv.reset_index(drop=True)], axis=1)
    df = df[df["CNT"] == "QCI"].copy()          # 中国四省（直辖市）样本
    print("中国四省样本:", df.shape, flush=True)

    res = {}
    for tag, est_fn, qnames in [("serial", est_serial, SERIAL_Q),
                                ("parallel", est_parallel, PAR_Q)]:
        TH, UU, THM = [], [], []
        for k, p in enumerate(PVS):
            th, u = brr_var(df, est_fn, p)
            TH.append(th); UU.append(u)
            # PV 均值法（旧做法）对照
            THM.append(est_fn(df, YM, "W_FSTUWT"))
            print(f"  {tag} {p} 完成", flush=True)
        TH = np.array(TH); UU = np.array(UU)
        rb = rubin(TH, UU)
        tm = np.mean(np.array(THM), axis=0)
        # PV 均值法的 BRR 抽样方差
        _, um = brr_var(df, est_fn, YM)
        res[tag] = {
            "quantities": qnames,
            "pooled_pv": {q: dict(est=float(rb["Q"][i]), se=float(rb["SE"][i]),
                                  df=float(rb["df"][i]), t=float(rb["t"][i]),
                                  p=float(rb["p"][i]),
                                  ci=[float(rb["ci_lo"][i]), float(rb["ci_hi"][i])],
                                  between_var=float(rb["B"][i]),
                                  within_var=float(rb["U"][i]),
                                  per_pv_min=float(np.nanmin(TH[:, i])),
                                  per_pv_max=float(np.nanmax(TH[:, i])))
                            for i, q in enumerate(qnames)},
            "mean_pv_practice": {q: dict(est=float(tm[i]), se=float(np.sqrt(um[i])))
                                 for i, q in enumerate(qnames)},
            "n": int(_blocks(df, X,
                             [M1, M2] if tag == "serial" else ["h_leisure", "h_learn", M2],
                             PVS[0], COVS, "W_FSTUWT")["n"]),
        }
        print(f"[{tag}] PV合并完成", flush=True)

    res["meta"] = {
        "M_pv": M, "rep_weights": len(C.REPW), "brr_factor": C.BRR_FACTOR,
        "fay_rho": 0.5, "nboot_note": "间接效应 CI 由 Rubin 合并 SE 给出",
        "vars": {"X": X, "M1": M1, "M2": M2, "Y": "PV1SCIE..PV10SCIE", "covs": COVS},
    }
    with open(os.path.join(OUT, "pv_mediation.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("已写出 output/pv_mediation.json", flush=True)

    for tag in ["serial", "parallel"]:
        print("\n==== %s : PV合并 vs PV均值法 ====" % tag, flush=True)
        for q in res[tag]["quantities"]:
            a = res[tag]["pooled_pv"][q]; b = res[tag]["mean_pv_practice"][q]
            print("%-12s PV合并 est=%9.4f se=%8.4f p=%-8.4f | PV均值 est=%9.4f se=%8.4f"
                  % (q, a["est"], a["se"], a["p"], b["est"], b["se"]), flush=True)


if __name__ == "__main__":
    run()
