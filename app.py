import streamlit as st
import pandas as pd
from io import StringIO
import csv
import os
from datetime import datetime
import requests
import base64
st.set_page_config(page_title="Kupony Dashboard", layout="wide")
st.title("📊 Garnek z kapustą")

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

st.subheader("💰 Kalkulator bezpiecznej stawki")

st.write("Wpisz swój aktualny bank, a system podliczy bezpieczną stawkę na podstawie zasad ochrony kapitału.")

bank_bazowy = 28.0
stawki_bazowe = {"Pewny": 1.50, "Średni": 1.00, "Ryzykowny": 0.50}

c6, c7 = st.columns(2)
bank_uzytkownika = c6.number_input("Twój aktualny bank (GBP)", min_value=1.0, value=28.0, step=1.0)
pewnosc_input = c7.selectbox("Poziom pewności zakładu", ["Pewny", "Średni", "Ryzykowny"])

if st.button("Policz stawkę"):
    wspolczynnik = bank_uzytkownika / bank_bazowy
    stawka_rekomendowana = round(stawki_bazowe[pewnosc_input] * wspolczynnik, 2)
    procent_banku = round((stawka_rekomendowana / bank_uzytkownika) * 100, 1)

    st.success(
        f"Przy banku {bank_uzytkownika:.2f} GBP i pewności '{pewnosc_input}', "
        f"bezpieczna stawka to około **{stawka_rekomendowana} GBP** "
        f"(to około {procent_banku}% Twojego banku)."
    )
    st.caption(
        "To przeliczenie bazuje na zasadzie, że przy banku 28 GBP stawki wynoszą: "
        "Pewny 1.50 GBP, Średni 1.00 GBP, Ryzykowny 0.50 GBP — czyli od 1.8% do 5.4% banku, "
        "zależnie od poziomu pewności."
    )

st.divider()
st.subheader("✏️ Dodaj nowy typ i analizę")

st.write("Wpisz dane kuponu oraz swoją analizę. Zostaną zapisane do archiwum w pliku analizy.csv w repozytorium.")

col1, col2 = st.columns(2)
data_input = col1.date_input("Data meczu", value=datetime.today())
sport_input = col2.text_input("Sport", value="Pilka")

mecz_input = st.text_input("Mecz", placeholder="np. Barcelona vs Inter")
rynek_input_analiza = st.text_input("Rynek", placeholder="np. Over/Under 2.5")
pewnosc_input_analiza = st.selectbox("Poziom pewności", ["Pewny", "Sredni", "Ryzykowny"])
stawka_input = st.number_input("Stawka (GBP)", min_value=0.0, step=0.5)
kurs_input_analiza = st.number_input("Kurs WH", min_value=1.0, step=0.01)

wynik_input = st.selectbox("Status kuponu", ["OPEN", "WYGRANA", "PRZEGRANA"])

analiza_input = st.text_area(
    "Twoja analiza (opis po ludzku)",
    placeholder="Tutaj wklej swoją analizę meczu w zwykłym języku..."
)
if st.button("Zapisz typ i analizę"):
    if not mecz_input or not analiza_input:
        st.error("Uzupełnij co najmniej nazwę meczu i analizę.")
    else:
        nowy_wiersz = {
            "data": data_input.strftime("%Y-%m-%d"),
            "sport": sport_input,
            "mecz": mecz_input,
            "rynek": rynek_input_analiza,
            "pewnosc": pewnosc_input_analiza,
            "stawka": f"{stawka_input:.2f}",
            "kurs": f"{kurs_input_analiza:.2f}",
            "wynik": wynik_input,
            "analiza": analiza_input.replace("\n", " ").strip()
        }

        token = st.secrets["GITHUB_TOKEN"]
        repo = "Maruha3000/kupony-dashboard"
        path = "analizy.csv"
        url = f"https://api.github.com/repos/{repo}/contents/{path}"
        headers = {"Authorization": f"token {token}"}

        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            file_data = r.json()
            sha = file_data["sha"]
            content = base64.b64decode(file_data["content"]).decode("utf-8")
        else:
            sha = None
            content = "data,sport,mecz,rynek,pewnosc,stawka,kurs,wynik,analiza\n"

        nowa_linia = ",".join([
            nowy_wiersz["data"], nowy_wiersz["sport"],
            f'"{nowy_wiersz["mecz"]}"', f'"{nowy_wiersz["rynek"]}"',
            nowy_wiersz["pewnosc"], nowy_wiersz["stawka"],
            nowy_wiersz["kurs"], nowy_wiersz["wynik"],
            f'"{nowy_wiersz["analiza"]}"'
        ])

        nowa_zawartosc = content.rstrip("\n") + "\n" + nowa_linia + "\n"
        encoded_content = base64.b64encode(nowa_zawartosc.encode("utf-8")).decode("utf-8")

        payload = {
            "message": f"Dodano typ: {mecz_input}",
            "content": encoded_content,
            "sha": sha
        }

        r2 = requests.put(url, headers=headers, json=payload)

        if r2.status_code in [200, 201]:
            st.success("Typ i analiza zostały zapisane na GitHub.")
        else:
            st.error(f"Błąd zapisu do GitHub: {r2.status_code} — {r2.text}")

        st.divider()
st.subheader("📚 Zapisane typy i analizy")

if os.path.exists("analizy.csv"):
    df_analizy = pd.read_csv("analizy.csv")
    if len(df_analizy) > 0:
        st.dataframe(df_analizy.sort_values("data", ascending=False), use_container_width=True)
    else:
        st.info("Brak zapisanych analiz.")
else:
    st.info("Brak zapisanych analiz — dodaj pierwszy typ powyżej.")
