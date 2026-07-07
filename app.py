import streamlit as st
import pandas as pd
from io import StringIO
import os
import random
from datetime import datetime, timedelta
import requests
import base64

st.set_page_config(page_title="Kupony Dashboard", layout="wide")
st.title("Garnek z kapustą")

MIESIACE_PL = {1:"Styczeń",2:"Luty",3:"Marzec",4:"Kwiecień",5:"Maj",6:"Czerwiec",
               7:"Lipiec",8:"Sierpień",9:"Wrzesień",10:"Październik",11:"Listopad",12:"Grudzień"}

def github_get(path):
    token = st.secrets["GITHUB_TOKEN"]
    repo = "Maruha3000/kupony-dashboard"
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        file_data = r.json()
        content = base64.b64decode(file_data["content"]).decode("utf-8")
        return content, file_data["sha"]
    return None, None

def github_put(path, content_str, sha, message):
    token = st.secrets["GITHUB_TOKEN"]
    repo = "Maruha3000/kupony-dashboard"
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"}
    encoded = base64.b64encode(content_str.encode("utf-8")).decode("utf-8")
    payload = {"message": message, "content": encoded}
    if sha:
        payload["sha"] = sha
    return requests.put(url, headers=headers, json=payload)

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

czerwiec_data = """Data,Sport,Rozgrywki,Mecz,Rynek,Pewnosc,Stawka,Kurs,Godzina,Status
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

lipiec_data = """Data,Sport,Rozgrywki,Mecz,Rynek,Pewnosc,Stawka,Kurs,Godzina,Status
01.07.2026,Pilka,MS 2026 R32,England vs DR Congo,England -1.5,Ryzykowny,0.50,1.89,17:00,PRZEGRANA
01.07.2026,Pilka,MS 2026 R32,Belgium vs Senegal,Belgium ML,Sredni,1.00,2.10,21:00,WYGRANA
01.07.2026,Pilka,MS 2026 R32,Belgium vs Senegal,BTTS Yes,Sredni,1.00,1.80,21:00,WYGRANA
01.07.2026,Pilka,MS 2026 R32,USA vs Bosnia & Herz.,Under 2.5 gole,Ryzykowny,0.50,2.08,01:00 (2.VII),WYGRANA
02.07.2026,Pilka,MS 2026 R32,Spain vs Austria,Under 2.5 gole,Sredni,1.00,1.80,20:00,PRZEGRANA
03.07.2026,Pilka,MS 2026 R32,Switzerland vs Algeria,BTTS Yes,Sredni,1.00,1.80,04:00 (3.VII),PRZEGRANA
03.07.2026,Pilka,MS 2026 R32,Australia vs Egypt,BTTS Yes,Ryzykowny,0.50,2.00,19:00 (3.VII),WYGRANA
04.07.2026,Pilka,MS 2026 R32,Colombia vs Ghana,Over 2.5,Sredni,1.00,1.90,01:30 (4.VII),PRZEGRANA
05.07.2026,Pilka,MS 2026 R16,Canada vs Morocco,Under 2.5 gole,Ryzykowny,0.50,1.75,18:00,PRZEGRANA
05.07.2026,Pilka,MS 2026 R16,Paraguay vs France,France -1.5,Sredni,1.00,1.62,22:00,PRZEGRANA
05.07.2026,Pilka,Friendly/MS,Brazil vs Norway,Over 2.5 gole,Sredni,1.00,1.73,20:00,WYGRANA
05.07.2026,Pilka,Friendly/MS,Mexico vs England,Under 1.5 gole,Ryzykowny,0.50,2.85,01:00 (06.07),PRZEGRANA
"""

df_czerwiec = pd.read_csv(StringIO(czerwiec_data))
df_czerwiec["Analiza"] = ""

df_lipiec = pd.read_csv(StringIO(lipiec_data))
df_lipiec["Analiza"] = ""

content, sha_a = github_get("analizy.csv")
if content:
    df_analizy = pd.read_csv(StringIO(content))
else:
    df_analizy = pd.DataFrame(columns=["data","sport","mecz","rynek","pewnosc","stawka","kurs","wynik","analiza"])
    sha_a = None

arch_cols = ["Data","Sport","Rozgrywki","Mecz","Rynek","Pewnosc","Stawka","Kurs","Godzina","Status","Analiza"]
content_arch, sha_arch = github_get("archiwum.csv")
if content_arch:
    df_archiwum = pd.read_csv(StringIO(content_arch))
else:
    df_archiwum = pd.DataFrame(columns=arch_cols)
    sha_arch = None

if len(df_analizy) > 0:
    df_analizy["data_dt"] = pd.to_datetime(df_analizy["data"], format="%Y-%m-%d", errors="coerce")
    df_analizy = df_analizy.sort_values("data_dt", ascending=False).reset_index(drop=True)

    top6_idx = df_analizy.index[:6].tolist()
    open_idx = df_analizy.index[df_analizy["wynik"] == "OPEN"].tolist()
    keep_idx = sorted(set(top6_idx) | set(open_idx))
    move_idx = [i for i in df_analizy.index if i not in keep_idx]

    if len(move_idx) > 0:
        do_przeniesienia = df_analizy.loc[move_idx].copy()
        nowe_wiersze = []
        for _, row in do_przeniesienia.iterrows():
            data_fmt = row["data_dt"].strftime("%d.%m.%Y") if pd.notna(row["data_dt"]) else row["data"]
            nowe_wiersze.append({
                "Data": data_fmt, "Sport": row["sport"], "Rozgrywki": "",
                "Mecz": row["mecz"], "Rynek": row["rynek"], "Pewnosc": row["pewnosc"],
                "Stawka": row["stawka"], "Kurs": row["kurs"], "Godzina": "-",
                "Status": row["wynik"], "Analiza": row.get("analiza", "")
            })
        df_archiwum = pd.concat([df_archiwum, pd.DataFrame(nowe_wiersze)], ignore_index=True)
        df_analizy = df_analizy.loc[keep_idx].reset_index(drop=True)

        buf1 = StringIO(); df_archiwum.to_csv(buf1, index=False)
        github_put("archiwum.csv", buf1.getvalue(), sha_arch, "Auto-archiwizacja starych typow")

        df_analizy_zapis = df_analizy.drop(columns=["data_dt"])
        buf2 = StringIO(); df_analizy_zapis.to_csv(buf2, index=False)
        github_put("analizy.csv", buf2.getvalue(), sha_a, "Usunieto zarchiwizowane typy")

    df_analizy = df_analizy.drop(columns=["data_dt"])

df_archiwum_full = pd.concat([df_czerwiec, df_lipiec, df_archiwum], ignore_index=True, sort=False)
df_archiwum_full["Data_dt"] = pd.to_datetime(df_archiwum_full["Data"], format="%d.%m.%Y", errors="coerce")

def koloruj_status(val):
    if val == "WYGRANA":
        return "background-color: #1e5e2e; color: white;"
    elif val == "PRZEGRANA":
        return "background-color: #6e1e1e; color: white;"
    elif val == "OPEN":
        return "background-color: #4a4a1e; color: white;"
    else:
        return "background-color: #3a3a3a; color: white;"

STATUS_KOLOR = {
    "WYGRANA": "#1e5e2e",
    "PRZEGRANA": "#6e1e1e",
    "OPEN": "#4a4a1e",
}

st.subheader("📊 Statystyki")
zakres_wyboru = st.selectbox("Przedział czasowy", ["Ostatnie 7 dni", "Ostatni miesiąc", "Cały okres"], index=2)

dzis = pd.Timestamp(datetime.today().date())
if zakres_wyboru == "Ostatnie 7 dni":
    data_od = dzis - timedelta(days=7)
elif zakres_wyboru == "Ostatni miesiąc":
    data_od = dzis - timedelta(days=30)
else:
    data_od = None

if data_od is not None:
    df_stats = df_archiwum_full[df_archiwum_full["Data_dt"] >= data_od]
else:
    df_stats = df_archiwum_full

wygrane = df_stats[df_stats["Status"] == "WYGRANA"]
przegrane = df_stats[df_stats["Status"] == "PRZEGRANA"]
rozliczone = df_stats[df_stats["Status"].isin(["WYGRANA", "PRZEGRANA"])]

zysk = (wygrane["Stawka"] * wygrane["Kurs"]).sum() - wygrane["Stawka"].sum() - przegrane["Stawka"].sum()
suma_stawek = rozliczone["Stawka"].sum()
yield_pct = (zysk / suma_stawek * 100) if suma_stawek > 0 else 0
sredni_kurs = rozliczone["Kurs"].mean() if len(rozliczone) > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Liczba kuponów", len(df_stats))
win_rate = len(wygrane) / (len(wygrane) + len(przegrane)) * 100 if (len(wygrane) + len(przegrane)) > 0 else 0
col2.metric("Win rate", f"{win_rate:.0f}%")
col3.metric("Suma stawek", f"£{suma_stawek:.2f}")
col4.metric("Zysk / strata netto", f"£{zysk:+.2f}")
col5.metric("Yield (ROI)", f"{yield_pct:+.1f}%")

st.caption(f"Średni kurs zagranych kuponów: {sredni_kurs:.2f}")
st.divider()

st.subheader("Najnowsze typy")
st.caption("Widoczne: 6 najnowszych typów + wszystkie ze statusem OPEN. Starsze rozliczone trafiają do archiwum.")

if len(df_analizy) > 0:
    for _, row in df_analizy.sort_values("data", ascending=False).iterrows():
        kolor = STATUS_KOLOR.get(row["wynik"], "#3a3a3a")
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{row['mecz']}**")
                st.caption(f"{row['data']} — {row['sport']}")
            with c2:
                st.markdown(
                    f"<div style='background-color:{kolor};color:white;padding:4px 10px;"
                    f"border-radius:6px;text-align:center;font-weight:600;'>{row['wynik']}</div>",
                    unsafe_allow_html=True
                )

            st.markdown(
                f"**Rynek:** {row['rynek']}  \n"
                f"**Pewność:** {row['pewnosc']}  \n"
                f"**Stawka:** £{row['stawka']}  |  **Kurs:** {row['kurs']}"
            )

            if str(row.get("analiza", "")).strip():
                st.markdown(f"_{row['analiza']}_")
else:
    st.info("Brak zapisanych analiz — dodaj pierwszy typ poniżej.")

st.divider()
st.subheader("💰 Kalkulator bezpiecznej stawki")

st.write("Wpisz swój aktualny bank, a system podliczy bezpieczną stawkę na podstawie zasad ochrony kapitału.")

bank_bazowy = 28.0
stawki_bazowe = {"Pewny": 1.50, "Sredni": 1.00, "Ryzykowny": 0.50}

col_bank1, col_bank2 = st.columns(2)
bank_uzytkownika = col_bank1.number_input("Twój aktualny bank (GBP)", min_value=1.0, value=28.0, step=1.0)
pewnosc_bank_input = col_bank2.selectbox("Poziom pewności zakładu", ["Pewny", "Sredni", "Ryzykowny"])

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
        "Pewny 1.50 GBP, Sredni 1.00 GBP, Ryzykowny 0.50 GBP — czyli od 1.8% do 5.4% banku, "
        "zależnie od poziomu pewności."
    )

st.divider()
st.subheader("Archiwum kuponów")

df_archiwum_full["MiesiacRok"] = df_archiwum_full["Data_dt"].apply(
    lambda d: f"{MIESIACE_PL[d.month]} {d.year}" if pd.notna(d) else "Nieznana data"
)
dostepne_miesiace = df_archiwum_full.sort_values("Data_dt", ascending=False)["MiesiacRok"].unique().tolist()

if len(dostepne_miesiace) > 0:
    wybrany_miesiac = st.selectbox("Wybierz miesiąc", dostepne_miesiace)
    df_miesiac = df_archiwum_full[df_archiwum_full["MiesiacRok"] == wybrany_miesiac].drop(columns=["Data_dt", "MiesiacRok"])

    c1, c2 = st.columns(2)
    sport_filter = c1.multiselect("Sport", options=df_miesiac["Sport"].unique(), default=df_miesiac["Sport"].unique())
    status_filter = c2.multiselect("Status", options=df_miesiac["Status"].unique(), default=df_miesiac["Status"].unique())

    df_filtered = df_miesiac[df_miesiac["Sport"].isin(sport_filter) & df_miesiac["Status"].isin(status_filter)]

    st.dataframe(
        df_filtered.style.map(koloruj_status, subset=["Status"]),
        use_container_width=True
    )
else:
    st.info("Brak danych archiwalnych.")

st.divider()
st.subheader("🔒 Zmień status kuponu")
st.caption("Zmiana statusu wymaga podania kodu PIN. Dotyczy typów widocznych w sekcji 'Najnowsze typy'.")

if len(df_analizy) > 0:
    opcje_meczow = df_analizy.apply(
        lambda row: f"{row['data']} | {row['mecz']} | {row['rynek']} (aktualny status: {row['wynik']})",
        axis=1
    ).tolist()

    wybrany_mecz = st.selectbox("Wybierz kupon do zmiany", opcje_meczow)
    nowy_status = st.selectbox("Nowy status", ["OPEN", "WYGRANA", "PRZEGRANA"])
    pin_input = st.text_input("Kod PIN", type="password", max_chars=4, key="pin_status")

    if st.button("Zapisz zmianę"):
        if pin_input != st.secrets["APP_PIN"]:
            st.error("Nieprawidłowy kod PIN. Zmiana nie została zapisana.")
        else:
            wybrany_idx = opcje_meczow.index(wybrany_mecz)
            wybrany_row = df_analizy.iloc[wybrany_idx]

            content_now, sha_now = github_get("analizy.csv")
            df_now = pd.read_csv(StringIO(content_now)) if content_now else df_analizy.copy()

            mask = (
                (df_now["data"] == wybrany_row["data"]) &
                (df_now["mecz"] == wybrany_row["mecz"]) &
                (df_now["rynek"] == wybrany_row["rynek"]) &
                (df_now["stawka"].astype(str) == str(wybrany_row["stawka"])) &
                (df_now["kurs"].astype(str) == str(wybrany_row["kurs"]))
            )

            if mask.sum() == 0:
                st.error("Nie znaleziono tego kuponu w pliku na GitHubie. Odśwież stronę i spróbuj ponownie.")
            else:
                df_now.loc[mask, "wynik"] = nowy_status
                buf = StringIO(); df_now.to_csv(buf, index=False)
                r2 = github_put("analizy.csv", buf.getvalue(), sha_now, f"Zmieniono status: {wybrany_mecz} -> {nowy_status}")

                if r2.status_code in [200, 201]:
                    st.success(f"Status zaktualizowany na: {nowy_status}. Odśwież stronę, aby zobaczyć zmianę w tabeli.")
                    if nowy_status == "WYGRANA":
                        st.balloons()
                else:
                    st.error(f"Błąd zapisu do GitHub: {r2.status_code} — {r2.text}")
else:
    st.info("Brak kuponów do edycji.")

st.divider()
st.subheader("Dodaj typ")
st.caption("Dodanie typu wymaga podania kodu PIN.")

opcje_sportow = [
    "Pilka", "Tenis", "Hokej", "Koszykowka", "Siatkowka",
    "Baseball", "Rugby", "Snooker", "Darts", "MMA/Boks", "Inne"
]

opcje_rynkow = [
    "1X2 - Gospodarze", "1X2 - Remis", "1X2 - Gość",
    "Over 0.5", "Under 0.5", "Over 1.5", "Under 1.5",
    "Over 2.5", "Under 2.5", "Over 3.5", "Under 3.5",
    "Over 4.5", "Under 4.5", "BTTS Yes", "BTTS No",
    "Handicap -1", "Handicap -1.5", "Handicap -2",
    "Handicap +1", "Handicap +1.5", "Handicap +2",
    "Double Chance 1X", "Double Chance X2", "Double Chance 12",
    "Win to Nil - Gospodarze", "Win to Nil - Gość",
    "Correct Score", "Zwycięzca meczu (ML)",
    "Over/Under sety", "Over/Under gemy",
    "Over/Under punkty", "Over/Under goli w hokeju", "Inne"
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

    pin_input_dodaj = st.text_input("Kod PIN", type="password", max_chars=4, key="pin_dodaj")

    if st.button("Zapisz typ i analizę"):
        if pin_input_dodaj != st.secrets["APP_PIN"]:
            st.error("Nieprawidłowy kod PIN. Typ nie został zapisany.")
        elif not mecz_input or not analiza_input:
            st.error("Uzupełnij co najmniej nazwę meczu i analizę.")
        else:
            nowy_wiersz = pd.DataFrame([{
                "data": data_input.strftime("%Y-%m-%d"),
                "sport": sport_input,
                "mecz": mecz_input,
                "rynek": rynek_input_analiza,
                "pewnosc": pewnosc_input_analiza,
                "stawka": f"{stawka_input:.2f}",
                "kurs": f"{kurs_input_analiza:.2f}",
                "wynik": "OPEN",
                "analiza": analiza_input.replace("\n", " ").strip()
            }])

            content_now, sha_now = github_get("analizy.csv")
            if content_now:
                df_now = pd.read_csv(StringIO(content_now))
            else:
                df_now = pd.DataFrame(columns=["data","sport","mecz","rynek","pewnosc","stawka","kurs","wynik","analiza"])

            df_now = pd.concat([df_now, nowy_wiersz], ignore_index=True)
            buf = StringIO(); df_now.to_csv(buf, index=False)
            r2 = github_put("analizy.csv", buf.getvalue(), sha_now, f"Dodano typ: {mecz_input}")

            if r2.status_code in [200, 201]:
                st.success("Typ i analiza zostały zapisane na GitHub (status: OPEN).")
            else:
                st.error(f"Błąd zapisu do GitHub: {r2.status_code} — {r2.text}")
