import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Titel van de app
st.title("Defecten Analyse Dashboard")

st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload je Excel-bestand", type=["xlsx"])

if uploaded_file:
    data = pd.read_excel(uploaded_file, engine="openpyxl")
    data.columns = data.columns.str.lower().str.replace(" ", "_")

    st.subheader("Kolommen in de dataset:")
    st.write(data.columns.tolist())

    # Verwijder duplicaten en vul ontbrekende waarden
    data.drop_duplicates(inplace=True)
    data.fillna(data.mean(numeric_only=True), inplace=True)

    # Controleer datumnotaties
    if "reported_date" in data.columns:
        data["reported_date"] = pd.to_datetime(data["reported_date"], errors="coerce")
        data['year'] = data['reported_date'].dt.year

    # Frequentieanalyse
    if "defect" in data.columns:
        st.subheader("Top 10 Defectcategorieën")
        defect_counts = data['defect'].value_counts().head(10)
        st.bar_chart(defect_counts)

    # Jaarlijkse defecttrends
    if "year" in data.columns:
        yearly_trends = data.groupby('year').size()
        st.subheader("Jaarlijkse Defecttrends")
        st.line_chart(yearly_trends)

    # Oplostijd berekenen
    if "resolved_date" in data.columns and "reported_date" in data.columns:
        data['resolution_time'] = (data['resolved_date'] - data['reported_date']).dt.days
        avg_resolution_time = data['resolution_time'].mean()
        st.subheader("Gemiddelde Oplostijd")
        st.write(f"{avg_resolution_time:.2f} dagen")

    # Interactieve Plotly-trendgrafiek
    if "reported_date" in data.columns:
        data['year_month'] = data['reported_date'].dt.to_period('M').astype(str)
        defect_trends = data.groupby('year_month').size().reset_index(name='defect_count')

        st.subheader("Interactieve Defecttrends Over Tijd")
        fig = px.line(defect_trends, x='year_month', y='defect_count',
                      title="Defecttrends Over Tijd", markers=True)
        st.plotly_chart(fig)

    # Defecten per sectie
    if "section" in data.columns and "defect" in data.columns:
        section_summary = data.groupby('section')['defect'].count().reset_index()
        section_summary.columns = ['Section', 'Defect Count']
        st.subheader("Defecten per Sectie")
        st.bar_chart(section_summary.set_index('Section'))

else:
    st.info("Upload een Excel-bestand om te beginnen.")
