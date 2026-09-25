import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Alpina Transport Assistant",
    page_icon="🚛",
    layout="wide"
)

# CSS - interfață mai compactă
st.markdown("""
<style>
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
    }

    h1 {font-size: 1.8rem !important;}
    h2 {font-size: 1.25rem !important;}
    h3 {font-size: 1.05rem !important;}

    div[data-testid="stMetricValue"] {
        font-size: 1.25rem;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.75rem;
    }

    .cursa-box {
        padding: 7px 10px;
        border: 1px solid #444;
        border-radius: 7px;
        margin-bottom: 5px;
        font-size: 0.88rem;
    }

    .verde {
        color: #21c55d;
        font-weight: bold;
    }

    .rosu {
        color: #ff4b4b;
        font-weight: bold;
    }

    .mic {
        font-size: 0.78rem;
        opacity: 0.80;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚛 Alpina Transport Assistant")
st.caption("Analiză rentabilitate Export → Import")


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
        "Preț export €",
        min_value=0,
        value=0,
        step=50
    )


# =====================================================
# CAMION / CIRCUIT
# =====================================================

st.write("## 🚛 Camion / circuit")

c1, c2, c3, c4, c5 = st.columns(5)

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
        max_value=15,
        value=4,
        step=1
    )

with c5:
    tinta_tarif = st.number_input(
        "Țintă €/km",
        min_value=0.50,
        max_value=3.00,
        value=1.20,
        step=0.01,
        format="%.2f"
    )


# =====================================================
# COSTURI
# =====================================================

with st.expander("⚙️ Costuri camion", expanded=False):

    x1, x2, x3, x4 = st.columns(4)

    with x1:
        consum_motorina = st.number_input(
            "Consum motorină l/100 km",
            value=37.0,
            step=0.5
        )

    with x2:
        pret_motorina = st.number_input(
            "Motorină €/l",
            value=2.15,
            step=0.01
        )

    with x3:
        consum_adblue = st.number_input(
            "AdBlue l/100 km",
            value=1.7,
            step=0.1
        )

    with x4:
        pret_adblue = st.number_input(
            "AdBlue €/l",
            value=1.00,
            step=0.05
        )

    y1, y2, y3, y4 = st.columns(4)

    with y1:
        diurna = st.number_input(
            "Diurnă €/zi",
            value=100.0,
            step=5.0
        )

    with y2:
        salariu_lunar = st.number_input(
            "Salariu brut €/lună",
            value=1000.0,
            step=50.0
        )

    with y3:
        taxe_drum = st.number_input(
            "Taxe drum / circuit €",
            value=300.0,
            step=10.0
        )

    with y4:
        mentenanta_km = st.number_input(
            "Revizii + anvelope €/km",
            value=0.20,
            step=0.01
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
        "km_gol": 45,
        "greutate": 22
    },
    {
        "incarcare": "Gliwice, PL",
        "descarcare": "Cluj-Napoca, RO",
        "km_import": 790,
        "pret_import": 1350,
        "km_gol": 32,
        "greutate": 24
    },
    {
        "incarcare": "Częstochowa, PL",
        "descarcare": "Baia Mare, RO",
        "km_import": 690,
        "pret_import": 1250,
        "km_gol": 78,
        "greutate": 21
    }
]


# =====================================================
# CĂUTARE
# =====================================================

if st.button(
    "🔎 ANALIZEAZĂ IMPORTURILE",
    type="primary",
    use_container_width=True
):

    if km_export <= 0:
        st.warning("Introdu km export.")

    elif pret_export <= 0:
        st.warning("Introdu prețul exportului.")

    elif not locatie:
        st.warning("Introdu locația camionului.")

    elif not destinatie:
        st.warning("Introdu destinația importului.")

    else:

        st.write("## 📊 Oferte import")

        # -----------------------------
        # COST ȘOFER
        # -----------------------------

        salariu_zi = salariu_lunar / 30

        cost_sofer = (
            (diurna + salariu_zi)
            * zile_circuit
        )

        rezultate = []

        for index, cursa in enumerate(curse_test):

            km_total = (
                km_export
                + cursa["km_gol"]
                + cursa["km_import"]
            )

            # Preț minim import pentru ținta €/km
            venit_necesar_tinta = (
                km_total * tinta_tarif
            )

            import_necesar = max(
                0,
                venit_necesar_tinta - pret_export
            )

            rezultate.append({
                **cursa,
                "index": index,
                "km_total": km_total,
                "import_necesar": import_necesar
            })

        # Sortare inițială după oferta de import
        rezultate = sorted(
            rezultate,
            key=lambda x: x["pret_import"],
            reverse=True
        )


        # =================================================
        # AFIȘARE COMPACTĂ
        # =================================================

        for nr, cursa in enumerate(rezultate, start=1):

            st.markdown(
                f"### {nr}. {cursa['incarcare']} → "
                f"{cursa['descarcare']}"
            )

            a, b, c, d, e, f = st.columns(
                [1.4, 1, 1, 1.4, 1.2, 1.2]
            )

            with a:
                st.write(
                    f"**Ofertă:** {cursa['pret_import']} €"
                )

            with b:
                st.write(
                    f"**Gol:** {cursa['km_gol']} km"
                )

            with c:
                st.write(
                    f"**Import:** {cursa['km_import']} km"
                )

            with d:

                pret_negociat = st.number_input(
                    "Preț negociat €",
                    min_value=0,
                    value=cursa["pret_import"],
                    step=10,
                    key=f"negociat_{cursa['index']}"
                )

            # -----------------------------------------
            # CALCUL CU PREȚUL NEGOCIAT
            # -----------------------------------------

            venit_total = (
                pret_export
                + pret_negociat
            )

            km_total = cursa["km_total"]

            tarif_ciclu = (
                venit_total / km_total
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

            # MENTENANȚĂ
            cost_mentenanta = (
                km_total
                * mentenanta_km
            )

            # COST TOTAL
            cost_total = (
                cost_motorina
                + cost_adblue
                + cost_mentenanta
                + taxe_drum
                + cost_sofer
            )

            # PROFIT
            profit = (
                venit_total
                - cost_total
            )

            # CÂT MAI TREBUIE NEGOCIAT
            diferenta_tinta = max(
                0,
                cursa["import_necesar"]
                - pret_negociat
            )

            with e:

                if tarif_ciclu >= tinta_tarif:

                    st.markdown(
                        f"<span class='verde'>"
                        f"🟢 {tarif_ciclu:.3f} €/km"
                        f"</span>",
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"<span class='rosu'>"
                        f"🔴 {tarif_ciclu:.3f} €/km"
                        f"</span>",
                        unsafe_allow_html=True
                    )

            with f:

                if profit >= 0:

                    st.markdown(
                        f"<span class='verde'>"
                        f"Profit: {profit:.0f} €"
                        f"</span>",
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"<span class='rosu'>"
                        f"Pierdere: {profit:.0f} €"
                        f"</span>",
                        unsafe_allow_html=True
                    )

            # -----------------------------------------
            # AL DOILEA RÂND - FOARTE COMPACT
            # -----------------------------------------

            r1, r2, r3, r4 = st.columns(4)

            with r1:
                st.caption(
                    f"Total circuit: {km_total} km"
                )

            with r2:
                st.caption(
                    f"Cost total: {cost_total:.0f} €"
                )

            with r3:
                st.caption(
                    f"Import necesar: "
                    f"{cursa['import_necesar']:.0f} €"
                )

            with r4:

                if diferenta_tinta > 0:

                    st.markdown(
                        f"<span class='rosu mic'>"
                        f"Negociază +{diferenta_tinta:.0f} €"
                        f"</span>",
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        "<span class='verde mic'>"
                        "✓ ȚINTĂ ATINSĂ"
                        "</span>",
                        unsafe_allow_html=True
                    )

            st.divider()


        st.caption(
            "⚠️ Ofertele sunt momentan date de test. "
            "După conectarea Trans.eu vor fi înlocuite "
            "cu ofertele reale."
        )
