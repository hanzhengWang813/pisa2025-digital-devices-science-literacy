# -*- coding: utf-8 -*-
"""
s0_extract.py — 链式中介研究数据抽取与派生
=================================================================
路径：数字设备使用 → 使用方式 → 自我调节 → 科学素养

从 PISA 2025 学生公开数据 (CY09_MS_STU_PUF.sav) 抽取相关变量，
清洗 PISA 缺失码，构造派生变量，落盘为 parquet（供后续所有脚本复用）。

产出：output/analysis.parquet
"""
import os, json, time
import numpy as np
import pandas as pd
import pyreadstat

_HERE = os.path.dirname(os.path.abspath(__file__))
# 原始数据：请用环境变量指定，例如
#   export PISA_SAV=/path/to/CY09_MS_STU_PUF.sav
SAV = os.environ.get("PISA_SAV", "")
# 中间数据目录：默认与本文件同级的 output/
OUT = os.environ.get("PISA_OUT2", os.path.join(_HERE, "output"))
# 缺失码取值标签：留空则直接用 .sav 自带的值标签（推荐）
META = os.environ.get("PISA_META", "")
os.makedirs(OUT, exist_ok=True)

PV = [f"PV{i}SCIE" for i in range(1, 11)]
REPW = [f"W_FSTURWT{i}" for i in range(1, 81)]
ST326 = [f"ST326Q0{i}JA" for i in range(1, 7)]

COLS = (
    ["CNT", "W_FSTUWT"] + REPW + PV +
    ["ICTWKDY", "ICTWKEND"] + ST326 +
    ["SELFREG", "ICTREG", "ICTDISTR",
     "ST322Q01JA", "ST322Q02JA", "ST322Q06JA", "ST322Q07JA",
     "IC173Q03JA", "ST097Q06DA", "ST437Q01DA", "ST437Q02DA",
     "EFFSCIE", "JOYSCIE", "STBELSCIE", "ENGSCIPR",
     "PERSEV", "CURIO", "GOALSET", "COGABIL",
     "ESCS", "HOMEPOS", "HISEI", "PAREDINT",
     "ST004D01T", "ST001D01T", "GRADE", "REPEAT", "AGE", "ST022Q01TA",
     "ICTHOME", "ICTSCH", "ICTRES", "ICTOUT", "ICTINFO", "INTICT", "ICTQUAL"]
)

# 值标签自动识别未覆盖时，按变量显式补充的缺失码
OVERRIDE_MISS = {
    "IC173Q03JA": {6.0},          # 6 = 我没有这门课
    "ST437Q01DA": {5.0, 6.0, 7.0, 8.0, 9.0},
    "ST437Q02DA": {5.0, 6.0, 7.0, 8.0, 9.0},
    "ST097Q06DA": {5.0, 6.0, 7.0, 8.0, 9.0},
    "ST322Q01JA": {6.0}, "ST322Q02JA": {6.0}, "ST322Q06JA": {6.0}, "ST322Q07JA": {6.0},
    "REPEAT": {95.0, 96.0, 97.0, 98.0, 99.0},
}
# ST326 使用 1-9 表示时长（6 是有效值，绝不能当缺失）；仅 95-99 为缺失
ST326_MISS = {95.0, 96.0, 97.0, 98.0, 99.0}
# 时长中点（小时/天）：1=0 小时 ... 9=>7 小时
HOUR_MAP = {1: 0.0, 2: 0.5, 3: 1.5, 4: 2.5, 5: 3.5, 6: 4.5, 7: 5.5, 8: 6.5, 9: 7.5}


def load_missing_codes(vlab=None):
    if vlab is None:
        vlab = json.load(open(os.path.join(META, "value_labels_by_variable.json"), encoding="utf-8"))
    pat = ["missing", "skip", "not administered", "invalid", "no response",
           "not applicable"]
    generic = {95, 96, 97, 98, 99, 995, 996, 997, 998, 999}
    out = {}
    for v in vlab:
        m = set()
        for code, lab in vlab[v].items():
            if any(p in str(lab).lower() for p in pat):
                try:
                    m.add(float(code))
                except (ValueError, TypeError):
                    pass
        out[v] = m
    out["_generic"] = generic
    return out


