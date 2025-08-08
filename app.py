import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# --- USER AUTHENTICATION SETUP ---
# Example credentials (you can expand or store in a separate config)
names = ["John Doe", "Jane Smith"]
usernames = ["johndoe", "janesmith"]
passwords = ["123", "abc"]  # In production, use hashed passwords!

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "geoai_dashboard",  # Cookie name
    "abcdef1234",       # Cookie key
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Username or password is incorrect.")

if authentication_status is None:
    st.warning("Please enter your username and password.")

# --- MAIN APP AFTER LOGIN ---
if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome {name} 👋")

    # Load Excel
    @st.cache_data
    def load_data(sheet_name):
        df = pd.read_excel("Geospatial Data Repository (1).xlsx", sheet_name=sheet_name)
        df.columns = df.iloc[0]  # Use first row as headers
        df = df[1:]  # Skip header
        df = df.dropna(subset=[df.columns[0]])  # Drop empty rows
        return df

    # Sidebar Navigation
    sheet_options = {
        "Data Sources": "Data Sources",
        "Tools": "Tools",
        "Free Tutorials": "Free Tutorials",
        "Python Codes (GEE)": "Google Earth EnginePython Codes",
        "Courses": "Courses",
    }

    selected_tab = st.sidebar.radio("Select Category", list(sheet_options.keys()))

    # Load selected data
    df = load_data(sheet_options[selected_tab])

    st.title(f"🌍 GeoAI Repository – {selected_tab}")

    # Display filters based on sheet type
    if selected_tab == "Data Sources":
        type_filter = st.sidebar.multiselect("Filter by Type", df["Type"].dropna().unique())
        if type_filter:
            df = df[df["Type"].isin(type_filter)]

    # Display data
    for idx, row in df.iterrows():
        st.subheader(str(row.get("Data Source") or row.get("Tools") or row.get("Title") or row.get("Tutorials") or "Unnamed"))
        st.write(row.get("Description", ""))

        # Show link
        link = row.get("Links") or row.get("Link") or row.get("Link to the codes")
        if pd.notna(link):
            st.markdown(f"[🔗 Access Link]({link})", unsafe_allow_html=True)

        # Optional: Add more fields
        if "Purpose" in row:
            st.markdown(f"**Purpose:** {row['Purpose']}")
        if "Year/Month of Data Availability" in row:
            st.markdown(f"**Year/Month:** {row['Year/Month of Data Availability']}")
        st.markdown("---")
