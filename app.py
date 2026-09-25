import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Alpina Transport Assistant",
    page_icon="🚛",
    layout="wide"
)

st.title("🚛 Alpina Transport Assistant")
st.subheader("Asistent personal pentru dispecerat transport")

st.success("🟢 Aplicația este online")

st.divider()

# =========================
# CAMION DISPONIBIL
# =========================

st.write("### 🚛 Camion disponibil")

col1, col2, col3 = st.columns(3)

with col1:
    locatie = st.text_input(
        "Locație camion",
        placeholder="ex: Katowice, PL"
    )

with col2:
    destinatie = st.text_input(
        "Destinație dorită",
        placeholder="ex: România"
    )

with col3:
    data_disponibilitate = st.date_input(
        "Data disponibilității",
        value=date.today()
    )

col4, col5 = st.columns(2)

with col4:
    semiremorca = st.selectbox(
        "Tip semiremorcă",
        [
            "MEGA 13.6 m / 3 m",
            "Prelată standard",
            "Alt tip"
        ]
    )

with col5:
    raza = st.selectbox(
        "Rază maximă până la încărcare",
        [
            "50 km",
            "100 km",
            "150 km",
            "200 km",
            "300 km"
        ],
        index=2
    )

st.divider()

# =========================
# CRITERII
# =========================

st.write("### 🎯 Criterii căutare")

col6, col7, col8 = st.columns(3)

with col6:
    pret_minim = st.number_input(
        "Preț minim cursă (€)",
        min_value=0,
        value=0,
        step=50
    )

with col7:
    tarif_minim = st.number_input(
        "Tarif minim dorit (€/km)",
        min_value=0.0,
        value=0.0,
        step=0.05
    )

with col8:
    greutate_max = st.number_input(
        "Greutate maximă (tone)",
        min_value=1.0,
        max_value=30.0,
        value=24.0,
        step=1.0
    )

st.write("")

# =========================
# CURSE TEST
# =========================

curse_test = [
    {
        "incarcare": "Katowice, PL",
        "descarcare": "Oradea, RO",
        "km": 720,
        "pret": 1150,
        "km_pana_incarcare": 45,
        "greutate": 22
    },
    {
        "incarcare": "Gliwice, PL",
        "descarcare": "Cluj-Napoca, RO",
        "km": 790,
        "pret": 1350,
        "km_pana_incarcare": 32,
        "greutate": 24
    },
    {
        "incarcare": "Częstochowa, PL",
        "descarcare": "Baia Mare, RO",
        "km": 690,
        "pret": 1250,
        "km_pana_incarcare": 78,
        "greutate": 21
    }
]

# =========================
# BUTON CĂUTARE
# =========================

if st.button(
    "🔎 CAUTĂ CURSE",
    type="primary",
    use_container_width=True
):

    if not locatie:
        st.warning("Introdu locația camionului.")

    elif not destinatie:
        st.warning("Introdu destinația dorită.")

    else:

        st.divider()
        st.write("## 📋 Curse găsite")

        rezultate = []

        for cursa in curse_test:

            tarif_km = cursa["pret"] / cursa["km"]

            if (
                cursa["pret"] >= pret_minim
                and tarif_km >= tarif_minim
                and cursa["greutate"] <= greutate_max
            ):

                cursa["tarif_km"] = tarif_km
                rezultate.append(cursa)

        rezultate = sorted(
            rezultate,
            key=lambda x: x["tarif_km"],
            reverse=True
        )

        if not rezultate:

            st.warning(
                "Nu există curse care să respecte criteriile selectate."
            )

        else:

            st.success(
                f"Au fost găsite {len(rezultate)} curse potrivite."
            )

            for nr, cursa in enumerate(rezultate, start=1):

                with st.container(border=True):

                    st.write(
                        f"### {nr}. "
                        f"{cursa['incarcare']} → "
                        f"{cursa['descarcare']}"
                    )

                    c1, c2, c3, c4, c5 = st.columns(5)

                    with c1:
                        st.metric(
                            "Distanță cursă",
                            f"{cursa['km']} km"
                        )

                    with c2:
                        st.metric(
                            "Preț",
                            f"{cursa['pret']} €"
                        )

                    with c3:
                        st.metric(
                            "Tarif",
                            f"{cursa['tarif_km']:.2f} €/km"
                        )

                    with c4:
                        st.metric(
                            "Până la încărcare",
                            f"{cursa['km_pana_incarcare']} km"
                        )

                    with c5:
                        st.metric(
                            "Greutate",
                            f"{cursa['greutate']} t"
                        )

        st.caption(
            "⚠️ Momentan sunt afișate curse de test. "
            "După aprobarea API Trans.eu, acestea vor fi "
            "înlocuite cu ofertele reale."
        )
