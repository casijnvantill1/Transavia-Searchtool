import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Functie om Excel-bestanden te laden
@st.cache
def load_data(file_path):
    return pd.read_excel(file_path, engine="openpyxl")

# Bestandspad en data laden
file_path = '/Users/casijnvantill/Desktop/Data Science/Case Transavia/defect_report_24042024.xlsx'
data = load_data(file_path)

# Standaardiseer kolomnamen
data.columns = data.columns.str.upper()

# Titel van de app
st.title("Transavia Data Visualisatie")

# Sidebar met filters
st.sidebar.header("Filters")
selected_section = st.sidebar.multiselect("Selecteer Sectie", options=data['SECTION'].dropna().unique(), default=data['SECTION'].dropna().unique())
selected_defect = st.sidebar.multiselect("Selecteer Defect", options=data['DEFECT_DESCRIPTION'].dropna().unique(), default=data['DEFECT_DESCRIPTION'].dropna().unique())

# Data filteren op basis van selecties
filtered_data = data[(data['SECTION'].isin(selected_section)) & (data['DEFECT_DESCRIPTION'].isin(selected_defect))]

# Toon de gefilterde data
st.subheader("Gefilterde Data")
st.dataframe(filtered_data)

# Visualisatie 1: Heatmap van Secties
st.subheader("Heatmap: Defecten per Sectie")

# Tellen van defecten per sectie
section_defect_counts = filtered_data.groupby('SECTION').size().reset_index(name='Defect Count')

# Heatmap maken
sections = section_defect_counts['SECTION'].tolist()
defects = section_defect_counts['Defect Count'].tolist()
colors = plt.cm.viridis(np.array(defects) / max(defects) if defects else [0])

fig, ax = plt.subplots(figsize=(12, 4))
for i, section in enumerate(sections):
    rect = plt.Rectangle((i, 0), 1, 1, color=colors[i], edgecolor="black")
    ax.add_patch(rect)
    ax.text(i + 0.5, 0.5, f"{section}\n({defects[i]})", ha="center", va="center", color="white", fontsize=10)

ax.set_xlim(0, len(sections))
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.axis("off")
ax.set_title("Heatmap: Aantal Defecten per Sectie", fontsize=16)

# Voeg kleurenbalk toe
if defects:
    sm = plt.cm.ScalarMappable(cmap="viridis", norm=plt.Normalize(vmin=min(defects), vmax=max(defects)))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.1, aspect=40)
    cbar.set_label('Aantal Defecten', fontsize=12)

st.pyplot(fig)

# Visualisatie 2: Trendanalyse
st.subheader("Trendanalyse: Defecten Over Tijd")

# Zorg dat de datumnotatie correct is
if 'REPORTED_DATE' in data.columns:
    filtered_data['REPORTED_DATE'] = pd.to_datetime(filtered_data['REPORTED_DATE'], errors='coerce')
    filtered_data['YEAR_MONTH'] = filtered_data['REPORTED_DATE'].dt.to_period('M')

    # Groepeer defecten per maand
    defect_trends = filtered_data.groupby('YEAR_MONTH').size().reset_index(name='Defect Count')
    defect_trends['YEAR_MONTH'] = defect_trends['YEAR_MONTH'].astype(str)

    # Plot met Plotly
    trend_fig = px.line(
        defect_trends,
        x='YEAR_MONTH',
        y='Defect Count',
        title="Defect Trends Over Tijd",
        labels={'YEAR_MONTH': 'Jaar-Maand', 'Defect Count': 'Aantal Defecten'},
        markers=True
    )
    st.plotly_chart(trend_fig)
else:
    st.write("De kolom 'REPORTED_DATE' ontbreekt in de dataset.")

# Downloadoptie voor gefilterde data
st.sidebar.download_button(
    label="Download Gefilterde Data",
    data=filtered_data.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)

import pandas as pd
import streamlit as st

# Functie om te zoeken in het hele bestand, inclusief partiële matches
def search_anywhere_partial(df, search_term):
    """
    Zoekt naar een willekeurige term (of deel van een term) in alle kolommen van een DataFrame.
    
    Parameters:
        df (DataFrame): De dataset om te doorzoeken.
        search_term (str): De zoekterm.
        
    Returns:
        DataFrame: Rijen waar de zoekterm (of deel ervan) voorkomt.
    """
    if not search_term:
        return pd.DataFrame()
    
    mask = df.astype(str).apply(lambda row: row.str.contains(search_term, case=False, na=False)).any(axis=1)
    return df[mask]

# Streamlit-app configureren
st.title("Interactie Zoektool voor CSV-bestanden")

# Upload CSV-bestand
uploaded_file = st.file_uploader("Upload een CSV-bestand", type="csv")

if uploaded_file:
    # Laad de dataset
    data = pd.read_csv(uploaded_file)
    
    # Toon de eerste paar rijen
    st.subheader("Voorbeeld van data:")
    st.write(data.head())
    
    # Zoekterm invoeren
    search_term = st.text_input("Voer een zoekterm in (bijvoorbeeld een woord, getal, of een deelstring):")
    
    if st.button("Zoek"):
        # Zoek de resultaten
        results = search_anywhere_partial(data, search_term)
        
        if not results.empty:
            st.success(f"Gevonden resultaten ({len(results)} rijen):")
            st.write(results)
            
            # Optie om resultaten op te slaan
            csv = results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download resultaten als CSV",
                data=csv,
                file_name="search_results.csv",
                mime="text/csv",
            )
        else:
            st.warning("Geen resultaten gevonden.")

else:
    st.info("Upload een CSV-bestand om te beginnen.")

