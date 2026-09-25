import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Alpina Transport Assistant",
    page_icon="🚛",
    layout="wide"
)

st.title("🚛 Alpina Transport Assistant")
st.subheader("Analiză rentabilitate Export → Import")

# =========================
# EXPORT
# =========================

st.write("## 🇷🇴 EXPORT – cursa de plecare")

e1, e2, e3, e4 = st.columns(4)

with e1:
    plecare_export = st.text_input(
        "Plecare export",
        placeholder="ex: Baia Mare, RO"
    )

with e2:
    descarcare_export = st.text_input(
        "Descărcare export",
        placeholder="ex: Katowice, PL"
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
        "Preț export (€)",
        min_value=0,
        value=0,
        step=50
    )

if km_export > 0:
    tarif_export = pret_export / km_export
    st.info(f"Tarif export: **{tarif_export:.2f} €/km**")

st.divider()

# =========================
# CAMION LIBER
# =========================

st.write("## 🚛 Camion disponibil după descărcare")

c1, c2, c3 = st.columns(3)

with c1:
    locatie = st.text_input(
        "Locație camion",
        placeholder="ex: Katowice, PL"
    )

with c2:
    destinatie = st.text_input(
        "Destinație import",
        placeholder="ex: România"
    )

with c3:
    data_disponibilitate = st.date_input(
        "Data disponibilității",
        value=date.today()
    )

c4, c5 = st.columns(2)

with c4:
    semiremorca = st.selectbox(
        "Tip semiremorcă",
        [
            "MEGA 13.6 m / 3 m",
            "Prelată standard",
            "Alt tip"
        ]
    )

with c5:
    raza = st.selectbox(
        "Rază maximă până la încărcare",
        ["50 km", "100 km", "150 km", "200 km", "300 km"],
        index=2
    )

st.divider()

# =========================
# CURSE IMPORT TEST
# =========================

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

# =========================
# CĂUTARE / CALCUL
# =========================

if st.button(
    "🔎 CAUTĂ IMPORT ȘI CALCULEAZĂ RENTABILITATEA",
    type="primary",
    use_container_width=True
):

    if km_export <= 0:
        st.warning("Introdu numărul de km al cursei de export.")

    elif pret_export <= 0:
        st.warning("Introdu prețul cursei de export.")

    elif not locatie:
        st.warning("Introdu locația camionului după descărcarea exportului.")

    elif not destinatie:
        st.warning("Introdu destinația dorită pentru import.")

    else:

        rezultate = []

        for cursa in curse_test:

            venit_total = (
                pret_export +
                cursa["pret_import"]
            )

            km_total = (
                km_export +
                cursa["km_gol"] +
                cursa["km_import"]
            )

            tarif_import_real = (
                cursa["pret_import"] /
                (cursa["km_gol"] + cursa["km_import"])
            )

            tarif_ciclu = venit_total / km_total

            rezultat = cursa.copy()
            rezultat["venit_total"] = venit_total
            rezultat["km_total"] = km_total
            rezultat["tarif_import_real"] = tarif_import_real
            rezultat["tarif_ciclu"] = tarif_ciclu

            rezultate.append(rezultat)

        # Cele mai rentabile cicluri primele
        rezultate = sorted(
            rezultate,
            key=lambda x: x["tarif_ciclu"],
            reverse=True
        )

        st.divider()
        st.write("## 📊 Rentabilitate Export + Import")

        for nr, cursa in enumerate(rezultate, start=1):

            with st.container(border=True):

                st.write(
                    f"### {nr}. {cursa['incarcare']} → "
                    f"{cursa['descarcare']}"
                )

                a, b, c, d = st.columns(4)

                with a:
                    st.metric(
                        "Preț import",
                        f"{cursa['pret_import']} €"
                    )

                with b:
                    st.metric(
                        "Km gol",
                        f"{cursa['km_gol']} km"
                    )

                with c:
                    st.metric(
                        "Tarif import real",
                        f"{cursa['tarif_import_real']:.2f} €/km"
                    )

                with d:
                    st.metric(
                        "TARIF CICLU",
                        f"{cursa['tarif_ciclu']:.2f} €/km"
                    )

                st.write("#### 🚛 Circuit complet")

                st.write(
                    f"Export: **{km_export} km / {pret_export} €**  →  "
                    f"Gol: **{cursa['km_gol']} km**  →  "
                    f"Import: **{cursa['km_import']} km / "
                    f"{cursa['pret_import']} €**"
                )

                t1, t2 = st.columns(2)

                with t1:
                    st.metric(
                        "KM TOTAL CICLU",
                        f"{cursa['km_total']} km"
                    )

                with t2:
                    st.metric(
                        "VENIT TOTAL CICLU",
                        f"{cursa['venit_total']} €"
                    )

        st.caption(
            "⚠️ Importurile sunt momentan date de test. "
            "După conectarea API Trans.eu vor fi înlocuite "
            "cu ofertele reale."
        )
