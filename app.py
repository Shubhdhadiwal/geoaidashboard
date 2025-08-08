import streamlit as st
import pandas as pd

st.set_page_config(page_title="GeoAI Repository", layout="wide")

# ----- Load Excel ----- #
@st.cache_data
def load_data(sheet_name):
    df = pd.read_excel("Geospatial Data Repository (1).xlsx", sheet_name=sheet_name)
    df.columns = df.iloc[0]  # Use first row as headers
    df = df[1:]  # Skip the header row
    df = df.dropna(subset=[df.columns[0]])  # Drop empty rows
    return df

# ----- Sidebar Navigation ----- #
st.sidebar.header("🧭 GeoAI Repository")
sheet_options = {
    "Data Sources": "Data Sources",
    "Tools": "Tools",
    "Free Tutorials": "Free Tutorials",
    "Python Codes (GEE)": "Google Earth EnginePython Codes",
    "Courses": "Courses",
    "Submit New Resource": "Submit New Resource",
    "About": "About"
}
selected_tab = st.sidebar.radio("Select Category", list(sheet_options.keys()))

# ----- About Page ----- #
if selected_tab == "About":
    st.title("📘 About GeoAI Repository")
    st.markdown("""
        The **GeoAI Repository** is a community-curated knowledge base of datasets, tools, tutorials, and codes 
        for geospatial analysis and AI applications. The goal is to democratize access to resources 
        for students, researchers, and practitioners.
        
        This platform is managed voluntarily. If you find it helpful, consider supporting us via UPI 🙏
    """)
    st.markdown("---")
    st.subheader("💡 Vision")
    st.markdown("- Foster open knowledge sharing in geospatial AI\n- Encourage collaborative contributions\n- Support education and innovation")
    st.markdown("---")
    st.subheader("📬 Contact / Feedback")
    st.markdown("Feel free to reach out to [your-email@example.com] for collaboration or queries.")
    st.stop()

# ----- UPI Donation QR (Sticky Sidebar Option) ----- #
st.sidebar.markdown("---")
st.sidebar.markdown("💖 **Support This Project**")
st.sidebar.image("upi_qr.png", caption="UPI: yourname@upi", use_column_width=True)
st.sidebar.markdown("🙏 Thank you for your support!")

# ----- Resource Submission Form ----- #
if selected_tab == "Submit New Resource":
    st.title("📤 Submit a New Resource")

    with st.form("submit_form"):
        title = st.text_input("Title")
        description = st.text_area("Description")
        link = st.text_input("Link")
        category = st.selectbox("Category", list(sheet_options.keys())[:-2])
        resource_type = st.text_input("Type (e.g. Satellite, Python Tool, etc.)")
        purpose = st.text_input("Purpose or Use Case")

        submitted = st.form_submit_button("Submit")

        if submitted:
            st.success("✅ Thank you! Your resource has been submitted.")
            st.markdown("We will review and add it to the repository soon.")

    st.stop()

# ----- Load selected sheet data ----- #
df = load_data(sheet_options[selected_tab])

# ----- Search Filter ----- #
search_term = st.sidebar.text_input("🔍 Search")
if search_term:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

# ----- Type Filter (for specific tabs) ----- #
if selected_tab == "Data Sources":
    type_filter = st.sidebar.multiselect("📂 Filter by Type", df["Type"].dropna().unique())
    if type_filter:
        df = df[df["Type"].isin(type_filter)]

# ----- Main Title ----- #
st.title(f"🌍 GeoAI Repository – {selected_tab}")

# ----- Display Data ----- #
for idx, row in df.iterrows():
    title = row.get("Data Source") or row.get("Tools") or row.get("Title") or row.get("Tutorials") or "Unnamed"
    st.subheader(f"🔹 {title}")

    if "Description" in row and pd.notna(row["Description"]):
        st.write(row["Description"])

    link = row.get("Links") or row.get("Link") or row.get("Link to the codes")
    if pd.notna(link):
        st.markdown(f"[🔗 Access Link]({link})", unsafe_allow_html=True)

    # Category-specific details
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

# ----- Footer ----- #
st.markdown("""<hr style="border:1px solid #ccc"/>""", unsafe_allow_html=True)
st.markdown("© 2025 GeoAI Repository | Built with ❤️ using Streamlit")
