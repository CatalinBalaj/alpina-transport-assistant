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

h1 {font-size: 1.55rem !important;}
h2 {font-size: 1.10rem !important;}
h3 {font-size: 0.95rem !important;}

div[data-testid="stMetricValue"] {
    font-size: 1.05rem;
}

div[data-testid="stMetricLabel"] {
    font-size: 0.70rem;
}

.small {
    font-size: 0.78rem;
}

.green {
    color: #16a34a;
    font-weight: bold;
}

.red {
    color: #dc2626;
    font-weight: bold;
}

.orange {
    color: #d97706;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


st.title("🚛 Alpina Transport Assistant")
st.caption(
    "Export → Import extern → Import România → Garaj"
)


# =====================================================
# 1. EXPORT
# =====================================================

st.write("## 1️⃣ EXPORT – FIX")

e1, e2, e3, e4 = st.columns(4)

with e1:
    plecare_export = st.text_input(
        "Plecare export",
        placeholder="Baia Mare"
    )

with e2:
    descarcare_export = st.text_input(
        "Descărcare export",
        placeholder="Polonia"
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
# 2. IMPORT EXTERN
# =====================================================

st.write("## 2️⃣ IMPORT EXTERN – DE NEGOCIAT")

c1, c2, c3, c4 = st.columns(4)

with c1:
    locatie = st.text_input(
        "Camion liber în",
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
        "Zile circuit total",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )


# =====================================================
# 3. IMPORT PE ȚARĂ
# =====================================================

st.write("## 3️⃣ IMPORT PE ȚARĂ → GARAJ")

t1, t2, t3 = st.columns(3)

with t1:
    km_gol_intern = st.number_input(
        "Km gol până la încărcare internă",
        min_value=0,
        value=0,
        step=10
    )

with t2:
    km_intern = st.number_input(
        "Km cursă internă",
        min_value=0,
        value=0,
        step=10
    )

with t3:
    incasare_intern = st.number_input(
        "Încasare import pe țară €",
        min_value=0,
        value=0,
        step=50
    )


# =====================================================
# RENTABILITATE DORITĂ
# =====================================================

st.write("## 🎯 RENTABILITATE")

r1, r2 = st.columns(2)

with r1:
    tinta_profit = st.number_input(
        "Profit dorit peste cost %",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=1.0
    )

with r2:
    st.info(
        "Ținta se calculează: PROFIT ÷ COST TOTAL × 100"
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
# OFERTE TEST
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
# VALIDARE
# =====================================================

date_complete = (
    km_export > 0
    and pret_export > 0
    and locatie != ""
)


if not date_complete:

    st.info(
        "Completează exportul și locația camionului "
        "pentru a analiza importurile."
    )

else:

    # =================================================
    # COST ȘOFER
    # =================================================

    salariu_zi = salariu_lunar / 30

    cost_sofer = (
        (diurna + salariu_zi)
        * zile_circuit
    )

    rezultate = []

    # =================================================
    # CALCUL OFERTE
    # =================================================

    for index, cursa in enumerate(curse_test):

        km_total = (
            km_export
            + cursa["km_gol"]
            + cursa["km_import"]
            + km_gol_intern
            + km_intern
        )

        # MOTORINĂ
        litri_motorina = (
            km_total
            * consum_motorina
            / 100
        )

        cost_motorina = (
            litri_motorina
            * pret_motorina
        )

        # ADBLUE
        litri_adblue = (
            km_total
            * consum_adblue
            / 100
        )

        cost_adblue = (
            litri_adblue
            * pret_adblue
        )

        # COST TOTAL
        cost_total = (
            cost_motorina
            + cost_adblue
            + cost_sofer
            + taxe_drum
            + mentenanta
        )

        # =============================================
        # VENIT NECESAR PENTRU PROFITUL DORIT
        #
        # Exemplu:
        # cost = 3000 €
        # țintă = 20%
        # venit necesar = 3600 €
        # =============================================

        venit_necesar = (
            cost_total
            * (1 + tinta_profit / 100)
        )

        # Export + intern sunt venituri FIXE.
        # Calculăm cât trebuie obținut pe import extern.

        import_extern_necesar = max(
            0,
            venit_necesar
            - pret_export
            - incasare_intern
        )

        rezultate.append({
            **cursa,
            "index": index,
            "km_total": km_total,
            "cost_total": cost_total,
            "cost_motorina": cost_motorina,
            "cost_adblue": cost_adblue,
            "import_extern_necesar": import_extern_necesar
        })


    # =================================================
    # SORTARE
    # =================================================

    rezultate = sorted(
        rezultate,
        key=lambda x:
        x["pret_import"] - x["import_extern_necesar"],
        reverse=True
    )


    st.write("## 📊 IMPORT EXTERN")


    # =================================================
    # AFIȘARE OFERTE
    # =================================================

    for nr, cursa in enumerate(rezultate, start=1):

        st.markdown(
            f"### {nr}. {cursa['incarcare']} → "
            f"{cursa['descarcare']}"
        )

        col1, col2, col3, col4, col5, col6 = st.columns(
            [1.0, 0.7, 0.8, 1.2, 1.0, 1.0]
        )

        with col1:

            st.write(
                f"**Ofertă:** {cursa['pret_import']} €"
            )

        with col2:

            st.write(
                f"**Gol:** {cursa['km_gol']} km"
            )

        with col3:

            st.write(
                f"**Km:** {cursa['km_import']}"
            )


        # =================================================
        # PREȚ NEGOCIAT
        # =================================================

        with col4:

            pret_negociat = st.number_input(
                "Preț negociat €",
                min_value=0,
                value=cursa["pret_import"],
                step=10,
                key=f"pret_negociat_{cursa['index']}"
            )


        # =================================================
        # RECALCULARE LIVE
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

        if cursa["cost_total"] > 0:

            rentabilitate = (
                profit
                / cursa["cost_total"]
            ) * 100

        else:

            rentabilitate = 0


        diferenta_negociere = max(
            0,
            cursa["import_extern_necesar"]
            - pret_negociat
        )


        # =================================================
        # PREȚ NECESAR
        # =================================================

        with col5:

            st.markdown(
                f"<span class='orange'>"
                f"Necesar: "
                f"{cursa['import_extern_necesar']:.0f} €"
                f"</span>",
                unsafe_allow_html=True
            )


        # =================================================
        # DIFERENȚĂ NEGOCIERE
        # =================================================

        with col6:

            if diferenta_negociere > 0:

                st.markdown(
                    f"<span class='red'>"
                    f"💬 +{diferenta_negociere:.0f} €"
                    f"</span>",
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    "<span class='green'>"
                    "✓ ȚINTĂ ATINSĂ"
                    "</span>",
                    unsafe_allow_html=True
                )


        # =================================================
        # REZULTAT LIVE
        # =================================================

        x1, x2, x3, x4, x5, x6 = st.columns(6)

        with x1:

            st.caption(
                f"Total: "
                f"{cursa['km_total']:.0f} km"
            )

        with x2:

            st.caption(
                f"Cost: "
                f"{cursa['cost_total']:.0f} €"
            )

        with x3:

            st.caption(
                f"Venit: "
                f"{venit_total:.0f} €"
            )

        with x4:

            if profit >= 0:

                st.markdown(
                    f"<span class='green small'>"
                    f"Profit: +{profit:.0f} €"
                    f"</span>",
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"<span class='red small'>"
                    f"Pierdere: {profit:.0f} €"
                    f"</span>",
                    unsafe_allow_html=True
                )


        with x5:

            if rentabilitate >= tinta_profit:

                st.markdown(
                    f"<span class='green small'>"
                    f"Rentabilitate: "
                    f"{rentabilitate:.1f}%"
                    f"</span>",
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"<span class='red small'>"
                    f"Rentabilitate: "
                    f"{rentabilitate:.1f}%"
                    f"</span>",
                    unsafe_allow_html=True
                )


        with x6:

            venit_km = (
                venit_total
                / cursa["km_total"]
            )

            st.caption(
                f"Venit/km: "
                f"{venit_km:.3f} €"
            )


        st.divider()


    # =====================================================
    # EXPLICAȚIE COSTURI
    # =====================================================

    with st.expander(
        "📋 Detalii calcul",
        expanded=False
    ):

        st.write(
            f"Motorină: "
            f"**{consum_motorina:.1f} l/100 km × "
            f"{pret_motorina:.2f} €/l**"
        )

        st.write(
            f"AdBlue: "
            f"**{consum_adblue:.1f} l/100 km × "
            f"{pret_adblue:.2f} €/l**"
        )

        st.write(
            f"Șofer: "
            f"**{diurna:.0f} €/zi diurnă + "
            f"{salariu_zi:.2f} €/zi salariu × "
            f"{zile_circuit} zile**"
        )

        st.write(
            f"Taxe drum: **{taxe_drum:.0f} €**"
        )

        st.write(
            f"Mentenanță: **{mentenanta:.0f} € / circuit**"
        )


    st.caption(
        f"🎯 Ținta este {tinta_profit:.0f}% profit peste cost. "
        "Suma NECESAR reprezintă exclusiv prețul necesar "
        "pentru IMPORTUL EXTERN."
    )

    st.caption(
        "⚠️ Ofertele sunt momentan date de test. "
        "După conectarea API Trans.eu vor fi înlocuite "
        "cu ofertele reale."
    )
