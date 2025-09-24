import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Mini Energy Allocator", layout="wide")


# ------------------------
# Synthetic data generator
# ------------------------
@st.cache_data
def make_data(hours=48, seed=42):
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2025-01-01", periods=hours, freq="H")

    # PV: bell curve midt på dagen + lidt skyer
    t = np.arange(hours) % 24
    pv_base = np.exp(-0.5 * ((t - 12) / 4.5) ** 2)  # klokkeform
    pv_var = 0.15 * rng.normal(0, 1, hours)
    pv = np.clip(pv_base + pv_var, 0, None) * 5.0  # ca. op til 5 kWh/time

    # H1: morgen + aften peak
    h1 = (
        0.5
        + 0.9 * np.exp(-0.5 * ((t - 7) / 2.2) ** 2)
        + 0.8 * np.exp(-0.5 * ((t - 20) / 2.5) ** 2)
    )
    # H2: mere aften, lidt natlige loads
    h2 = (
        0.4
        + 1.0 * np.exp(-0.5 * ((t - 19) / 2.0) ** 2)
        + 0.2 * (rng.random(hours) > 0.8)  # sporadiske spikes
    )

    df = pd.DataFrame({"PV": pv, "H1_load": h1, "H2_load": h2}, index=idx)
    return df


df = make_data()

st.title("⚡ Mini Energy Allocator (demo)")

# ------------------------
# Controls
# ------------------------
with st.sidebar:
    st.header("Parametre")
    algo = st.radio(
        "Fordelingsalgoritme",
        ["A1: Samtidigt forbrug", "A2: Investeringsandel + redistrib."],
    )
    h1_share = st.slider("H1 investeringsandel", 0.0, 1.0, 0.5, 0.05)
    h2_share = 1.0 - h1_share
    st.write(f"H2 investeringsandel: **{h2_share:.2f}**")

    buy_price = st.number_input("Købspris (DKK/kWh)", 0.0, 10.0, 2.00, 0.10)
    sell_price = st.number_input("Salgspris (DKK/kWh)", 0.0, 10.0, 0.70, 0.10)
    tariff = st.number_input("Tarif (DKK/kWh på køb)", 0.0, 10.0, 0.30, 0.05)


# ------------------------
# Allocation functions
# ------------------------
def alloc_A1(Gt, L1, L2):
    """Proportional efter samtidige loads. Capped til individuelt load."""
    Lsum = L1 + L2
    if Lsum <= 1e-12 or Gt <= 1e-12:
        return 0.0, 0.0, Gt
    # rå allokering proportionalt med load
    a1_raw = Gt * (L1 / Lsum)
    a2_raw = Gt * (L2 / Lsum)
    # cap til respektive loads
    a1 = min(a1_raw, L1)
    a2 = min(a2_raw, L2)
    used = a1 + a2
    surplus = max(Gt - used, 0.0)
    return a1, a2, surplus


def alloc_A2(Gt, L1, L2, w1, w2):
    """Investeringsandel først, overskud redistribueres til dem med rest-load."""
    if Gt <= 1e-12:
        return 0.0, 0.0, 0.0
    # startkvoter
    q1 = Gt * w1
    q2 = Gt * w2
    a1 = min(q1, L1)
    a2 = min(q2, L2)
    R = Gt - (a1 + a2)  # overskud fra dem der ikke kan bruge deres kvote
    if R > 1e-12:
        # fordel rest efter rest-load
        r1 = max(L1 - a1, 0.0)
        r2 = max(L2 - a2, 0.0)
        rsum = r1 + r2
        if rsum > 1e-12:
            a1 += R * (r1 / rsum)
            a2 += R * (r2 / rsum)
        # evt. stadig surplus (hvis ingen rest-load)
    used = a1 + a2
    surplus = max(Gt - used, 0.0)
    return a1, a2, surplus


# ------------------------
# Simulation
# ------------------------
res = []
for t, row in df.iterrows():
    Gt = float(row["PV"])
    L1 = float(row["H1_load"])
    L2 = float(row["H2_load"])

    if algo.startswith("A1"):
        a1, a2, surplus = alloc_A1(Gt, L1, L2)
    else:
        a1, a2, surplus = alloc_A2(Gt, L1, L2, h1_share, h2_share)

    # køb fra net pr. deltager
    k1 = max(L1 - a1, 0.0)
    k2 = max(L2 - a2, 0.0)

    # økonomi (simpel): køb betaler pris + tarif; PV-allokering "værdisættes" til sell_price
    cost1 = k1 * (buy_price + tariff) - a1 * sell_price
    cost2 = k2 * (buy_price + tariff) - a2 * sell_price

    res.append(
        {
            "time": t,
            "PV": Gt,
            "H1_load": L1,
            "H2_load": L2,
            "H1_alloc": a1,
            "H2_alloc": a2,
            "Surplus_to_grid": surplus,
            "H1_grid_buy": k1,
            "H2_grid_buy": k2,
            "H1_cost_DKK": cost1,
            "H2_cost_DKK": cost2,
        }
    )

out = pd.DataFrame(res).set_index("time")

# ------------------------
# Plots
# ------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Produktion og forbrug")
    st.line_chart(out[["PV", "H1_load", "H2_load"]])

with c2:
    st.subheader("Allokering og køb fra net")
    st.line_chart(
        out[["H1_alloc", "H2_alloc", "Surplus_to_grid", "H1_grid_buy", "H2_grid_buy"]]
    )


# ------------------------
# Summary
# ------------------------
def summarize(prefix):
    cols = [c for c in out.columns if c.startswith(prefix)]
    return out[cols].sum()


sum_row = pd.DataFrame(
    {
        "kWh": [
            out["H1_load"].sum(),
            out["H2_load"].sum(),
            out["H1_alloc"].sum(),
            out["H2_alloc"].sum(),
            out["Surplus_to_grid"].sum(),
            out["H1_grid_buy"].sum(),
            out["H2_grid_buy"].sum(),
        ],
        "DKK": [
            out["H1_cost_DKK"].sum(),
            out["H2_cost_DKK"].sum(),
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ],
    },
    index=[
        "H1: Load",
        "H2: Load",
        "H1: PV-allokering",
        "H2: PV-allokering",
        "Fælles: PV-overskud (salg)",
        "H1: Køb fra net",
        "H2: Køb fra net",
    ],
)

st.subheader("Opsummering (periode)")
st.dataframe(sum_row.style.format({"kWh": "{:.1f}", "DKK": "{:.0f}"}))

# Simple fairness-indikator: % af PV der gik til hver
pv_total = out["PV"].sum()
if pv_total > 1e-9:
    share_h1 = out["H1_alloc"].sum() / pv_total
    share_h2 = out["H2_alloc"].sum() / pv_total
else:
    share_h1 = share_h2 = 0.0

st.markdown(
    f"""
**Valgt algoritme:** `{algo}`  
**PV-fordeling (andel af samlet PV):** H1 = **{share_h1:.2%}**, H2 = **{share_h2:.2%}**  
**Parametre:** Køb = {buy_price:.2f} DKK/kWh, Salg = {sell_price:.2f} DKK/kWh, Tarif(køb) = {tariff:.2f} DKK/kWh
"""
)
