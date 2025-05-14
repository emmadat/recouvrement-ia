import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard Recouvrement IA", layout="wide")
import streamlit as st
st.write("✅ L’application fonctionne !")
# 🔽 Chargement des données
try:
    df = pd.read_csv("data_mock.csv")

    # Nettoyage des dates
    cols_dates = ["dtprescc", "ddmotiet", "ddetatcr"]
    for col in cols_dates:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%d/%m/%Y')

    # Score IA simulé
    np.random.seed(42)
    df["score_risque"] = np.round(np.random.uniform(0, 1, len(df)), 2)

    # Interface Streamlit
    st.title("📊 Tableau de bord Recouvrement IA")

    # Filtres
    annees = sorted(df['annee_cohorte'].unique())
    annee_selection = st.selectbox("Choisir l'année de cohorte", annees)
    df_filtered = df[df["annee_cohorte"] == annee_selection]

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre de dossiers", len(df_filtered))
    col2.metric("Montant initial (€)", f"{df_filtered['mtinicre'].sum():,.2f}")
    col3.metric("Montant résiduel (€)", f"{df_filtered['mtsolree'].sum():,.2f}")

    # Graphique par état
    st.subheader("Répartition des dossiers par état")
    st.bar_chart(df_filtered["lb_etatcre"].value_counts())

    # Tableau des dossiers
    st.subheader("Liste des dossiers")
    st.dataframe(df_filtered)

    if st.checkbox("Afficher uniquement les dossiers à risque élevé (score > 0.8)"):
        st.dataframe(df_filtered[df_filtered["score_risque"] > 0.8])

except Exception as e:
    st.error(f"❌ Erreur lors du chargement ou de l’affichage : {e}")
