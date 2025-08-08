import streamlit as st
import pandas as pd

st.set_page_config(page_title="GeoAI Repository", layout="wide")

# ----- Load Excel -----
@st.cache_data
def load_data(sheet_name):
    df = pd.read_excel("Geospatial Data Repository (1).xlsx", sheet_name=sheet_name)
    df.columns = df.iloc[0]  # Use first row as headers
    df = df[1:]  # Skip the header row
    df = df.dropna(subset=[df.columns[0]])  # Drop empty rows
    return df

# ----- Sidebar Navigation -----
st.sidebar.header("🧭 GeoAI Repository")
sheet_options = {
    "Data Sources": "Data Sources",
    "Tools": "Tools",
    "Free Tutorials": "Free Tutorials",
    "Python Codes (GEE)": "Google Earth EnginePython Codes",
    "Courses": "Courses",
}
selected_tab = st.sidebar.radio("Select Category", list(sheet_options.keys()))

# ----- Load selected data -----
df = load_data(sheet_options[selected_tab])

# ----- Sidebar Filters -----
search_term = st.sidebar.text_input("🔍 Search")
if search_term:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

if selected_tab == "Data Sources":
    type_filter = st.sidebar.multiselect("📂 Filter by Type", df["Type"].dropna().unique())
    if type_filter:
        df = df[df["Type"].isin(type_filter)]

# ----- Main Title -----
st.title(f"🌍 GeoAI Repository – {selected_tab}")

# ----- Display Data -----
for idx, row in df.iterrows():
    # Title detection
    title = row.get("Data Source") or row.get("Tools") or row.get("Title") or row.get("Tutorials") or "Unnamed"
    st.subheader(f"🔹 {title}")

    # Description
    if "Description" in row and pd.notna(row["Description"]):
        st.write(row["Description"])

    # Link
    link = row.get("Links") or row.get("Link") or row.get("Link to the codes")
    if pd.notna(link):
        st.markdown(f"[🔗 Access Link]({link})", unsafe_allow_html=True)

    # Conditional Fields
    if selected_tab == "Data Sources":
        if "Type" in row and pd.notna(row["Type"]):
            st.markdown(f"**📂 Type:** {row['Type']}")
        if "Spatial Resolution" in row and pd.notna(row["Spatial Resolution"]):
            st.markdown(f"**📏 Spatial Resolution:** {row['Spatial Resolution']}")
        if "Version" in row and pd.notna(row["Version"]):
            st.markdown(f"**🧾 Version:** {row['Version']}")
        if "Year/Month of Data Availability" in row and pd.notna(row["Year/Month of Data Availability"]):
            st.markdown(f"**📅 Year/Month:** {row['Year/Month of Data Availability']}")

    elif selected_tab == "Tools":
        if "Applicability" in row and pd.notna(row["Applicability"]):
            st.markdown(f"**🛠️ Applicability:** {row['Applicability']}")
        if "Type" in row and pd.notna(row["Type"]):
            st.markdown(f"**📂 Type:** {row['Type']}")
        if "Datasets Availability" in row and pd.notna(row["Datasets Availability"]):
            st.markdown(f"**📊 Datasets Availability:** {row['Datasets Availability']}")

    # Common Purpose Field
    if "Purpose" in row and pd.notna(row["Purpose"]):
        st.markdown(f"**🎯 Purpose:** {row['Purpose']}")

    st.markdown("---")
