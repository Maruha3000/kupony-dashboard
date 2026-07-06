import streamlit as st
import pandas as pd
from io import StringIO
import csv
import os
import random
from datetime import datetime
import requests
import base64
st.set_page_config(page_title="Kupony Dashboard", layout="wide")
st.title("📊 Garnek z kapustą")

cytaty_dnia = [
    "Dyscyplina bije emocje. Zawsze.",
    "Bank nie rośnie od jednego kuponu — rośnie od systemu.",
    "Najlepszy zakład to czasem ten, którego nie postawisz.",
    "Cierpliwość to najbardziej niedoceniana strategia bukmacherska.",
    "Nie gonimy strat. Trzymamy się planu.",
    "Value > emocje. Zawsze.",
    "Mały, stabilny zysk pokona dużą, ryzykowną stratę.",
    "Systematyczność wygrywa z natchnieniem.",
]
random.seed(datetime.today().strftime("%Y-%m-%d"))
st.info(f"💡 {random.choice(cytaty_dnia)}")

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

wygrane = df[df["Status"] == "WYGRANA"]
przegrane = df[df["Status"] == "PRZEGRANA"]
rozliczone = df[df["Status"].isin(["WYGRANA", "PRZEGRANA"])]

zysk = (wygrane["Stawka"] * wygrane["Kurs"]).sum() - wygrane["Stawka"].sum() - przegrane["Stawka"].sum()
suma_stawek = rozliczone["Stawka"].sum()
yield_pct = (zysk / suma_stawek * 100) if suma_stawek > 0 else 0
sredni_kurs = rozliczone["Kurs"].mean() if len(rozliczone) > 0 else 0

rozliczone_sorted = rozliczone.copy()
rozliczone_sorted["Data_sort"] = pd.to_datetime(rozliczone_sorted["Data"], format="%d.%m.%Y", errors="coerce")
rozliczone_sorted = rozliczone_sorted.sort_values("Data_sort")
statusy_seria = rozliczone_sorted["Status"].tolist()

streak_count = 0
streak_type = None
for s in reversed(statusy_seria):
    if streak_type is None:
        streak_type = s
        streak_count = 1
    elif s == streak_type:
        streak_count += 1
    else:
        break

if streak_type == "WYGRANA":
    streak_label = f"🔥 {streak_count} wygrane z rzędu"
elif streak_type == "PRZEGRANA":
    streak_label = f"❄️ {streak_count} przegrane z rzędu"
else:
    streak_label = "brak serii"

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Liczba kuponów", len(df))
win_rate = len(wygrane) / (len(wygrane) + len(przegrane)) * 100 if (len(wygrane) + len(przegrane)) > 0 else 0
col2.metric("Win rate", f"{win_rate:.0f}%")
col3.metric("Suma stawek", f"£{suma_stawek:.2f}")
col4.metric("Zysk / strata netto", f"£{zysk:+.2f}")
col5.metric("Yield (ROI)", f"{yield_pct:+.1f}%")
col6.metric("Aktualna seria", streak_label)

st.caption(f"Średni kurs zagranych kuponów: {sredni_kurs:.2f}")
st.divider()

def koloruj_status(val):
    if val == "WYGRANA":
        return "background-color: #1e5e2e; color: white;"
    elif val == "PRZEGRANA":
        return "background-color: #6e1e1e; color: white;"
    elif val == "OPEN":
        return "background-color: #4a4a1e; color: white;"
    else:
        return "background-color: #3a3a3a; color: white;"

st.subheader("📚 Zapisane typy i analizy")

if os.path.exists("analizy.csv"):
    df_analizy = pd.read_csv("analizy.csv")
else:
    df_analizy = pd.DataFrame(columns=["data", "sport", "mecz", "rynek", "pewnosc", "stawka", "kurs", "wynik", "analiza"])

if len(df_analizy) > 0:
    st.dataframe(
        df_analizy.sort_values("data", ascending=False).style.map(koloruj_status, subset=["wynik"]),
        use_container_width=True
    )
else:
    st.info("Brak zapisanych analiz — dodaj pierwszy typ poniżej.")

st.divider()
st.subheader("✏️ Dodaj nowy typ i analizę")

opcje_sportow = [
    "Pilka", "Tenis", "Hokej", "Koszykowka", "Siatkowka",
    "Baseball", "Rugby", "Snooker", "Darts", "MMA/Boks", "Inne"
]

opcje_rynkow = [
    "1X2 - Gospodarze",
    "1X2 - Remis",
    "1X2 - Gość",
    "Over 0.5", "Under 0.5",
    "Over 1.5", "Under 1.5",
    "Over 2.5", "Under 2.5",
    "Over 3.5", "Under 3.5",
    "Over 4.5", "Under 4.5",
    "BTTS Yes", "BTTS No",
    "Handicap -1", "Handicap -1.5", "Handicap -2",
    "Handicap +1", "Handicap +1.5", "Handicap +2",
    "Double Chance 1X", "Double Chance X2", "Double Chance 12",
    "Win to Nil - Gospodarze", "Win to Nil - Gość",
    "Correct Score",
    "Zwycięzca meczu (ML)",
    "Over/Under sety", "Over/Under gemy",
    "Over/Under punkty", "Over/Under goli w hokeju",
    "Inne"
]

