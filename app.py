import streamlit as st
import pandas as pd

# ----- PAGE CONFIGURATION -----
st.set_page_config(page_title="GeoAI Repository", layout="wide")

# ----- CUSTOM CSS -----
st.markdown("""
    <style>
        .block-container {
            padding: 2rem 2rem 2rem 2rem;
        }
        .stButton>button {
            color: white;
            background: #4CAF50;
        }
        .stRadio > div {
            flex-direction: row;
        }
        .title-style {
            font-size: 1.3rem;
            font-weight: 600;
            color: #1a73e8;
        }
        .desc-style {
            font-size: 0.95rem;
        }
        .link-style {
            font-size: 0.9rem;
            color: #007BFF;
        }
    </style>
""", unsafe_allow_html=True)

# ----- LOAD DATA FUNCTION -----
@st.cache_data
def load_data(sheet_name):
    df = pd.read_excel("Geospatial Data Repository (1).xlsx", sheet_name=sheet_name)
    df.columns = df.iloc[0]
    df = df[1:]
    df = df.dropna(subset=[df.columns[0]])
    return df

# ----- SIDEBAR NAVIGATION -----
st.sidebar.header("🧭 Navigation")
sheet_options = {
    "Data Sources": "Data Sources",
    "Tools": "Tools",
    "Free Tutorials": "Free Tutorials",
    "Python Codes (GEE)": "Google Earth EnginePython Codes",
    "Courses": "Courses",
}
selected_tab = st.sidebar.radio("Select Category", list(sheet_options.keys()))

# ----- LOAD DATA -----
df = load_data(sheet_options[selected_tab])

# ----- SIDEBAR FILTERS -----
st.sidebar.markdown("---")
search_term = st.sidebar.text_input("🔍 Search Repository")
if search_term:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

if selected_tab == "Data Sources":
    type_filter = st.sidebar.multiselect("📁 Filter by Type", df["Type"].dropna().unique())
    if type_filter:
        df = df[df["Type"].isin(type_filter)]

# ----- MAIN TITLE -----
st.title(f"🌍 GeoAI Repository – {selected_tab}")

# ----- DISPLAY DATA AS CARDS -----
if df.empty:
    st.warning("No results found. Try adjusting your search or filters.")
else:
    cols = st.columns(2)
    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i % 2]:
            st.markdown(f"<div class='title-style'>🔹 {row.get('Data Source') or row.get('Tools') or row.get('Title') or row.get('Tutorials')}</div>", unsafe_allow_html=True)
            if "Description" in row and pd.notna(row["Description"]):
                st.markdown(f"<div class='desc-style'>{row['Description']}</div>", unsafe_allow_html=True)

            # Show link
            link = row.get("Links") or row.get("Link") or row.get("Link to the codes")
            if pd.notna(link):
                st.markdown(f"<div class='link-style'>🔗 [Access Link]({link})</div>", unsafe_allow_html=True)

            # Optional fields
            if "Purpose" in row and pd.notna(row["Purpose"]):
                st.markdown(f"**🎯 Purpose:** {row['Purpose']}")
            if "Year/Month of Data Availability" in row and pd.notna(row["Year/Month of Data Availability"]):
                st.markdown(f"**📅 Year/Month:** {row['Year/Month of Data Availability']}")

            st.markdown("---")
