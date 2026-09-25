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

if st.button("🔎 CAUTĂ CURSE", type="primary", use_container_width=True):

    if not locatie:
        st.warning("Introdu locația camionului.")

    elif not destinatie:
        st.warning("Introdu destinația dorită.")

    else:
        st.info(
            f"🔎 Căutare: {locatie} → {destinatie} | "
            f"{semiremorca} | rază {raza}"
        )

        st.warning(
            "Conectarea la Trans.eu este în așteptarea accesului API."
        )