with st.container():
    col_a, col_b = st.columns(2)
    data_input = col_a.date_input("Data meczu", value=datetime.today())
    sport_input = col_b.selectbox("Sport", opcje_sportow)

    col_c, col_d = st.columns(2)
    mecz_input = col_c.text_input("Mecz", placeholder="np. Barcelona vs Inter")
    rynek_input_analiza = col_d.selectbox("Rynek", opcje_rynkow)

    col_e, col_f = st.columns(2)
    pewnosc_input_analiza = col_e.selectbox("Poziom pewności", ["Pewny", "Sredni", "Ryzykowny"])
    stawka_input = col_f.number_input("Stawka (GBP)", min_value=0.0, step=0.5)

    kurs_input_analiza = st.number_input("Kurs WH", min_value=1.0, step=0.01)

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
                "wynik": "OPEN",
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
                st.success("Typ i analiza zostały zapisane na GitHub (status: OPEN).")
            else:
                st.error(f"Błąd zapisu do GitHub: {r2.status_code} — {r2.text}")

st.divider()
st.subheader("💰 Kalkulator bezpiecznej stawki")

st.write("Wpisz swój aktualny bank, a system podliczy bezpieczną stawkę na podstawie zasad ochrony kapitału.")

bank_bazowy = 28.0
stawki_bazowe = {"Pewny": 1.50, "Średni": 1.00, "Ryzykowny": 0.50}

col_bank1, col_bank2 = st.columns(2)
bank_uzytkownika = col_bank1.number_input("Twój aktualny bank (GBP)", min_value=1.0, value=28.0, step=1.0)
pewnosc_bank_input = col_bank2.selectbox("Poziom pewności zakładu", ["Pewny", "Średni", "Ryzykowny"])

if st.button("Policz stawkę"):
    wspolczynnik = bank_uzytkownika / bank_bazowy
    stawka_rekomendowana = round(stawki_bazowe[pewnosc_bank_input] * wspolczynnik, 2)
    procent_banku = round((stawka_rekomendowana / bank_uzytkownika) * 100, 1)

    st.success(
        f"Przy banku {bank_uzytkownika:.2f} GBP i pewności '{pewnosc_bank_input}', "
        f"bezpieczna stawka to około **{stawka_rekomendowana} GBP** "
        f"(to około {procent_banku}% Twojego banku)."
    )
    st.caption(
        "To przeliczenie bazuje na zasadzie, że przy banku 28 GBP stawki wynoszą: "
        "Pewny 1.50 GBP, Średni 1.00 GBP, Ryzykowny 0.50 GBP — czyli od 1.8% do 5.4% banku, "
        "zależnie od poziomu pewności."
    )

st.divider()
st.subheader("Filtry")
c1, c2 = st.columns(2)
sport_filter = c1.multiselect("Sport", options=df["Sport"].unique(), default=df["Sport"].unique())
status_filter = c2.multiselect("Status", options=df["Status"].unique(), default=df["Status"].unique())

df_filtered = df[df["Sport"].isin(sport_filter) & df["Status"].isin(status_filter)]

st.subheader("Wszystkie kupony - czerwiec 2026")
st.dataframe(
    df_filtered.style.map(koloruj_status, subset=["Status"]),
    use_container_width=True
)

st.divider()
st.subheader("🔒 Zmień status kuponu")
st.caption("Zmiana statusu wymaga podania kodu PIN.")

if len(df_analizy) > 0:
    opcje_meczow = df_analizy.apply(
        lambda row: f"{row['data']} | {row['mecz']} | {row['rynek']} (aktualny status: {row['wynik']})",
        axis=1
    ).tolist()

    wybrany_mecz = st.selectbox("Wybierz kupon do zmiany", opcje_meczow)
    nowy_status = st.selectbox("Nowy status", ["OPEN", "WYGRANA", "PRZEGRANA"])
    pin_input = st.text_input("Kod PIN", type="password", max_chars=4)

    if st.button("Zapisz zmianę"):
        if pin_input != st.secrets["APP_PIN"]:
            st.error("Nieprawidłowy kod PIN. Zmiana nie została zapisana.")
        else:
            idx = opcje_meczow.index(wybrany_mecz)
            df_analizy.loc[df_analizy.index[idx], "wynik"] = nowy_status

            token = st.secrets["GITHUB_TOKEN"]
            repo = "Maruha3000/kupony-dashboard"
            path = "analizy.csv"
            url = f"https://api.github.com/repos/{repo}/contents/{path}"
            headers = {"Authorization": f"token {token}"}

            r = requests.get(url, headers=headers)
            sha = r.json()["sha"] if r.status_code == 200 else None

            csv_buffer = StringIO()
            df_analizy.to_csv(csv_buffer, index=False)
            nowa_zawartosc = csv_buffer.getvalue()
            encoded_content = base64.b64encode(nowa_zawartosc.encode("utf-8")).decode("utf-8")

            payload = {
                "message": f"Zmieniono status: {wybrany_mecz} -> {nowy_status}",
                "content": encoded_content,
                "sha": sha
            }

            r2 = requests.put(url, headers=headers, json=payload)

            if r2.status_code in [200, 201]:
                st.success(f"Status zaktualizowany na: {nowy_status}. Odśwież stronę, aby zobaczyć zmianę w tabeli.")
                if nowy_status == "WYGRANA":
                    st.balloons()
            else:
                st.error(f"Błąd zapisu do GitHub: {r2.status_code} — {r2.text}")
else:
    st.info("Brak kuponów do edycji.")
