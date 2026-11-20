# -*- coding: utf-8 -*-
"""
common2.py — 链式中介研究共享工具
=================================================================
* 读取分析数据
* 加权最小二乘 (WLS)
* 加权 Bootstrap（按权重概率重抽样）— 预加权矩阵 + numpy 索引的快速实现
* Fay-BRR 标准误（80 套复制权重）
* 中文图字体
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

_HERE = os.path.dirname(os.path.abspath(__file__))
# 中间数据目录：默认与本文件同级的 output/，可用环境变量 PISA_OUT2 覆盖
OUT = os.environ.get("PISA_OUT2", os.path.join(_HERE, "output"))
REPW = [f"W_FSTURWT{i}" for i in range(1, 81)]
BRR_FACTOR = 1.0 / 20.0
SEED = 20261001
Z95 = 1.959964


# ---------------------------------------------------------------------------
# 数据
# ---------------------------------------------------------------------------
def read_frame(path_noext, columns=None):
    """读中间数据：<name>.parquet 优先，退回 <name>.pkl（有哪个读哪个）。

    早期版本只写 pickle（未装 pyarrow 时），装好后改写 parquet，
    两者内容等价，因此读入时做一次回退，避免换机器后路径/格式不一致报错。
    """
    for ext in (".parquet", ".pkl"):
        p = path_noext + ext
        if os.path.exists(p):
            df = pd.read_parquet(p) if ext == ".parquet" else pd.read_pickle(p)
            return df[columns] if columns else df
    raise FileNotFoundError(
        "找不到 %s.parquet 或 %s.pkl —— 请先运行 s0_extract.py 生成 analysis，"
        "再运行 s7_pv_extract.py 生成 pv。" % (path_noext, path_noext))


def load():
    return add_derived(read_frame(os.path.join(OUT, "analysis")))


def add_derived(df):
    """补充派生变量：设备使用强度、数字注意调节、数字依赖失调。"""
    df = df.copy()
    df["dev_int_z"] = df[["ICTWKDY", "ICTWKEND"]].apply(lambda c: z(c.values)).mean(axis=1)
    df["sr_attn"] = df[["sr_item1", "sr_item2"]].mean(axis=1)     # 数字注意调节(α≈.76)
    df["sr_dep"] = df[["sr_item3", "sr_item4"]].mean(axis=1)      # 数字依赖失调
    g = df.groupby("CNT")
    for c in ["science", "ICTWKDY", "ICTWKEND", "h_leisure", "h_learn", "SELFREG",
              "sr_attn", "ICTHOME", "ESCS", "leisure_share"]:
        df[c + "_w"] = ((df[c] - g[c].transform("mean")) / g[c].transform("std"))
    df["dev_int_w"] = df[["ICTWKDY_w", "ICTWKEND_w"]].mean(axis=1)   # 组内标准化
    return df


def z(v):
    v = np.asarray(v, float)
    sd = np.nanstd(v)
    return (v - np.nanmean(v)) / sd if sd > 0 else np.zeros_like(v)


def _col(v):
    """连续变量标准化；0/1 变量保持原样。"""
    v = np.asarray(v, float)
    u = np.unique(v[np.isfinite(v)])
    return v if u.size <= 2 else z(v)


# ---------------------------------------------------------------------------
# 加权最小二乘
# ---------------------------------------------------------------------------
def _solve_w(Xw, yw):
    """Xw, yw 已是 sqrt(w) 加权后的矩阵，直接解 WLS。返回 beta, se, t, p。"""
    XtX = Xw.T @ Xw
    k = Xw.shape[1]
    XtX = XtX + 1e-10 * (np.trace(XtX) / k) * np.eye(k)
    beta = np.linalg.solve(XtX, Xw.T @ yw)
    resid = yw - Xw @ beta
    n = Xw.shape[0]
    dof = max(n - k, 1)
    sigma2 = float(resid @ resid) / dof
    se = np.sqrt(np.maximum(np.diag(np.linalg.inv(XtX)) * sigma2, 0))
    t = beta / np.where(se > 0, se, np.nan)
    p = 2 * stats.t.sf(np.abs(t), dof)
    return beta, se, t, p


def wls(X, y, w):
    """常规加权最小二乘（X 含截距列）。"""
    X = np.asarray(X, float); y = np.asarray(y, float); w = np.asarray(w, float)
    ok = np.isfinite(y) & np.isfinite(w) & np.isfinite(X).all(axis=1)
    sw = np.sqrt(w[ok])
    return _solve_w(X[ok] * sw[:, None], y[ok] * sw)


def design(df, preds, covs=None):
    blocks = [np.ones((len(df), 1))]
    for p in preds:
        blocks.append(z(df[p].values).reshape(-1, 1))
    for c in (covs or []):
        blocks.append(_col(df[c].values).reshape(-1, 1))
    return np.hstack(blocks)


# ---------------------------------------------------------------------------
# 加权 Bootstrap 链式中介（快速）
# ---------------------------------------------------------------------------
def _prep(df, x, meds, y, covs, wcol, prestd=False):
    """prestd=True 时假定各列已由调用方标准化（如组内标准化），不再二次标准化。"""
    d = df[[x] + list(meds) + [y] + list(covs) + [wcol]].dropna().copy()
    n = len(d)
    W = d[wcol].values.astype(float)
    sw = np.sqrt(W)
    Xs = d[x].values.astype(float) if prestd else z(d[x].values)
    zmed = [d[m].values.astype(float) if prestd else z(d[m].values) for m in meds]
    raw = [d[m].values.astype(float) for m in meds]
    covc = [d[c].values.astype(float) if prestd else _col(d[c].values) for c in covs]
    Y = d[y].values.astype(float)
    return dict(d=d, n=n, W=W, sw=sw, Xs=Xs, zmed=zmed, raw=raw, covc=covc, Y=Y,
                names=list(meds))


def _mkui(p, extra):
    """返回未加权的设计矩阵：截距 + Xs + extra(标准化中介) + 控制变量。"""
    n = p["n"]
    return np.column_stack([np.ones(n), p["Xs"]] + extra + p["covc"])


def _boot_ci(arr):
    arr = arr[np.isfinite(arr).all(axis=1)] if arr.ndim == 2 else arr[np.isfinite(arr)]
    return np.percentile(arr, [2.5, 97.5], axis=0)


def serial_mediation(df, x, m1, m2, y, covs, wcol="W_FSTUWT", nboot=5000, seed=SEED, prestd=False):
    """
    链式中介（PROCESS Model 6）：
        M1 = a1·X + ...
        M2 = a2·X + d21·M1 + ...
        Y  = c'·X + b1·M1 + b2·M2 + ...
    间接效应：a1b1, a2b2, a1·d21·b2（链式）
    """
    p = _prep(df, x, [m1, m2], y, covs, wcol, prestd=prestd)
    n, sw = p["n"], p["sw"]
    U1 = _mkui(p, [])
    U2 = _mkui(p, [p["zmed"][0]])
    U3 = _mkui(p, [p["zmed"][0], p["zmed"][1]])
    W1, W2, W3 = U1 * sw[:, None], U2 * sw[:, None], U3 * sw[:, None]
    # 中介方程左侧（M1, M2）使用 z 标准化尺度，与右侧设计矩阵（_mkui 已用 p["zmed"]）保持一致
    yw1, yw2, yw3 = p["zmed"][0] * sw, p["zmed"][1] * sw, p["Y"] * sw

    b1_, s1_, t1_, p1_ = _solve_w(W1, yw1)     # a1
    b2_, s2_, t2_, p2_ = _solve_w(W2, yw2)     # a2, d21
    b3_, s3_, t3_, p3_ = _solve_w(W3, yw3)     # c', b1, b2
    bT, sT_, tT_, pT_ = _solve_w(W1, yw3)      # c

    iX, iM1, iM2 = 1, 2, 3
    a1, a2, d21 = b1_[iX], b2_[iX], b2_[iM1]
    cp, bY1, bY2 = b3_[iX], b3_[iM1], b3_[iM2]
    ctot = bT[iX]
    ind1, ind2, ind3 = a1 * bY1, a2 * bY2, a1 * d21 * bY2

    rng = np.random.default_rng(seed)
    pr = p["W"] / p["W"].sum()
    acc = np.full((nboot, 8), np.nan)
    for b in range(nboot):
        ix = rng.choice(n, size=n, replace=True, p=pr)
        try:
            A = _solve_w(W1[ix], yw1[ix])[0]
            B = _solve_w(W2[ix], yw2[ix])[0]
            C = _solve_w(W3[ix], yw3[ix])[0]
            T = _solve_w(W1[ix], yw3[ix])[0]
        except np.linalg.LinAlgError:
            continue
        _a1, _a2, _d21 = A[iX], B[iX], B[iM1]
        _cp, _by1, _by2 = C[iX], C[iM1], C[iM2]
        acc[b] = [_a1 * _by1, _a2 * _by2, _a1 * _d21 * _by2,
                  _a1 * _by1 + _a2 * _by2 + _a1 * _d21 * _by2, _cp, T[iX], _by2, _d21]
    lo, hi = _boot_ci(acc)

    out = {"n": int(n),
           "a1": float(a1), "a1_se": float(s1_[iX]), "a1_p": float(p1_[iX]),
           "a2": float(a2), "a2_se": float(s2_[iX]), "a2_p": float(p2_[iX]),
           "d21": float(d21), "d21_se": float(s2_[iM1]), "d21_p": float(p2_[iM1]),
           "b1": float(bY1), "b1_se": float(s3_[iM1]), "b1_p": float(p3_[iM1]),
           "b2": float(bY2), "b2_se": float(s3_[iM2]), "b2_p": float(p3_[iM2]),
           "cp": float(cp), "cp_se": float(s3_[iX]), "cp_p": float(p3_[iX]),
           "ctotal": float(ctot), "ctotal_se": float(sT_[iX]), "ctotal_p": float(pT_[iX]),
           "ind1": float(ind1), "ind2": float(ind2), "ind3": float(ind3),
           "ind_total": float(ind1 + ind2 + ind3),
           "prop_ind1": float(ind1 / ctot), "prop_ind2": float(ind2 / ctot),
           "prop_ind3": float(ind3 / ctot),
           "prop_ind_total": float((ind1 + ind2 + ind3) / ctot),
           "ind1_ci": [float(lo[0]), float(hi[0])], "ind2_ci": [float(lo[1]), float(hi[1])],
           "ind3_ci": [float(lo[2]), float(hi[2])], "ind_total_ci": [float(lo[3]), float(hi[3])],
           "cp_ci": [float(lo[4]), float(hi[4])], "ctotal_ci": [float(lo[5]), float(hi[5])]}
    return out


def parallel_serial_mediation(df, x, m1a, m1b, m2, y, covs,
                              wcol="W_FSTUWT", nboot=5000, seed=SEED, prestd=False):
    """
    平行—序列中介：
        M1a, M1b = a·X + ...
        M2       = a3·X + d1·M1a + d2·M1b + ...
        Y        = c'·X + b1·M1a + b2·M1b + b3·M2 + ...
    """
    p = _prep(df, x, [m1a, m1b, m2], y, covs, wcol, prestd=prestd)
    n, sw = p["n"], p["sw"]
    Za, Zb, Zm = p["zmed"][0], p["zmed"][1], p["zmed"][2]
    Ua = _mkui(p, [])
    Ub = _mkui(p, [])
    Um = _mkui(p, [Za, Zb])
    Uy = _mkui(p, [Za, Zb, Zm])
    Wa, Wb = Ua * sw[:, None], Ub * sw[:, None]
    Wm, Wy = Um * sw[:, None], Uy * sw[:, None]
    # 中介方程左侧（M1a, M1b, M2）使用 z 标准化尺度，与右侧设计矩阵（_mkui 已用 p["zmed"]）保持一致
    ywa, ywb = p["zmed"][0] * sw, p["zmed"][1] * sw
    ywm, ywy = p["zmed"][2] * sw, p["Y"] * sw

    A = _solve_w(Wa, ywa); B = _solve_w(Wb, ywb)
    C = _solve_w(Wm, ywm); D = _solve_w(Wy, ywy); T = _solve_w(Wa, ywy)

    iX = 1
    a1, a2 = A[0][iX], B[0][iX]
    a3, d1, d2 = C[0][iX], C[0][2], C[0][3]
    cp, b1, b2, b3 = D[0][iX], D[0][2], D[0][3], D[0][4]
    ctot = T[0][iX]

    def effects(a1, a2, a3, d1, d2, b1, b2, b3, cp, ctot):
        e = [a1 * b1, a2 * b2, a3 * b3, a1 * d1 * b3, a2 * d2 * b3]
        return e + [sum(e)] + [cp, ctot]
    full = effects(a1, a2, a3, d1, d2, b1, b2, b3, cp, ctot)

    rng = np.random.default_rng(seed)
    pr = p["W"] / p["W"].sum()
    acc = np.full((nboot, 8), np.nan)
    for b in range(nboot):
        ix = rng.choice(n, size=n, replace=True, p=pr)
        try:
            _A = _solve_w(Wa[ix], ywa[ix])[0]; _B = _solve_w(Wb[ix], ywb[ix])[0]
            _C = _solve_w(Wm[ix], ywm[ix])[0]; _D = _solve_w(Wy[ix], ywy[ix])[0]
            _T = _solve_w(Wa[ix], ywy[ix])[0]
        except np.linalg.LinAlgError:
            continue
        acc[b] = effects(_A[iX], _B[iX], _C[iX], _C[2], _C[3],
                         _D[2], _D[3], _D[4], _D[iX], _T[iX])
    lo, hi = _boot_ci(acc)

    names = ["ind_m1a", "ind_m1b", "ind_m2", "ind_m1a_m2", "ind_m1b_m2",
             "ind_total", "cp", "ctotal"]
    out = {"n": int(n),
           "a1": float(a1), "a1_se": float(A[1][iX]), "a1_p": float(A[3][iX]),
           "a2": float(a2), "a2_se": float(B[1][iX]), "a2_p": float(B[3][iX]),
           "a3": float(a3), "a3_se": float(C[1][iX]), "a3_p": float(C[3][iX]),
           "d1": float(d1), "d1_se": float(C[1][2]), "d1_p": float(C[3][2]),
           "d2": float(d2), "d2_se": float(C[1][3]), "d2_p": float(C[3][3]),
           "b1": float(b1), "b1_se": float(D[1][2]), "b1_p": float(D[3][2]),
           "b2": float(b2), "b2_se": float(D[1][3]), "b2_p": float(D[3][3]),
           "b3": float(b3), "b3_se": float(D[1][4]), "b3_p": float(D[3][4]),
           "cp": float(cp), "cp_se": float(D[1][iX]), "cp_p": float(D[3][iX]),
           "ctotal": float(ctot), "ctotal_se": float(T[1][iX])}
    for i, nm in enumerate(names):
        out[nm] = float(full[i])
        out[nm + "_ci"] = [float(lo[i]), float(hi[i])]
    out["prop_ind_total"] = float(full[5] / ctot) if ctot else np.nan
    return out


# ---------------------------------------------------------------------------
# BRR
# ---------------------------------------------------------------------------
def brr_se(df, est_fn, repw=None):
    repw = repw or REPW
    th = np.asarray(est_fn(df), float)
    reps = []
    for rc in repw:
        try:
            reps.append(np.asarray(est_fn(df, df[rc].values), float))
        except Exception:
            continue
    reps = np.array(reps)
    var = BRR_FACTOR * np.nansum((reps - th) ** 2, axis=0)
    return th, np.sqrt(np.maximum(var, 0))


def setup_font():
    """中文字体：按 Windows / macOS / Linux 常见路径依次查找，找不到就退回默认字体。"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    cands = [
        r"C:/Windows/Fonts/simhei.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for fp in cands:
        if os.path.exists(fp):
            try:
                font_manager.fontManager.addfont(fp)
                plt.rcParams["font.family"] = font_manager.FontProperties(fname=fp).get_name()
                break
            except Exception:
                continue
    plt.rcParams["axes.unicode_minus"] = False
    return plt
