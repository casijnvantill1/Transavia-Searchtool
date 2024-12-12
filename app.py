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
st.title("Interactieve Zoektool voor CSV-bestanden")

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
st.title("Searchtool Transavia Aircraft Data")

# Selecteer een bestand
file_options = {
    "PH-HS": "data/hoi/PH-HX.csv",
    "PH-HX": "data/hoi/PH-HS.csv"
}

selected_file = st.selectbox("Kies een CSV-bestand om te doorzoeken:", list(file_options.keys()))

if selected_file:
    # Laad het geselecteerde bestand
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


