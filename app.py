import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Kupony Dashboard", layout="wide")
st.title("📊 Dashboard Kuponów - William Hill")

data = """Data,Sport,Rozgrywki,Mecz,Rynek,Pewnosc,Stawka,Kurs,Godzina,Status
03.06.2026,Pilka,Friendly,Poland vs Nigeria,Over 2.5 goli,Ryzykowny,0.50,2.00,19:45,WYGRANA
03.06.2026,Tenis,ATP Roland Garros,Berrettini vs Arnaldi,Berrettini to win,Ryzykowny,0.50,1.50,19:15,PRZEGRANA
03.06.2026,Hokej,NHL SCF G2,Vegas vs Carolina,Carolina ML,Ryzykowny,0.50,1.95,01:00,WYGRANA
04.06.2026,Pilka,Friendly,France vs Ivory Coast,BTTS Yes,Ryzykowny,0.50,1.92,20:10,WYGRANA
04.06.2026,Tenis,WTA Roland Garros,Shnaider vs Chwalinska,Chwalinska to win,Ryzykowny,0.50,2.47,15:00,WYGRANA
04.06.2026,Tenis,WTA Roland Garros,Kostyuk vs Andreeva,Kostyuk to win,Ryzykowny,0.50,1.78,11:00,PRZEGRANA
05.06.2026,Tenis,ATP Roland Garros,Zverev vs Mensik,Mensik Set Hcp 1.5,Ryzykowny,0.50,2.25,13:30,PRZEGRANA
05.06.2026,Tenis,ATP Roland Garros,Arnaldi vs Cobolli,Over 3.5 sety,Ryzykowny,0.50,1.65,19:00,VOIDED
05.06.2026,Koszykowka,NBA Finals G2,Spurs vs Knicks,Under 215.5 pkt,Ryzykowny,0.50,1.80,01:30,WYGRANA
06.06.2026,Hokej,NHL SCF G3,Carolina vs Vegas,Vegas ML,Ryzykowny,0.50,1.91,01:00,WYGRANA
07.06.2026,Tenis,ATP Roland Garros finał,Zverev vs Cobolli,Over 36.5 gemów,Ryzykowny,0.50,1.83,14:00,WYGRANA
07.06.2026,Hokej,NHL SCF G4,Carolina vs Vegas,Over 5.5 goli,Ryzykowny,0.50,1.85,01:00,WYGRANA
07.06.2026,Koszykowka,NBA Finals G3,Spurs vs Knicks,Under 215.5 pkt,Ryzykowny,0.50,1.91,01:30,PRZEGRANA
14.06.2026,Pilka,MS 2026 Gr F,Netherlands vs Japan,Under 2.5 goli,Ryzykowna,0.50,1.79,21:00,PRZEGRANA
14.06.2026,Hokej,NHL SCF G6,Carolina @ Vegas,Under 5.5 goli,Ryzykowna,0.50,2.10,01:00,WYGRANA
15.06.2026,Pilka,MS 2026 Gr G,Belgia - Egipt,Under 2.5 goli,Ryzykowna,0.50,1.80,21:00,WYGRANA
16.06.2026,Pilka,MS 2026 Gr J,Argentyna - Algieria,Under 2.5 goli,Ryzykowna,0.50,1.90,02:00,PRZEGRANA
17.06.2026,Pilka,MS 2026 Gr L,Anglia - Chorwacja,England Win To Nil,Ryzykowna,0.50,2.70,wieczorem,PRZEGRANA
19.06.2026,Pilka,MS 2026 Gr C,Scotland vs Morocco,Morocco Wygrywa,Sredni,1.00,1.67,23:00,WYGRANA
20.06.2026,Pilka,MS 2026 Gr E,Germany vs Ivory Coast,BTTS Yes,Sredni,1.00,1.67,21:00,WYGRANA
21.06.2026,Pilka,MS 2026 Gr G,Belgium vs Iran,Over 2.5,Sredni,1.00,1.79,20:00,PRZEGRANA
22.06.2026,Pilka,MS Gr J,Argentina vs Austria,BTTS Yes,Sredni,1.00,1.90,18:00,PRZEGRANA
22.06.2026,Pilka,MS Gr I,France vs Iraq,France -2.5,Ryzykowny,0.50,1.76,22:00,WYGRANA
22.06.2026,Pilka,MS Gr I,Norway vs Senegal,Over 2.5,Sredni,1.00,1.85,01:00,WYGRANA
23.06.2026,Pilka,MS R32,Portugal vs Uzbekistan,Over 2.5,-,0.00,0,-,SKIP
23.06.2026,Pilka,MS R32,England vs Ghana,BTTS Yes,Ryzykowny,0.50,1.83,-,PRZEGRANA
26.06.2026,Pilka,MS Gr I,Norway vs France,Over 2.5,Sredni,1.00,1.50,20:00,WYGRANA
27.06.2026,Pilka,MS Gr K MD3,Colombia vs Portugal,Over 2.5,Ryzykowny,0.50,2.05,00:30,PRZEGRANA
28.06.2026,Pilka,MS R32,South Africa vs Canada,Under 2.5,Ryzykowny,0.50,1.72,20:00,WYGRANA
29.06.2026,Pilka,MS R32,Germany vs Paraguay,Under 2.5,Sredni,1.00,2.05,21:30,WYGRANA
30.06.2026,Pilka,MS R32,Ivory Coast vs Norway,Over 2.5,Sredni,1.00,1.80,18:00,WYGRANA
"""

