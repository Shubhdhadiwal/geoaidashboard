import streamlit as st
import pandas as pd

# ---------- Page Configuration ---------- #
st.set_page_config(page_title="🌍 GeoAI Repository", layout="wide")

# ---------- Title & Introduction ---------- #
st.title("🌍 GeoAI Repository")
st.markdown("""
Welcome to the **GeoAI Repository** — your one-stop destination for curated datasets, tools, and platforms 
at the intersection of **Geospatial Technology** and **Artificial Intelligence (AI)**.

This open repository is designed for:
- Researchers and students looking for reliable geospatial datasets
- AI enthusiasts exploring spatial ML/DL applications
- Policy makers and planners integrating spatial insights in decision-making

📬 You can also contribute by suggesting new resources or supporting this project via UPI.
""")

# ---------- UPI Support (Sidebar) ---------- #
st.sidebar.header("🙏 Support the GeoAI Repository")
st.sidebar.markdown("""
If this platform has helped you, consider supporting us.  
Every small contribution helps in maintaining and expanding the repository!

📌 **UPI ID:** `your-upi-id@upi`  
Or scan the QR code below:
""")

try:
    st.sidebar.image("images/your_upi_qr.png", caption="Scan to Pay via UPI", use_container_width=True)
except Exception:
    st.sidebar.warning("⚠️ QR Code image not found. Please ensure 'images/your_upi_qr.png' exists.")

# ---------- Resource Table ---------- #
st.subheader("🗂️ Available GeoAI Resources")

# ---- Sample Data ---- #
data = {
    "Data Source": [
        "Sentinel-2 Imagery", 
        "MODIS Land Surface Temperature", 
        "OpenStreetMap Buildings"
    ],
    "Link": [
        "https://sentinel.esa.int/web/sentinel/missions/sentinel-2",
        "https://modis.gsfc.nasa.gov/data/dataprod/mod11.php",
        "https://www.openstreetmap.org"
    ],
    "Type": [
        "Satellite Imagery", 
        "Temperature (Raster)", 
        "Vector Data"
    ],
    "Spatial Resolution": ["10m", "1km", "Varies"],
    "Version": ["2A", "v6", "Latest"],
    "Purpose": ["Land cover, NDVI", "Thermal analysis", "Urban mapping"]
}
df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

# ---------- Submission Form ---------- #
st.subheader("📤 Suggest a New Resource")

with st.form("submission_form"):
    name = st.text_input("Resource Name")
    link = st.text_input("Resource Link")
    res_type = st.selectbox(
        "Resource Type", 
        ["Satellite Imagery", "Tabular Data", "Vector Data", "Platform", "Other"]
    )
    submit = st.form_submit_button("Submit")

    if submit:
        st.success(f"✅ Thank you for suggesting: {name}")

# ---------- Detailed Display View ---------- #
st.subheader("🔍 Resource Details")

for idx, row in df.iterrows():
    # Title fallback
    title = row.get("Data Source") or row.get("Tools") or row.get("Title") or row.get("Tutorials") or "Unnamed"
    st.markdown(f"### 🔹 {title}")

    # Description
    if "Description" in row and pd.notna(row["Description"]):
        st.write(row["Description"])

    # Clickable Link
    link = row.get("Links") or row.get("Link") or row.get("Link to the codes")
    if pd.notna(link):
        st.markdown(f"[🔗 Access Link]({link})", unsafe_allow_html=True)

    # ----- Custom Fields ----- #
    if "Type" in row and pd.notna(row["Type"]):
        st.markdown(f"**📂 Type:** {row['Type']}")
    if "Spatial Resolution" in row and pd.notna(row.get("Spatial Resolution")):
        st.markdown(f"**📏 Spatial Resolution:** {row['Spatial Resolution']}")
    if "Version" in row and pd.notna(row.get("Version")):
        st.markdown(f"**🧾 Version:** {row['Version']}")
    if "Applicability" in row and pd.notna(row.get("Applicability")):
        st.markdown(f"**🛠️ Applicability:** {row['Applicability']}")
    if "Datasets Availability" in row and pd.notna(row.get("Datasets Availability")):
        st.markdown(f"**📊 Datasets Availability:** {row['Datasets Availability']}")
    if "Year/Month of Data Availability" in row and pd.notna(row.get("Year/Month of Data Availability")):
        st.markdown(f"**📅 Year/Month:** {row['Year/Month of Data Availability']}")
    if "Purpose" in row and pd.notna(row["Purpose"]):
        st.markdown(f"**🎯 Purpose:** {row['Purpose']}")

    st.markdown("---")

# ----- Display Data ----- #
for idx, row in df.iterrows():
    # Identify title dynamically
    title = row.get("Data Source") or row.get("Tools") or row.get("Title") or row.get("Tutorials") or "Unnamed"
    st.subheader(f"🔹 {title}")

    # Description
    if "Description" in row and pd.notna(row["Description"]):
        st.write(row["Description"])

    # Clickable link
    link = row.get("Links") or row.get("Link") or row.get("Link to the codes")
    if pd.notna(link):
        st.markdown(f"[🔗 Access Link]({link})", unsafe_allow_html=True)

    # ----- Custom Fields Based on Tab ----- #
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

    # Purpose (shown for any tab that has it)
    if "Purpose" in row and pd.notna(row["Purpose"]):
        st.markdown(f"**🎯 Purpose:** {row['Purpose']}")

    st.markdown("---")


# ---------- Footer ---------- #
st.markdown("© 2025 **GeoAI Repository** | Built with ❤️ using [Streamlit](https://streamlit.io)")
