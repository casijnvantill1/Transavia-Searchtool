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
    
    # Zoekterm in alle kolommen
    mask = df.astype(str).apply(lambda row: row.str.contains(search_term, case=False, na=False)).any(axis=1)
    return df[mask]

# Titel van de app
st.title("Excel Searchtool")

# Upload-sectie in de zijbalk
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload je Excel-bestand", type=["xlsx"])

if uploaded_file:
    # Laad het bestand
    data = pd.read_excel(uploaded_file, engine="openpyxl")
    
    # Toon de eerste paar rijen van de dataset
    st.subheader("Voorbeeld van de dataset:")
    st.write(data.head())

    # Zoekterm invoeren
    search_term = st.text_input("Voer een zoekterm in (bijvoorbeeld een woord, getal, of een deelstring):")
    
    if st.button("Zoek"):
        # Zoek de resultaten
        results = search_anywhere_partial(data, search_term)
        
        if not results.empty:
            st.success(f"Gevonden resultaten ({len(results)} rijen):")
            st.write(results)
            
            # Optie om de resultaten op te slaan
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
    st.info("Upload een Excel-bestand om te beginnen.")
