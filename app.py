import streamlit as st
import pandas as pd

# Load the Excel file with links
df = pd.read_excel("Geospatial Data Repository (1).xlsx")

st.set_page_config(page_title="Geospatial Data Repository", layout="wide")
st.title("🌍 Geospatial Data Repository")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
country_filter = st.sidebar.multiselect("Countries Covered", sorted(df['Countries Covered'].dropna().unique()))
type_filter = st.sidebar.multiselect("Type", sorted(df['Type'].dropna().unique()))
purpose_filter = st.sidebar.multiselect("Purpose", sorted(df['Purpose'].dropna().unique()))

# Filter logic
filtered_df = df.copy()

if country_filter:
    filtered_df = filtered_df[filtered_df['Countries Covered'].isin(country_filter)]
if type_filter:
    filtered_df = filtered_df[filtered_df['Type'].isin(type_filter)]
if purpose_filter:
    filtered_df = filtered_df[filtered_df['Purpose'].isin(purpose_filter)]

# Search box
search = st.text_input("Search for any keyword...")
if search:
    filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

# Display results
st.markdown(f"### Showing {len(filtered_df)} results")

for _, row in filtered_df.iterrows():
    if pd.notna(row.get('Link')):
        st.markdown(f"#### [{row['Data Source']}]({row['Link']})")
    else:
        st.markdown(f"#### {row['Data Source']}")
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

# Option to download filtered data
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_geospatial_data.csv",
    mime="text/csv"
)
