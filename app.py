import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Alpina Transport Assistant",
    page_icon="🚛",
    layout="wide"
)

# =====================================================
# DESIGN
# =====================================================

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1600px;
}

h1 {font-size: 1.50rem !important;}
h2 {font-size: 1.08rem !important;}
h3 {font-size: 0.92rem !important;}

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
        "Zile circuit",
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
        "Km gol până la încărcare",
        min_value=0,
        value=0,
        step=10
    )

with t2:
    km_intern = st.number_input(
        "Km import pe țară",
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
# RENTABILITATE
# =====================================================

r1, r2 = st.columns(2)

with r1:
    tinta_profit = st.number_input(
        "🎯 Rentabilitate minimă %",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=1.0
    )

with r2:
    st.info(
        "Rentabilitate = Profit ÷ Cost total × 100"
    )


# =====================================================
# COSTURI
# =====================================================

with st.expander("⚙️ COSTURI CAMION", expanded=False):

    st.caption(
        "Valorile pot fi modificate oricând."
    )

    a1, a2, a3 = st.columns(3)

    with a1:
        consum_motorina = st.number_input(
            "Consum motorină l/100 km",
            value=30.0,
            step=0.5
        )

    with a2:
        pret_motorina_brut = st.number_input(
            "Motorină brut €/l",
            value=2.15,
            step=0.01
        )

    with a3:
        tva_motorina = st.number_input(
            "TVA motorină %",
            value=21.0,
            step=1.0
        )

    foloseste_net = st.checkbox(
        "Calculează motorina fără TVA recuperabil",
        value=True
    )

    if foloseste_net:

        pret_motorina_calcul = (
            pret_motorina_brut /
            (1 + tva_motorina / 100)
        )

    else:

        pret_motorina_calcul = pret_motorina_brut

    st.caption(
        f"Preț motorină folosit în calcul: "
        f"{pret_motorina_calcul:.3f} €/l"
    )

    b1, b2, b3 = st.columns(3)

    with b1:
        procent_adblue = st.number_input(
            "Consum AdBlue % din motorină",
            value=5.0,
            step=0.5
        )

    with b2:
        pret_adblue = st.number_input(
            "AdBlue €/l",
            value=0.55,
            step=0.05
        )

    with b3:
        taxe_drum = st.number_input(
            "Taxe drum / circuit €",
            value=300.0,
            step=10.0
        )

    d1, d2, d3 = st.columns(3)

    with d1:
        diurna = st.number_input(
            "Diurnă șofer €/zi",
            value=100.0,
            step=5.0
        )

    with d2:
        salariu_lunar = st.number_input(
            "Salariu brut €/lună",
            value=1000.0,
            step=50.0
        )

    with d3:
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
# BUTON CĂUTARE
# =====================================================

if "afiseaza_rezultate" not in st.session_state:
    st.session_state.afiseaza_rezultate = False


if st.button(
    "🔎 CAUTĂ ȘI ANALIZEAZĂ IMPORTURILE",
    type="primary",
    use_container_width=True
):

    if km_export <= 0:

        st.warning("Introdu km export.")

        st.session_state.afiseaza_rezultate = False

    elif pret_export <= 0:

        st.warning("Introdu încasarea exportului.")

        st.session_state.afiseaza_rezultate = False

    elif not locatie:

        st.warning("Introdu locația camionului.")

        st.session_state.afiseaza_rezultate = False

    else:

        st.session_state.afiseaza_rezultate = True


# =====================================================
# REZULTATE
# =====================================================

if st.session_state.afiseaza_rezultate:

    salariu_zi = salariu_lunar / 30

    cost_diurna = (
        diurna * zile_circuit
    )

    cost_salariu = (
        salariu_zi * zile_circuit
    )

    rezultate = []

    for index, cursa in enumerate(curse_test):

        # ===============================================
        # KM TOTAL
        # ===============================================

        km_total = (
            km_export
            + cursa["km_gol"]
            + cursa["km_import"]
            + km_gol_intern
            + km_intern
        )

        # ===============================================
        # MOTORINĂ
        # ===============================================

        litri_motorina = (
            km_total *
            consum_motorina /
            100
        )

        cost_motorina = (
            litri_motorina *
            pret_motorina_calcul
        )

        # ===============================================
        # ADBLUE
        # ===============================================

        litri_adblue = (
            litri_motorina *
            procent_adblue /
            100
        )

        cost_adblue = (
            litri_adblue *
            pret_adblue
        )

        # ===============================================
        # COST TOTAL
        # ===============================================

        cost_total = (
            cost_motorina
            + cost_adblue
            + cost_diurna
            + cost_salariu
            + taxe_drum
            + mentenanta
        )

        # ===============================================
        # VENIT NECESAR PENTRU RENTABILITATE
        # ===============================================

        venit_necesar = (
            cost_total *
            (1 + tinta_profit / 100)
        )

        # ===============================================
        # IMPORT EXTERN NECESAR
        # ===============================================

        import_necesar = max(
            0,
            venit_necesar
            - pret_export
            - incasare_intern
        )

        rezultate.append({
            **cursa,
            "index": index,
            "km_total": km_total,
            "litri_motorina": litri_motorina,
            "cost_motorina": cost_motorina,
            "litri_adblue": litri_adblue,
            "cost_adblue": cost_adblue,
            "cost_total": cost_total,
            "import_necesar": import_necesar
        })


    # ===============================================
    # SORTARE
    # ===============================================

    rezultate = sorted(
        rezultate,
        key=lambda x:
        x["pret_import"] - x["import_necesar"],
        reverse=True
    )


    st.write("## 📊 IMPORT EXTERN")


    # ===============================================
    # AFIȘARE
    # ===============================================

    for nr, cursa in enumerate(rezultate, start=1):

        st.markdown(
            f"### {nr}. "
            f"{cursa['incarcare']} → "
            f"{cursa['descarcare']}"
        )

        c1, c2, c3, c4, c5, c6 = st.columns(
            [1, 0.7, 0.7, 1.2, 1, 1]
        )

        with c1:

            st.write(
                f"**Ofertă:** "
                f"{cursa['pret_import']} €"
            )

        with c2:

            st.write(
                f"**Gol:** "
                f"{cursa['km_gol']} km"
            )

        with c3:

            st.write(
                f"**Km:** "
                f"{cursa['km_import']}"
            )


        # ===============================================
        # PREȚ NEGOCIAT
        # ===============================================

        with c4:

            pret_negociat = st.number_input(
                "Preț negociat €",
                min_value=0,
                value=cursa["pret_import"],
                step=10,
                key=f"neg_{cursa['index']}"
            )


        # ===============================================
        # RECALCULARE LIVE
        # ===============================================

        venit_total = (
            pret_export
            + pret_negociat
            + incasare_intern
        )

        profit = (
            venit_total
            - cursa["cost_total"]
        )

        rentabilitate = (
            profit /
            cursa["cost_total"] *
            100
        )

        diferenta = max(
            0,
            cursa["import_necesar"]
            - pret_negociat
        )


        with c5:

            st.markdown(
                f"<span class='orange'>"
                f"Necesar: "
                f"{cursa['import_necesar']:.0f} €"
                f"</span>",
                unsafe_allow_html=True
            )


        with c6:

            if diferenta > 0:

                st.markdown(
                    f"<span class='red'>"
                    f"💬 +{diferenta:.0f} €"
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


        # ===============================================
        # REZULTATE COMPACTE
        # ===============================================

        x1, x2, x3, x4, x5, x6 = st.columns(6)

        with x1:
            st.caption(
                f"{cursa['km_total']:.0f} km total"
            )

        with x2:
            st.caption(
                f"Cost {cursa['cost_total']:.0f} €"
            )

        with x3:
            st.caption(
                f"Venit {venit_total:.0f} €"
            )

        with x4:

            if profit >= 0:

                st.markdown(
                    f"<span class='green small'>"
                    f"Profit +{profit:.0f} €"
                    f"</span>",
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"<span class='red small'>"
                    f"Pierdere {profit:.0f} €"
                    f"</span>",
                    unsafe_allow_html=True
                )


        with x5:

            if rentabilitate >= tinta_profit:

                culoare = "green"

            else:

                culoare = "red"

            st.markdown(
                f"<span class='{culoare} small'>"
                f"Rent. {rentabilitate:.1f}%"
                f"</span>",
                unsafe_allow_html=True
            )


        with x6:

            venit_km = (
                venit_total /
                cursa["km_total"]
            )

            st.caption(
                f"{venit_km:.3f} €/km"
            )


        # ===============================================
        # DETALII COST
        # ===============================================

        with st.expander(
            "Vezi costurile acestei variante"
        ):

            q1, q2, q3 = st.columns(3)

            with q1:

                st.write(
                    f"⛽ Motorină: "
                    f"**{cursa['cost_motorina']:.0f} €**"
                )

                st.caption(
                    f"{cursa['litri_motorina']:.0f} litri × "
                    f"{pret_motorina_calcul:.3f} €/l"
                )

            with q2:

                st.write(
                    f"💧 AdBlue: "
                    f"**{cursa['cost_adblue']:.0f} €**"
                )

                st.caption(
                    f"{cursa['litri_adblue']:.1f} litri"
                )

            with q3:

                st.write(
                    f"🛣️ Taxe drum: "
                    f"**{taxe_drum:.0f} €**"
                )

            q4, q5, q6 = st.columns(3)

            with q4:

                st.write(
                    f"👨‍✈️ Diurnă: "
                    f"**{cost_diurna:.0f} €**"
                )

            with q5:

                st.write(
                    f"💼 Salariu alocat: "
                    f"**{cost_salariu:.0f} €**"
                )

            with q6:

                st.write(
                    f"🔧 Mentenanță: "
                    f"**{mentenanta:.0f} €**"
                )

        st.divider()


    st.caption(
        f"🎯 Țintă: {tinta_profit:.0f}% profit peste cost. "
        "Necesar = prețul necesar DOAR pe importul extern."
    )

    st.caption(
        "⚠️ Ofertele sunt momentan de test. "
        "După aprobarea API Trans.eu vor fi înlocuite "
        "cu ofertele reale."
    )
