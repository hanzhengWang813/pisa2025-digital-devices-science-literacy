# -*- coding: utf-8 -*-
"""抽取 PV1SCIE-PV10SCIE，并与 analysis.parquet 逐行对齐校验。"""
import os, sys
import numpy as np, pandas as pd, pyreadstat

_HERE = os.path.dirname(os.path.abspath(__file__))
SAV = os.environ.get("PISA_SAV", "")     # 指向 CY09_MS_STU_PUF.sav
OUT = os.environ.get("PISA_OUT2", os.path.join(_HERE, "output"))
if not SAV:
    sys.exit("请先设置环境变量 PISA_SAV 指向 CY09_MS_STU_PUF.sav")
PVS = ["PV%dSCIE" % i for i in range(1, 11)]

def main():
    cols = PVS + ["CNT", "W_FSTUWT"]
    print("读取列:", cols, flush=True)
    df, meta = pyreadstat.read_sav(SAV, usecols=cols)
    print("读入:", df.shape, flush=True)

    sys.path.insert(0, _HERE)
    import common2 as C
    base = C.read_frame(os.path.join(OUT, "analysis"), ["CNT", "W_FSTUWT"])
    print("基线:", base.shape, flush=True)

    assert len(df) == len(base), ("行数不一致", len(df), len(base))
    c1 = df["CNT"].astype(str).values
    c2 = base["CNT"].astype(str).values
    same_cnt = bool((c1 == c2).all())
    same_w = bool(np.allclose(df["W_FSTUWT"].values, base["W_FSTUWT"].values, equal_nan=True))
    print("CNT 逐行一致:", same_cnt, "| W_FSTUWT 逐行一致:", same_w, flush=True)
    if not (same_cnt and same_w):
        n = int((c1 != c2).sum())
        print("!! 行序不一致，差异行数:", n, flush=True)
        sys.exit(2)

    pv = df[PVS].astype("float64")
    print("PV 缺失率:")
    print((pv.isna().mean() * 100).round(2).to_string(), flush=True)
    print("PV 间相关(前3):")
    print(pv[PVS[:3]].corr().round(4).to_string(), flush=True)

    try:
        pv.to_parquet(os.path.join(OUT, "pv.parquet"), index=False)
        print("已写出 output/pv.parquet", pv.shape, flush=True)
    except Exception as e:                       # 未装 pyarrow 时退回 pickle
        pv.to_pickle(os.path.join(OUT, "pv.pkl"))
        print("未装 pyarrow（%s），已写出 output/pv.pkl" % type(e).__name__, pv.shape, flush=True)

if __name__ == "__main__":
    main()
