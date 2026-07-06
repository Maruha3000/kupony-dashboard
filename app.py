import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kupony Dashboard", layout="wide")

st.title("📊 Dashboard Kuponów - William Hill")

data = """Data,Sport,Rozgrywki,Mecz,Rynek,Pewnosc,Stawka,Kurs,Godzina,Status
03.06.2026,Pilka,Friendly,Poland vs Nigeria,Over 2.5 goli,Ryzykowny,0.50,2.00,19:45,WYGRANA
03.06.2026,Tenis,ATP Roland Garros,Berrettini vs Arnaldi,Berrettini to win,Ryzykowny,0.50,1.50,19:15,PRZEGRANA
04.06.2026,Pilka,Friendly,France vs Ivory Coast,BTTS Yes,Ryzykowny,0.50,1.92,20:10,WYGRANA
14.06.2026,Pilka,MS 2026 Gr F,Netherlands vs Japan,Under 2.5 goli,Ryzykowna,0.50,1.80,21:00,PRZEGRANA
19.06.2026,Pilka,MS 2026 Gr C,Scotland vs Morocco,Morocco Wygrywa,Sredni,1.00,1.67,23:00,WYGRANA
20.06.2026,Pilka,MS 2026 Gr E,Germany vs Ivory Coast,BTTS Yes,Sredni,1.00,1.67,21:00,WYGRANA
28.06.2026,Pilka,MS R32,South Africa vs Canada,Under 2.5,Ryzykowny,0.50,1.72,20:00,WYGRANA
29.06.2026,Pilka,MS R32,Germany vs Paraguay,Under 2.5,Sredni,1.00,2.05,21:30,WYGRANA
30.06.2026,Pilka,MS R32,Ivory Coast vs Norway,Over 2.5,Sredni,1.00,1.80,18:00,WYGRANA
"""

from io import StringIO
df = pd.read_csv(StringIO(data))

bank_start = 28.0
wygrane = df[df["Status"] == "WYGRANA"]
przegrane = df[df["Status"] == "PRZEGRANA"]
zysk = (wygrane["Stawka"] * wygrane["Kurs"]).sum() - wygrane["Stawka"].sum() - przegrane["Stawka"].sum()
bank_current = bank_start + zysk

col1, col2, col3 = st.columns(3)
col1.metric("Bank startowy", f"£{bank_start:.2f}")
col2.metric("Bank aktualny", f"£{bank_current:.2f}", f"{zysk:+.2f}")
col3.metric("Liczba kuponów", len(df))

st.subheader("Wszystkie kupony")
st.dataframe(df, use_container_width=True)
