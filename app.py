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
