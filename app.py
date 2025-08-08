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

# ----- Sidebar Support Section -----
st.sidebar.markdown("---")
st.sidebar.markdown("💰 **Support the GeoAI Repository**")
st.sidebar.markdown("If you find this helpful, consider supporting the project!")
st.sidebar.markdown("**📧 UPI ID:** `yourupi@upi`")
st.sidebar.markdown("[📲 Pay via UPI](upi://pay?pa=yourupi@upi&pn=YourName)", unsafe_allow_html=True)
st.sidebar.image("images/your_upi_qr.png", caption="Scan to Pay via UPI", use_column_width=True)

# ----- About Section -----
with st.expander("ℹ️ About the GeoAI Repository", expanded=True):
    st.markdown("""
    The **GeoAI Repository** is a curated, open-access platform designed to support researchers, students, professionals, and enthusiasts working at the intersection of **Geospatial Technologies** and **Artificial Intelligence (AI)**.

    ### 🚀 What You’ll Find Here

    - ✅ High-quality **open geospatial datasets**  
    - 🛠️ AI-powered and geospatial **tools and platforms**  
    - 📚 Free **tutorials**, **courses**, and **sample code** (e.g., in Google Earth Engine, Python)  
    - 🔎 A searchable and categorized **resource hub** to save your time and accelerate your work  

    Whether you're building urban analytics tools, mapping climate impacts, monitoring biodiversity, or exploring satellite imagery, this repository is built to empower your journey with **practical and trustworthy GeoAI resources**.

    ### 🙌 Why Support This Project?

    This repository is a passion-driven, community-centered initiative — maintained without external funding.

    If you find this resource useful, your support will help us:

    - Continuously add and validate new tools, datasets, and examples  
    - Improve usability and structure of the platform  
    - Keep the repository **free and open to all**

    ---  
    **📧 UPI ID**: `yourupi@upi`  
    [📲 Click here to contribute via UPI](upi://pay?pa=yourupi@upi&pn=YourName)  
    _or scan the QR code on the left sidebar_
    """)

# ----- Main Title -----
st.title(f"🌍 GeoAI Repository – {selected_tab}")

# ----- Display Data -----
for idx, row in df.iterrows():
    title = row.get("Data Source") or row.get("Tools") or row.get("Title") or row.get("Tutorials") or "Unnamed"
    st.subheader(f"🔹 {title}")

    # Description
    if "Description" in row and pd.notna(row["Description"]):
        st.write(row["Description"])

    # Link
    link = row.get("Links") or row.get("Link") or row.get("Link to the codes")
    if pd.notna(link):
        st.markdown(f"[🔗 Access Link]({link})", unsafe_allow_html=True)

    # Tab-specific metadata
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

    # Common field
    if "Purpose" in row and pd.notna(row["Purpose"]):
        st.markdown(f"**🎯 Purpose:** {row['Purpose']}")

    st.markdown("---")
