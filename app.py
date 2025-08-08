
import streamlit as st
import pandas as pd

# Load the cleaned Excel file
df = pd.read_excel("geospatial_repository_cleaned.xlsx")

st.set_page_config(page_title="Geospatial Data Repository", layout="wide")
st.title("🌍 Geospatial Data Repository")

# Filters
search = st.text_input("🔎 Search for data source, type, or purpose")

if search:
    df_filtered = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
else:
    df_filtered = df

# Show the data
for idx, row in df_filtered.iterrows():
    st.markdown(f"### {row['Data Source']}")
    st.markdown(f"**Description:** {row['Description']}")
    st.markdown(f"**Year/Month:** {row['Year/Month of Data Availability']}")
    st.markdown(f"**Countries Covered:** {row['Countries Covered']}")
    st.markdown(f"**Type:** {row['Type']}")
    st.markdown(f"**Resolution:** {row['Spatial Resolution (in m)']}")
    st.markdown(f"**Version:** {row['Version']}")
    st.markdown(f"**Purpose:** {row['Purpose']}")
    if pd.notna(row['Remarks/Suggestions']):
        st.markdown(f"**Remarks:** {row['Remarks/Suggestions']}")
    st.markdown("---")