def main():
    t0 = time.time()
    print("reading sav (usecols) ...", flush=True)
    df, meta = pyreadstat.read_sav(SAV, usecols=COLS)
    print("raw shape:", df.shape, "%.1fs" % (time.time() - t0), flush=True)

    miss = load_missing_codes(meta.variable_value_labels if not META else None)
    for c in [x for x in COLS if x != "CNT"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # ---- 缺失处理 ----
    def clean(col):
        if col in ST326:
            s = ST326_MISS
        else:
            s = set(miss.get(col, miss["_generic"]))
            if not s:
                s = set(miss["_generic"])
            s |= OVERRIDE_MISS.get(col, set())
        df.loc[df[col].isin(s), col] = np.nan

    for c in [x for x in COLS if x != "CNT"]:
        clean(c)

    # ---- 科学素养：10 个 PV 均值 ----
    df["science"] = df[PV].mean(axis=1)
    df["female"] = (df["ST004D01T"] == 2).astype(float)

    # ---- 使用方式 ----
    df["use_learn"] = df[[ST326[0], ST326[1], ST326[2]]].mean(axis=1)       # 在校/前后/周末 学习时长
    df["use_leisure"] = df[[ST326[3], ST326[4], ST326[5]]].mean(axis=1)     # 在校/前后/周末 娱乐时长
    df["use_total"] = df[ST326].mean(axis=1)
    # 小时制（中点编码）
    h = np.zeros_like(df[ST326].values, dtype="float64")
    h[:] = np.nan
    for i, q in enumerate(ST326):
        h[:, i] = df[q].map(HOUR_MAP).values
    for i, q in enumerate(ST326):
        df[f"q{i + 1}h"] = h[:, i]          # 6 个情境题的时长编码，供潜在剖面分析
    df["h_learn"] = np.nanmean(h[:, :3], axis=1)
    df["h_leisure"] = np.nanmean(h[:, 3:], axis=1)
    df["h_total"] = np.nanmean(h, axis=1)
    # 娱乐偏向 = 娱乐时长占比
    with np.errstate(invalid="ignore", divide="ignore"):
        df["leisure_share"] = df["h_leisure"] / (df["h_learn"] + df["h_leisure"])
    df.loc[(df["h_learn"] + df["h_leisure"]) <= 0, "leisure_share"] = np.nan

    # ---- 自我调节 ----
    df["sr_offclass"] = df["ST322Q01JA"]
    df["sr_offsleep"] = df["ST322Q02JA"]
    df["sr_pressured"] = df["ST322Q06JA"]
    df["sr_anxious"] = df["ST322Q07JA"]
    df["sr_item1"], df["sr_item2"] = df["sr_offclass"], df["sr_offsleep"]   # 正向
    df["sr_item3"] = 6 - df["sr_pressured"]                                # 反向
    df["sr_item4"] = 6 - df["sr_anxious"]                                  # 反向
    z = lambda s: (s - s.mean()) / s.std()
    df["digit_sr"] = (z(df["sr_item1"]) + z(df["sr_item2"]) +
                      z(df["sr_item3"]) + z(df["sr_item4"])) / 4
    df["digit_sr_z"] = z(df["digit_sr"])
    df["class_distract"] = df["ST097Q06DA"]

    keep = ["CNT", "W_FSTUWT"] + REPW + [
        "science", "female", "ESCS", "HOMEPOS", "HISEI", "PAREDINT",
        "ST001D01T", "GRADE", "REPEAT", "AGE", "ST022Q01TA",
        "ICTWKDY", "ICTWKEND",
        "use_learn", "use_leisure", "use_total",
        "h_learn", "h_leisure", "h_total", "leisure_share",
        "q1h", "q2h", "q3h", "q4h", "q5h", "q6h",
        "SELFREG", "ICTREG", "ICTDISTR",
        "digit_sr", "sr_item1", "sr_item2", "sr_item3", "sr_item4",
        "sr_offclass", "sr_offsleep", "sr_pressured", "sr_anxious",
        "IC173Q03JA", "class_distract", "ST437Q01DA", "ST437Q02DA",
        "EFFSCIE", "JOYSCIE", "STBELSCIE", "ENGSCIPR",
        "PERSEV", "CURIO", "GOALSET", "COGABIL",
        "ICTHOME", "ICTSCH", "ICTRES", "ICTOUT", "ICTINFO", "INTICT", "ICTQUAL",
    ]
    df = df[keep]
    for c in df.columns:
        if c != "CNT":
            df[c] = df[c].astype("float32")

    try:
        out = os.path.join(OUT, "analysis.parquet")
        df.to_parquet(out, index=False)
    except Exception as e:                       # 未装 pyarrow 时退回 pickle
        out = os.path.join(OUT, "analysis.pkl")
        df.to_pickle(out)
        print("未装 pyarrow（%s），改存 pickle" % type(e).__name__, flush=True)
    print("saved ->", out, df.shape, "%.1fs" % (time.time() - t0), flush=True)

    for e in ["QCI", "USA", "FIN", "KOR", "HKG"]:
        s = df[df["CNT"] == e]
        print(f"  {e}: n={len(s)} | science={s['science'].notna().sum()} "
              f"| SELFREG={s['SELFREG'].notna().sum()} | ICTWKDY={s['ICTWKDY'].notna().sum()} "
              f"| sr_attn={s['sr_item1'].notna().sum()} | h_total={s['h_total'].notna().sum()} "
              f"| q1h={s['q1h'].notna().sum()}")
    print("列数:", df.shape[1], "| 含使用方式剖面题:", all(f"q{i}h" in df.columns for i in range(1, 7)))


if __name__ == "__main__":
    if not SAV:
        raise SystemExit("请先设置环境变量 PISA_SAV，指向 PISA 2025 学生问卷文件\n"
                         "  export PISA_SAV=/path/to/CY09_MS_STU_PUF.sav")
    if not os.path.exists(SAV):
        raise SystemExit("PISA_SAV 指向的文件不存在：%s" % SAV)
    main()
