import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

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
st.title("Searchtool Transavia Aircraft Data")

# Transavia-logo toevoegen
st.image("data/hoi/Transavia_logo.png", use_container_width=True)

# Tabs voor zoekfunctie en visualisatie
tab1, tab2 = st.tabs(["🔍 Zoektool", "📊 Visualisatie"])

# Bestandsopties
file_options = {
    "PH-HS": "data/hoi/PH-HS.csv",
    "PH-HX": "data/hoi/PH-HX.csv"
}

# Tab 1: Zoektool
with tab1:
    selected_file = st.selectbox("Kies een CSV-bestand om te doorzoeken:", list(file_options.keys()))
    
    if selected_file:
        file_path = file_options[selected_file]
        data = pd.read_csv(file_path)
        
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

# Tab 2: Visualisatie
with tab2:
    st.subheader("Visualisatie van PH-HS Data")

    # Laad de PH-HS CSV
    ph_hs_data = pd.read_csv("data/hoi/PH-HS.csv")

    # Selecteer kolommen voor visualisatie
    numeric_columns = ph_hs_data.select_dtypes(include=['number']).columns.tolist()
    if numeric_columns:
        x_col = st.selectbox("Selecteer de X-as:", numeric_columns)
        y_col = st.selectbox("Selecteer de Y-as:", numeric_columns)
        
        # Maak een scatter plot
        fig, ax = plt.subplots()
        ax.scatter(ph_hs_data[x_col], ph_hs_data[y_col], alpha=0.7)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{x_col} vs {y_col}")
        
        # Toon de grafiek
        st.pyplot(fig)
    else:
        st.warning("Geen numerieke kolommen beschikbaar voor visualisatie.")
