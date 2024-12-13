import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Titel van de app
st.title("Defecten Analyse Dashboard")

# Upload sectie
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload je Excel-bestand", type=["xlsx"])

if uploaded_file:
    # Laad het bestand
    data = pd.read_excel(uploaded_file, engine="openpyxl")

    # Standaardiseer kolomnamen
    data.columns = data.columns.str.lower().str.replace(" ", "_")

    # Toon basisinformatie
    st.subheader("Kolommen in de dataset:")
    st.write(data.columns)

    st.subheader("Dataset Info:")
    buffer = st.empty()
    buffer.write(data.info())

    # Verwijder duplicaten en vul ontbrekende waarden
    data.drop_duplicates(inplace=True)
    data.fillna(data.mean(numeric_only=True), inplace=True)

    # Controleer datumnotaties
    if "datum" in data.columns:
        data["datum"] = pd.to_datetime(data["datum"], errors="coerce")
    if "reported_date" in data.columns:
        data["reported_date"] = pd.to_datetime(data["reported_date"], errors="coerce")
        data['year'] = data['reported_date'].dt.year

    # Frequentieanalyse van de kolom 'defect'
    if "defect" in data.columns:
        defect_counts = data['defect'].value_counts()
        st.subheader("Top 10 Defectcategorieën:")
        st.bar_chart(defect_counts.head(10))

    # Jaarlijkse defecttrends
    if "year" in data.columns:
        yearly_trends = data.groupby('year').size()
        st.subheader("Jaarlijkse Defecttrends:")
        st.line_chart(yearly_trends)

  # Gemiddelde oplostijd berekenen
    if "resolved_date" in data.columns and "reported_date" in data.columns:
        data['resolution_time'] = (data['resolved_date'] - data['reported_date']).dt.days
        avg_resolution_time = data['resolution_time'].mean()
        st.subheader("Gemiddelde Oplostijd:")
        st.write(f"{avg_resolution_time:.2f} dagen")

    # Defecttrends per jaar en categorie
    if "defect" in data.columns and "year" in data.columns:
        defect_trends = data.groupby(['defect', 'year']).size().reset_index(name='count')
        defect_trends_pivot = defect_trends.pivot(index='year', columns='defect', values='count').fillna(0)
        defect_trends_pivot = defect_trends_pivot.loc[:, defect_trends_pivot.sum().sort_values(ascending=False).index]

        # Selecteer de top 10 defectcategorieën
        top_10_defects = defect_trends_pivot.iloc[:, :10]
        st.subheader("Top 10 Defectcategorieën Over Tijd")
        st.line_chart(top_10_defects)

    # Interactieve plot met Plotly
    if "reported_date" in data.columns:
        data['year_month'] = data['reported_date'].dt.to_period('M').astype(str)
        defect_trends = data.groupby('year_month').size().reset_index(name='defect_count')

        st.subheader("Interactieve Defecttrends Over Tijd")
        fig = px.line(
            defect_trends,
            x='year_month',
            y='defect_count',
            title="Interactieve Defecttrends Over Tijd",
            labels={'year_month': 'Jaar-Maand', 'defect_count': 'Aantal Defecten'},
            markers=True
        )
        st.plotly_chart(fig)

    # Overzicht defecten per sectie
    if 'section' in data.columns and 'defect' in data.columns:
        section_summary = data.groupby('section')['defect'].count().reset_index()
        section_summary.columns = ['Section', 'Defect Count']
        section_summary = section_summary.sort_values(by='Defect Count', ascending=False)
        st.subheader("Overzicht van Defecten per Sectie")
        st.bar_chart(section_summary.set_index("Section"))

    # Heatmap van defecten per sectie
  if 'section' in data.columns and 'defect' in data.columns:
        defects_per_section = data.groupby('section')['defect'].count().reset_index()
        defects_per_section.columns = ['Section', 'Defect Count']
        sections = defects_per_section['Section'].tolist()
        defects = defects_per_section['Defect Count'].tolist()
        colors = plt.cm.viridis(np.array(defects) / max(defects))

        fig, ax = plt.subplots(figsize=(12, 4))
        for i, section in enumerate(sections):
            rect = plt.Rectangle((i, 0), 1, 1, color=colors[i], edgecolor="black")
            ax.add_patch(rect)
            ax.text(i + 0.5, 0.5, f"{section}\n({defects[i]})", ha="center", va="center", color="white", fontsize=10)

        ax.set_xlim(0, len(sections))
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title("Heatmap: Aantal Defecten per Sectie (737 Romp)", fontsize=16)
        sm = plt.cm.ScalarMappable(cmap="viridis", norm=plt.Normalize(vmin=min(defects), vmax=max(defects)))
        cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.1, aspect=40)
        cbar.set_label('Aantal Defecten')
        st.pyplot(fig)

else:
    st.info("Upload een Excel-bestand om te beginnen.")
