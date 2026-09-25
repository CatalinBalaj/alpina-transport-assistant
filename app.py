import streamlit as st

st.set_page_config(
    page_title="Alpina Transport Assistant",
    page_icon="🚛",
    layout="wide"
)

st.title("🚛 Alpina Transport Assistant")
st.subheader("Asistent personal pentru dispecerat transport")

st.success("Aplicația funcționează!")

st.write("### Camion disponibil")

col1, col2, col3 = st.columns(3)

with col1:
    locatie = st.text_input("Locație camion", placeholder="ex: Katowice, PL")

with col2:
    destinatie = st.text_input("Destinație dorită", placeholder="ex: România")

with col3:
    data = st.date_input("Data disponibilității")

st.selectbox(
    "Tip semiremorcă",
    ["MEGA 13.6 m / 3 m", "Prelată standard", "Alt tip"]
)

if st.button("🔎 Caută curse"):
    st.info("Căutarea Trans.eu va fi disponibilă după conectarea API.")
