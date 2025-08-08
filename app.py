import streamlit as st
import pandas as pd

# ----- Page Configuration ----- #
st.set_page_config(page_title="GeoAI Repository", layout="wide")

# ----- Load Excel Data ----- #
@st.cache_data
def load_data(sheet_name):
    df = pd.read_excel("Geospatial Data Repository (1).xlsx", sheet_name=sheet_name)
    df.columns = df.iloc[0]  # Set first row as header
    df = df[1:]  # Skip header row
    df = df.dropna(subset=[df.columns[0]])  # Drop rows with empty first column
    return df

# ----- Sidebar Navigation ----- #
st.sidebar.header("🧭 GeoAI Repository")

# Custom tab order: About first, then categories, then submission
sheet_options = {
    "About": "About",
    "Data Sources": "Data Sources",
    "Tools": "Tools",
    "Free Tutorials": "Free Tutorials",
    "Python Codes (GEE)": "Google Earth EnginePython Codes",
    "Courses": "Courses",
    "Submit New Resource": "Submit New Resource"
}
selected_tab = st.sidebar.radio("Select Section", list(sheet_options.keys()))

# ----- UPI Donation Section (Sidebar) ----- #
st.sidebar.markdown("---")
st.sidebar.markdown("💖 **Support This Project**")
try:
    st.sidebar.image("upi_qr.png", caption="📱 Scan QR to Contribute", use_column_width=True)
except:
    st.sidebar.warning("UPI QR image not found. Please add 'upi_qr.png' to your folder.")
st.sidebar.markdown("🙏 Thank you for your support!")

# ----- Footer (Sidebar) ----- #
st.sidebar.markdown("---")
st.sidebar.markdown("© 2025 GeoAI Repository\nCreated by [Your Name]")

# ----- About Section ----- #
if selected_tab == "About":
    st.title("📘 About GeoAI Repository")
    st.markdown("""
    The **GeoAI Repository** is a free and open resource hub for students, researchers, and professionals 
    working in geospatial analytics, machine learning, and urban/climate planning.

    This repository curates:
    - 🌐 **Public geospatial datasets**
    - 🛠️ **Open-source tools and platforms**
    - 📘 **Free learning tutorials**
    - 💻 **Python codes (especially for Google Earth Engine)**
    
    Our goal is to foster inclusive learning, open innovation, and rapid knowledge sharing in the geospatial-AI community.
    """)
    st.subheader("💡 Vision")
    st.markdown("- Democratize access to GeoAI tools and knowledge\n- Promote open science and reproducibility\n- Connect learners with meaningful resources")

    st.subheader("📬 Contact / Feedback")
    st.markdown("📧 Reach out at: [your.email@example.com](mailto:your.email@example.com)")
    st.stop()

# ----- Submission Form Section ----- #
if selected_tab == "Submit New Resource":
    st.title("📤 Submit a New Resource")
    st.markdown("Help us grow this repository by contributing useful links and resources.")

    with st.form("submit_form"):
        title = st.text_input("📌 Title")
        description = st.text_area("📝 Description")
        link = st.text_input("🔗 Link")
        category = st.selectbox("📁 Category", list(sheet_options.keys())[1:-1])  # Exclude About & Submit New
        resource_type = st.text_input("📂 Type (e.g. Satellite, Tool, Course)")
        purpose = st.text_input("🎯 Purpose or Use Case")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if title and description and link:
                st.success("✅ Thank you! Your resource has been submitted for review.")
            else:
                st.error("⚠️ Please fill out all required fields.")
    st.stop()

# ----- Load Selected Sheet Data ----- #
df = load_data(sheet_options[selected_tab])

# ----- Sidebar Search Filter ----- #
search_term = st.sidebar.text_input("🔍 Search")
if search_term:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

# ----- Sidebar Filter for "Data Sources" ----- #
if selected_tab == "Data Sources" and "Type" in df.columns:
    type_filter = st.sidebar.multiselect("📂 Filter by Type", df["Type"].dropna().unique())
    if type_filter:
        df = df[df["Type"].isin(type_filter)]

# ----- Main Content Display ----- #
st.title(f"🌍 GeoAI Repository – {selected_tab}")

for idx, row in df.iterrows():
    # Get title from any of the likely column names
    title = row.get("Data Source") or row.get("Tools") or row.get("Title") or row.get("Tutorials") or "Unnamed Resource"
    st.subheader(f"🔹 {title}")

    # Description
    if "Description" in row and pd.notna(row["Description"]):
        st.write(row["Description"])

    # Link
    link = row.get("Links") or row.get("Link") or row.get("Link to the codes")
    if pd.notna(link):
        st.markdown(f"[🔗 Access Resource]({link})", unsafe_allow_html=True)

    # Category-specific fields
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

    # Common Purpose field
    if "Purpose" in row and pd.notna(row["Purpose"]):
        st.markdown(f"**🎯 Purpose:** {row['Purpose']}")

    st.markdown("---")

# ----- Footer ----- #
st.markdown("<hr style='border:1px solid #ddd'/>", unsafe_allow_html=True)
st.markdown("📘 Powered by [Streamlit](https://streamlit.io) | © 2025 GeoAI Repository")
