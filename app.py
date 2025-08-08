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

# ---------- Resource Table ---------- #
st.subheader("🗂️ Available GeoAI Resources")

data = {
    "Name": [
        "Sentinel-2 Imagery", 
        "MODIS Land Surface Temperature", 
        "OpenStreetMap Buildings", 
        "Google Earth Engine"
    ],
    "Link": [
        "https://sentinel.esa.int/web/sentinel/missions/sentinel-2",
        "https://modis.gsfc.nasa.gov/data/dataprod/mod11.php",
        "https://www.openstreetmap.org",
        "https://earthengine.google.com/"
    ],
    "Type": [
        "Satellite Imagery", 
        "Temperature (Raster)", 
        "Vector Data", 
        "Cloud Platform"
    ]
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
except Exception as e:
    st.sidebar.warning("⚠️ QR Code image not found. Please ensure 'images/your_upi_qr.png' exists.")

# ---------- Footer ---------- #
st.markdown("---")
st.markdown("© 2025 **GeoAI Repository** | Built with ❤️ using [Streamlit](https://streamlit.io)")
