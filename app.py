import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Alpina Transport Assistant",
    page_icon="🚛",
    layout="wide"
)

# =====================================================
# DESIGN COMPACT
# =====================================================

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1600px;
}

h1 {font-size: 1.65rem !important;}
h2 {font-size: 1.15rem !important;}
h3 {font-size: 1rem !important;}

div[data-testid="stMetricValue"] {
    font-size: 1.15rem;
}

div[data-testid="stMetricLabel"] {
    font-size: 0.72rem;
}

.small {
    font-size: 0.80rem;
}

.green {
    color: #16a34a;
    font-weight: bold;
}

.red {
    color: #dc2626;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🚛 Alpina Transport Assistant")
st.caption("Analiză rentabilitate circuit complet")


# =====================================================
# EXPORT
# =====================================================

st.write("## 🇷🇴 Export")

e1, e2, e3, e4 = st.columns(4)

with e1:
    plecare_export = st.text_input(
        "Plecare",
        placeholder="Baia Mare, RO"
    )

with e2:
    descarcare_export = st.text_input(
        "Descărcare",
        placeholder="Katowice, PL"
    )

with e3:
    km_export = st.number_input(
        "Km export",
        min_value=0,
        value=0,
        step=10
    )

with e4:
    pret_export = st.number_input(
        "Încasare export €",
        min_value=0,
        value=0,
        step=50
    )


# =====================================================
# CAMION DUPĂ EXPORT
# =====================================================

st.write("## 🚛 Camion disponibil")

c1, c2, c3, c4 = st.columns(4)

with c1:
    locatie = st.text_input(
        "Locație camion",
        placeholder="Katowice, PL"
    )

with c2:
    destinatie = st.text_input(
        "Import spre",
        placeholder="România"
    )

with c3:
    data_disponibilitate = st.date_input(
        "Disponibil",
        value=date.today()
    )

with c4:
    zile_circuit = st.number_input(
        "Zile circuit",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )


# =====================================================
# CURSĂ INTERNĂ
# =====================================================

st.write("## 🇷🇴 Cursă internă după import")

i1, i2 = st.columns(2)

with i1:
    km_intern = st.number_input(
        "Km cursă internă până la garaj",
        min_value=0,
        value=0,
        step=10
    )

with i2:
    incasare_intern = st.number_input(
        "Încasare cursă internă €",
        min_value=0,
        value=0,
        step=50
    )


# =====================================================
# COSTURI
# =====================================================

with st.expander("⚙️ Costuri camion", expanded=False):

    a1, a2, a3, a4 = st.columns(4)

    with a1:
        consum_motorina = st.number_input(
            "Consum motorină l/100 km",
            value=30.0,
            step=0.5
        )

    with a2:
        pret_motorina = st.number_input(
            "Motorină €/l",
            value=2.15,
            step=0.01
        )

    with a3:
        consum_adblue = st.number_input(
            "AdBlue l/100 km",
            value=1.7,
            step=0.1
        )

    with a4:
        pret_adblue = st.number_input(
            "AdBlue €/l",
            value=1.00,
            step=0.05
        )

    b1, b2, b3, b4 = st.columns(4)

    with b1:
        diurna = st.number_input(
            "Diurnă €/zi",
            value=100.0,
            step=5.0
        )

    with b2:
        salariu_lunar = st.number_input(
            "Salariu brut €/lună",
            value=1000.0,
            step=50.0
        )

    with b3:
        taxe_drum = st.number_input(
            "Taxe drum / circuit €",
            value=300.0,
            step=10.0
        )

    with b4:
        mentenanta = st.number_input(
            "Mentenanță / circuit €",
            value=150.0,
            step=10.0
        )


# =====================================================
# OFERTE IMPORT TEST
# =====================================================

curse_test = [
    {
        "incarcare": "Katowice, PL",
        "descarcare": "Oradea, RO",
        "km_import": 720,
        "pret_import": 1150,
        "km_gol": 45
    },
    {
        "incarcare": "Gliwice, PL",
        "descarcare": "Cluj-Napoca, RO",
        "km_import": 790,
        "pret_import": 1350,
        "km_gol": 32
    },
    {
        "incarcare": "Częstochowa, PL",
        "descarcare": "Baia Mare, RO",
        "km_import": 690,
        "pret_import": 1250,
        "km_gol": 78
    }
]


# =====================================================
# ANALIZĂ
# =====================================================

if st.button(
    "🔎 ANALIZEAZĂ IMPORTURILE",
    type="primary",
    use_container_width=True
):

    if km_export <= 0:

        st.warning("Introdu km export.")

    elif pret_export <= 0:

        st.warning("Introdu încasarea exportului.")

    elif not locatie:

        st.warning("Introdu locația camionului.")

    else:

        st.write("## 📊 Oferte import")

        salariu_zi = salariu_lunar / 30

        cost_sofer = (
            (diurna + salariu_zi)
            * zile_circuit
        )

        rezultate = []

        # =================================================
        # CALCULĂM TOATE OFERTELE
        # =================================================

        for index, cursa in enumerate(curse_test):

            km_total = (
                km_export
                + cursa["km_gol"]
                + cursa["km_import"]
                + km_intern
            )

            venit_total = (
                pret_export
                + cursa["pret_import"]
                + incasare_intern
            )

            litri_motorina = (
                km_total
                * consum_motorina
                / 100
            )

            cost_motorina = (
                litri_motorina
                * pret_motorina
            )

            litri_adblue = (
                km_total
                * consum_adblue
                / 100
            )

            cost_adblue = (
                litri_adblue
                * pret_adblue
            )

            cost_total = (
                cost_motorina
                + cost_adblue
                + cost_sofer
                + taxe_drum
                + mentenanta
            )

            profit = (
                venit_total
                - cost_total
            )

            venit_km = (
                venit_total / km_total
            )

            cost_km = (
                cost_total / km_total
            )

            profit_km = (
                profit / km_total
            )

            # Import minim pentru ZERO profit
            import_zero_profit = max(
                0,
                cost_total
                - pret_export
                - incasare_intern
            )

            rezultate.append({
                **cursa,
                "index": index,
                "km_total": km_total,
                "venit_total": venit_total,
                "cost_total": cost_total,
                "profit": profit,
                "venit_km": venit_km,
                "cost_km": cost_km,
                "profit_km": profit_km,
                "import_zero_profit": import_zero_profit
            })


        # Cele mai profitabile primele
        rezultate = sorted(
            rezultate,
            key=lambda x: x["profit"],
            reverse=True
        )


        # =================================================
        # AFIȘARE
        # =================================================

        for nr, cursa in enumerate(rezultate, start=1):

            st.markdown(
                f"### {nr}. {cursa['incarcare']} → "
                f"{cursa['descarcare']}"
            )

            r1, r2, r3, r4, r5, r6 = st.columns(
                [1.2, 0.8, 0.9, 1.2, 1.0, 1.0]
            )

            with r1:
                st.write(
                    f"**Ofertă:** {cursa['pret_import']} €"
                )

            with r2:
                st.write(
                    f"**Gol:** {cursa['km_gol']} km"
                )

            with r3:
                st.write(
                    f"**Import:** {cursa['km_import']} km"
                )

            with r4:

                pret_negociat = st.number_input(
                    "Preț negociat €",
                    min_value=0,
                    value=cursa["pret_import"],
                    step=10,
                    key=f"pret_{cursa['index']}"
                )


            # =================================================
            # RECALCULARE CU PREȚ NEGOCIAT
            # =================================================

            venit_total = (
                pret_export
                + pret_negociat
                + incasare_intern
            )

            profit = (
                venit_total
                - cursa["cost_total"]
            )

            venit_km = (
                venit_total
                / cursa["km_total"]
            )

            profit_km = (
                profit
                / cursa["km_total"]
            )

            with r5:

                if profit >= 0:

                    st.markdown(
                        f"<span class='green'>"
                        f"🟢 +{profit:.0f} €"
                        f"</span>",
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"<span class='red'>"
                        f"🔴 {profit:.0f} €"
                        f"</span>",
                        unsafe_allow_html=True
                    )

            with r6:

                if profit >= 0:

                    st.markdown(
                        f"<span class='green'>"
                        f"{venit_km:.3f} €/km"
                        f"</span>",
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"<span class='red'>"
                        f"{venit_km:.3f} €/km"
                        f"</span>",
                        unsafe_allow_html=True
                    )


            # =================================================
            # AL DOILEA RÂND
            # =================================================

            x1, x2, x3, x4, x5 = st.columns(5)

            with x1:

                st.caption(
                    f"Total: {cursa['km_total']:.0f} km"
                )

            with x2:

                st.caption(
                    f"Cost: {cursa['cost_total']:.0f} €"
                )

            with x3:

                st.caption(
                    f"Cost/km: "
                    f"{cursa['cost_km']:.3f} €"
                )

            with x4:

                st.caption(
                    f"Profit/km: "
                    f"{profit_km:.3f} €"
                )

            with x5:

                diferenta = (
                    cursa["import_zero_profit"]
                    - pret_negociat
                )

                if diferenta > 0:

                    st.markdown(
                        f"<span class='red small'>"
                        f"Zero profit: +{diferenta:.0f} €"
                        f"</span>",
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        "<span class='green small'>"
                        "✓ Peste prag rentabilitate"
                        "</span>",
                        unsafe_allow_html=True
                    )

            st.divider()


        # =================================================
        # REPER COSTURI
        # =================================================

        with st.expander(
            "📋 Cum se calculează costul",
            expanded=False
        ):

            st.write(
                f"Motorină: **{consum_motorina:.1f} l/100 km** "
                f"× **{pret_motorina:.2f} €/l**"
            )

            st.write(
                f"AdBlue: **{consum_adblue:.1f} l/100 km** "
                f"× **{pret_adblue:.2f} €/l**"
            )

            st.write(
                f"Șofer: **{diurna:.0f} €/zi diurnă + "
                f"{salariu_zi:.2f} €/zi salariu** "
                f"× **{zile_circuit} zile**"
            )

            st.write(
                f"Taxe drum: **{taxe_drum:.0f} €**"
            )

            st.write(
                f"Mentenanță: **{mentenanta:.0f} € / circuit**"
            )


        st.caption(
            "⚠️ Ofertele de import sunt momentan date de test. "
            "După conectarea API Trans.eu vor fi înlocuite "
            "cu ofertele reale."
        )