df = pd.read_csv(StringIO(data))

bank_start = 28.0
wygrane = df[df["Status"] == "WYGRANA"]
przegrane = df[df["Status"] == "PRZEGRANA"]
zysk = (wygrane["Stawka"] * wygrane["Kurs"]).sum() - wygrane["Stawka"].sum() - przegrane["Stawka"].sum()
bank_current = bank_start + zysk

col1, col2, col3, col4 = st.columns(4)
col1.metric("Bank startowy", f"£{bank_start:.2f}")
col2.metric("Bank aktualny", f"£{bank_current:.2f}", f"{zysk:+.2f}")
col3.metric("Liczba kuponów", len(df))
win_rate = len(wygrane) / (len(wygrane) + len(przegrane)) * 100 if (len(wygrane) + len(przegrane)) > 0 else 0
col4.metric("Win rate", f"{win_rate:.0f}%")

st.subheader("Filtry")
c1, c2 = st.columns(2)
sport_filter = c1.multiselect("Sport", options=df["Sport"].unique(), default=df["Sport"].unique())
status_filter = c2.multiselect("Status", options=df["Status"].unique(), default=df["Status"].unique())

df_filtered = df[df["Sport"].isin(sport_filter) & df["Status"].isin(status_filter)]

st.subheader("Wszystkie kupony - czerwiec 2026")
st.dataframe(df_filtered, use_container_width=True)
st.divider()
st.header("🔍 Kalkulator zgodności z zasadami (sekcja B)")
st.caption("Wpisz parametry meczu, a system sprawdzi zgodność z Twoimi zasadami B19, B21, B31.")

c1, c2, c3 = st.columns(3)
sport_input = c1.selectbox("Sport", ["Pilka", "Tenis", "Hokej", "Koszykowka", "Inne"])
kurs_input = c2.number_input("Kurs WH", min_value=1.01, max_value=20.0, value=1.80, step=0.01)
rozgrywki_input = c3.selectbox("Typ rozgrywek", ["Faza grupowa", "Faza pucharowa / KO", "Friendly (towarzyski)", "Liga krajowa", "Inne"])

rynek_input = st.selectbox("Rynek", ["Over/Under", "BTTS", "1X2 / ML", "Handicap", "Inne"])

if st.button("Sprawdź zgodność"):
    powody_skip = []
    ostrzezenia = []

    if kurs_input < 1.20:
        powody_skip.append("B19: kurs poniżej minimalnego progu 1.20 — automatyczny SKIP")

    if rozgrywki_input == "Friendly (towarzyski)" and kurs_input < 1.60:
        powody_skip.append("B21: mecz towarzyski (friendly) z niskim kursem — ryzyko braku motywacji zespołów")

    if rozgrywki_input == "Faza pucharowa / KO" and rynek_input in ["Over/Under", "BTTS"] and kurs_input < 1.85:
        powody_skip.append("B31: rynek Over/BTTS w fazie pucharowej wymaga kursu min. 1.85")

    if kurs_input < 1.50:
        ostrzezenia.append("Niski kurs — sprawdź, czy value jest wystarczające (K3)")

    if powody_skip:
        st.error("❌ SKIP — mecz nie przechodzi kontroli zasad:")
        for p in powody_skip:
            st.write(f"- {p}")
    else:
        st.success("✅ Mecz przechodzi wstępną kontrolę zasad B")
        if ostrzezenia:
            st.warning("⚠️ Uwagi:")
            for o in ostrzezenia:
                st.write(f"- {o}")
        st.info("Pamiętaj: to tylko filtr reguł kursowych. Pełna decyzja wymaga jeszcze procedury K1-K7 (statystyki, źródła, składy).")
